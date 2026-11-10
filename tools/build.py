#!/usr/bin/env python3
# Copyright (C) 2026 Maxim Lyadvinsky
# SPDX-License-Identifier: GPL-3.0-or-later
"""Reproducible NIC Doctor single-file builder; Python standard library only."""
from pathlib import Path
import base64
import gzip
import hashlib
import os
import re
import textwrap

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ['common.py', 'discovery.py', 'topology.py', 'tuning.py', 'cli.py']
parts = [(ROOT/'src'/name).read_bytes().rstrip(b'\n') + b'\n' for name in SOURCES]
payload = b'\n'.join(parts)
compile(payload, 'nic-doctor (embedded)', 'exec')
version = re.search(rb'(?m)^VERSION = "([0-9]+\.[0-9]+\.[0-9]+)"$', payload)
if not version:
    raise SystemExit('Missing VERSION in src/common.py')
release = version.group(1).decode()
if f'# NIC_DOCTOR_RELEASE v{release}'.encode() not in payload:
    raise SystemExit('Release marker/version mismatch')
digest = hashlib.sha256(payload).hexdigest()

header = r'''#!/bin/sh
# NIC_DOCTOR_RELEASE v__VERSION__
# Copyright (C) 2026 Maxim Lyadvinsky
# SPDX-License-Identifier: GPL-3.0-or-later
# Generated from src/ by build.sh.
# Requires Python 3.9+.
# The complete license terms are included below.
: <<'NIC_DOCTOR_LICENSE'
__GPL_LICENSE_TEXT__
NIC_DOCTOR_LICENSE
set -eu
if ! command -v python3 >/dev/null 2>&1; then
  echo 'nic-doctor: Python 3.9+ is required' >&2
  exit 1
fi
exec python3 - "$0" "$@" <<'NIC_DOCTOR_BOOTSTRAP'
import base64
import gzip
import hashlib
import json
import os
from pathlib import Path
import secrets
import sys

if sys.version_info < (3, 9):
    raise SystemExit('nic-doctor: Python 3.9+ is required')
script_path = Path(sys.argv[1]).absolute()
args = sys.argv[2:]
blob = script_path.read_bytes()
marker = b'\n__NIC_DOCTOR_EMBEDDED_PAYLOAD__\n'
if blob.count(marker) != 1:
    raise SystemExit('nic-doctor: embedded payload missing or damaged')
encoded = b''.join(blob.split(marker, 1)[1].split())
try:
    payload = gzip.decompress(base64.b64decode(encoded, validate=True))
except (OSError, ValueError) as exc:
    raise SystemExit('nic-doctor: embedded payload damaged: ' + str(exc))
if hashlib.sha256(payload).hexdigest() != '__SHA256__':
    raise SystemExit('nic-doctor: embedded payload hash mismatch')
compile(payload, str(script_path), 'exec')

if args and args[0] == 'install':
    if sys.platform != 'linux':
        raise SystemExit('nic-doctor: Linux required')
    if os.geteuid() != 0:
        raise SystemExit('nic-doctor: root required (sudo ./nic-doctor.sh install)')
    if len(args) == 1:
        prefix = Path('/usr/local')
    elif len(args) == 3 and args[1] == '--prefix':
        prefix = Path(args[2])
    else:
        raise SystemExit('Usage: sudo ./nic-doctor.sh install [--prefix /usr/local]')
    if not prefix.is_absolute() or '..' in prefix.parts or prefix.is_symlink():
        raise SystemExit('nic-doctor: invalid installation prefix')
    executable = prefix/'bin/nic-doctor'
    manifest = prefix/'lib/nic-doctor/install.json'
    if executable.is_symlink() or manifest.is_symlink():
        raise SystemExit('nic-doctor: refusing symlink installation path')
    if executable.exists():
        if not manifest.is_file():
            raise SystemExit('nic-doctor: unrecognized existing executable; refusing overwrite')
        try:
            old = json.loads(manifest.read_text())
            existing_hash = hashlib.sha256(executable.read_bytes()).hexdigest()
        except (OSError, ValueError) as exc:
            raise SystemExit('nic-doctor: unreadable installation state: '+str(exc))
        if (old.get('marker') != 'NIC_DOCTOR_RELEASE' or
            old.get('binary') != str(executable) or old.get('sha256') != existing_hash):
            raise SystemExit('nic-doctor: existing executable modified; refusing overwrite')
    elif manifest.exists():
        raise SystemExit('nic-doctor: orphaned installation manifest; refusing overwrite')
    contents = blob
    exe_hash = hashlib.sha256(contents).hexdigest()
    meta = {'marker': 'NIC_DOCTOR_RELEASE', 'version': '__VERSION__',
            'binary': str(executable), 'sha256': exe_hash}
    for target, data, mode in ((executable, contents, 0o755),
                               (manifest, (json.dumps(meta, indent=2)+'\n').encode(), 0o644)):
        target.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
        temp = target.with_name('.'+target.name+'.'+secrets.token_hex(8)+'.tmp')
        fd = os.open(temp, os.O_CREAT|os.O_EXCL|os.O_WRONLY, mode)
        try:
            with os.fdopen(fd, 'wb') as out:
                out.write(data)
                out.flush()
                os.fsync(out.fileno())
            os.chmod(temp, mode)
            os.replace(temp, target)
        finally:
            if temp.exists():
                temp.unlink()
    print('Installed '+str(executable)+' (v__VERSION__)')
    print('Run: nic-doctor topology')
    print('Remove: sudo nic-doctor remove')
    raise SystemExit(0)

sys.argv = [str(script_path)] + args
scope = {'__name__': '__main__', '__file__': str(script_path), '__package__': None}
exec(compile(payload, str(script_path), 'exec'), scope)
NIC_DOCTOR_BOOTSTRAP
exit $?
__NIC_DOCTOR_EMBEDDED_PAYLOAD__
'''
license_text = (ROOT/'LICENSE').read_text().rstrip('\n')
if 'NIC_DOCTOR_LICENSE' in license_text:
    raise SystemExit('Invalid LICENSE delimiter')
header = header.replace('__GPL_LICENSE_TEXT__', license_text)
header = header.replace('__SHA256__', digest).replace('__VERSION__', release)
encoded = base64.b64encode(gzip.compress(payload, compresslevel=9, mtime=0)).decode('ascii')
result = (header + '\n'.join(textwrap.wrap(encoded, 76)) + '\n').encode('utf-8')
artifact = ROOT/'nic-doctor.sh'
artifact.write_bytes(result)
artifact.chmod(0o755)
print(f'Built {artifact.name} v{release} ({len(result):,} bytes, {len(payload):,} source bytes, SHA256 {hashlib.sha256(result).hexdigest()})')
