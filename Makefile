# Copyright (C) 2026 Maxim Lyadvinsky
# SPDX-License-Identifier: GPL-3.0-or-later
.PHONY: build test check
build:
	./build.sh

test: build
	python3 -m unittest discover -s tests -v

check: test
	./nic-doctor.sh --version
	./nic-doctor.sh help topology
