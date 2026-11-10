#!/usr/bin/env python3
# Copyright (C) 2026 Maxim Lyadvinsky
# SPDX-License-Identifier: GPL-3.0-or-later
# NIC_DOCTOR_RELEASE v1.1.0
"""Linux network interface discovery, diagnostics, and configuration."""
import argparse
from contextlib import contextmanager
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import sys
import time

VERSION = "1.1.0"
AUTHOR = "Maxim Lyadvinsky"
COPYRIGHT = "Copyright (C) 2026 Maxim Lyadvinsky"
LICENSE_ID = "GPL-3.0-or-later"
DEVICE_RE = re.compile(r"^[A-Za-z0-9_.:@-]{1,64}$")
IRQ_RE = re.compile(r"^\d+$")
DROP_RE = re.compile(r"(?:drop|discard|out_of_buffer|buffer_alloc_err|wqe_err|missed|error|timeout|recover)", re.I)


class DoctorError(Exception):
    pass


def read(path, default=None):
    try:
        return Path(path).read_text().strip()
    except (OSError, UnicodeError):
        return default


def run(*argv, timeout=8):
    if not shutil.which(argv[0]):
        return None
    try:
        p = subprocess.run(list(argv), text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=timeout, check=False)
        return p.stdout if p.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def parse_cpulist(value):
    if value is None or not re.fullmatch(r"\s*\d+(?:-\d+)?(?:\s*,\s*\d+(?:-\d+)?)*\s*", value):
        raise DoctorError("invalid CPU list; expected e.g. 8-21 or 2,4,6-9")
    out = set()
    for part in value.split(','):
        s = part.strip()
        if '-' in s:
            a, b = map(int, s.split('-'))
            if b < a or b-a > 8192:
                raise DoctorError("invalid CPU range")
            out.update(range(a, b+1))
        else:
            out.add(int(s))
    if not out or max(out) > 1048575:
        raise DoctorError("invalid CPU range")
    return sorted(out)


def cpulist(values):
    nums = sorted(set(int(x) for x in values))
    if not nums:
        return ""
    groups, first, last = [], nums[0], nums[0]
    for x in nums[1:]:
        if x == last + 1:
            last = x
        else:
            groups.append(f"{first}-{last}" if first != last else str(first))
            first = last = x
    groups.append(f"{first}-{last}" if first != last else str(first))
    return ','.join(groups)


def cpu_mask(values):
    bitmap = 0
    for c in values:
        bitmap |= 1 << c
    text = f"{bitmap:x}"
    parts = []
    while text:
        parts.append(text[-8:].zfill(8))
        text = text[:-8]
    return ','.join(reversed(parts)) if parts else '00000000'


def mask_cpus(value):
    try:
        num = int(value.replace(',', ''), 16)
        if num.bit_length() > 1048576:
            return []
        return [i for i in range(num.bit_length()) if num & (1 << i)]
    except (AttributeError, ValueError):
        return []


def ethtool_channels(raw):
    """Return {'maximum': {...}, 'current': {...}} or null."""
    if not raw:
        return None
    blocks = {'maximum': {}, 'current': {}}
    block = None
    for line in raw.splitlines():
        if 'Pre-set maximums:' in line:
            block = 'maximum'
        elif 'Current hardware settings:' in line:
            block = 'current'
        elif block:
            m = re.match(r"\s*(RX|TX|Other|Combined):\s*(\d+|n/a)\s*$", line, re.I)
            if m:
                blocks[block][m.group(1).lower()] = None if m.group(2).lower() == 'n/a' else int(m.group(2))
    return blocks if blocks['current'] else None


def ethtool_rss(raw):
    """Parse the default RSS indirection table; do not confuse RSS hash-key lines with queue entries."""
    if not raw:
        return None
    rows = {}
    for line in raw.splitlines():
        m = re.match(r"^\s*(\d+):\s+((?:\d+\s*)+)$", line)
        if m:
            at = int(m.group(1))
            for i, value in enumerate(m.group(2).split()):
                rows[at+i] = int(value)
    if not rows or sorted(rows) != list(range(len(rows))):
        return None
    return [rows[i] for i in range(len(rows))]


def rss_equal_model(table):
    """Find exactly representable (start, equal N) layout; never approximate RSS rollback."""
    if not table:
        return None
    start = table[0]
    for n in range(1, min(len(table), 4096)+1):
        if all(x == start + (i % n) for i, x in enumerate(table)):
            return {'start': start, 'equal': n}
    return None


def ethtool_stats(raw):
    result = {}
    if raw:
        for line in raw.splitlines():
            m = re.match(r'^\s*([A-Za-z0-9_.-]+):\s*(-?\d+)\s*$', line)
            if m:
                result[m.group(1)] = int(m.group(2))
    return result
