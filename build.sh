#!/bin/sh
# Copyright (C) 2026 Maxim Lyadvinsky
# SPDX-License-Identifier: GPL-3.0-or-later
# Deterministically build one self-contained NIC Doctor shell script from src/.
set -eu
cd "$(dirname "$0")"
exec python3 tools/build.py
