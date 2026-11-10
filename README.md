# NIC Doctor v1.0.7

Linux network interface discovery, PCIe/NUMA topology, IRQ/CPU mapping, diagnostics, and guarded configuration.

## Requirements

- Linux with Python 3.9 or later (standard library only).
- Optional system utilities: `ethtool`, `ip`, `lspci`, `systemctl`.
- Root privileges for installation, configuration changes, rollback, and removal.

## Install

`nic-doctor.sh` contains the complete application and can run without installation.

```sh
./nic-doctor.sh --version
./nic-doctor.sh topology
sudo ./nic-doctor.sh install
nic-doctor
```

For a custom installation prefix:

```sh
sudo ./nic-doctor.sh install --prefix /opt/nic-tools
/opt/nic-tools/bin/nic-doctor topology
```

The installer copies the script to `PREFIX/bin/nic-doctor` and records its checksum in `PREFIX/lib/nic-doctor/install.json`. It verifies an existing installation before overwriting it.

To uninstall:

```sh
sudo nic-doctor remove
```

Removal preserves NIC configuration and saved state in `/var/lib/nic-doctor`. To reverse a configuration transaction, run `sudo nic-doctor rollback` before removal.

## Build and test

The prebuilt `nic-doctor.sh` is included in the source archive.

```sh
./build.sh
python3 -m unittest discover -s tests -v
```

`build.sh` combines `src/*.py` in a fixed order, checks Python syntax, and creates a deterministic standalone shell script containing a compressed Python payload. The generated program does not require the source tree at runtime.

## Commands

| Command | Description |
| --- | --- |
| `list` | List network interfaces. |
| `show [DEVICE]` | Display interface details; defaults to all interfaces. |
| `topology` | Merged hardware, network, CPU/IRQ, or datapath tree. |
| `cpu-map DEVICE` | Show device IRQ affinity and channel-label hints. |
| `rss DEVICE` | Inspect RSS indirection; optionally rebalance it. |
| `channels DEVICE` | Inspect or configure combined hardware channels. |
| `pin DEVICE` | Assign known channel IRQs to CPUs. |
| `rps DEVICE`, `xps DEVICE` | Inspect or configure software queue steering. |
| `stats DEVICE`, `watch DEVICE` | Read counters or monitor counter deltas. |
| `diagnose DEVICE` | Check RSS, IRQ locality, and counter anomalies. |
| `snapshot`, `diff` | Save and compare NIC state. |
| `profile` | Plan, apply, or verify JSON configuration. |
| `rollback` | Restore the most recent applicable configuration transaction. |
| `remove` | Uninstall the CLI. |

Run `nic-doctor help` or `nic-doctor help COMMAND` for full usage. Running `nic-doctor` without arguments displays help.

```sh
nic-doctor list
nic-doctor show
nic-doctor show eth0
nic-doctor show 'en*'
nic-doctor topology
nic-doctor topology --device eth0
nic-doctor topology --view cpu
nic-doctor topology --view datapath
nic-doctor topology --json
nic-doctor topology --format dot > topology.dot
nic-doctor cpu-map eth0
nic-doctor stats eth0 --all
nic-doctor diagnose eth0 --duration 15
nic-doctor snapshot save before.json --device eth0 --full
nic-doctor diff before.json
```

Quote wildcard selectors to prevent shell expansion. Device names are discovered using `nic-doctor list`.

## Hardware topology

`topology` merges interfaces by NUMA node, PCI domain, and shared PCI ancestry. Devices without a PCI parent appear in a separate group.

```text
NIC Doctor  |  TOPOLOGY
Interfaces 3  |  PCI functions 2

HARDWARE TREE
Network
├─ NUMA node 0 [local CPUs 0-7]
│  └─ PCI domain 0000
│     └─ 00:01.0 — PCIe bridge [Gen3 x8]
│        ├─ 03:00.0 — Network controller
│        │  └─ enp3s0f0 [ixgbe; 10 Gb/s; up; RXQ 4 / TXQ 4]
│        └─ 03:00.1 — Network controller
│           └─ enp3s0f1 [ixgbe; 10 Gb/s; up; RXQ 4 / TXQ 4]
└─ Non-PCI interfaces (virtual, USB or other)
   └─ lo
```

PCIe speed, width, NUMA and queue values are read from the host. IRQ channel indices inferred from driver labels are hints, not verified NAPI-to-queue associations.

## Configuration

Commands that change NIC state require `--apply` and root privileges. Channel count and RSS modifications also require `--accept-disruption`.

```sh
nic-doctor pin eth0 --cpus 0-3
sudo nic-doctor pin eth0 --cpus 0-3 --apply
nic-doctor channels eth0 --combined 4
sudo nic-doctor channels eth0 --combined 4 --apply --accept-disruption
nic-doctor rss eth0 --rebalance --queues 0-3
nic-doctor rps eth0 --disable
nic-doctor xps eth0 --cpus 0-3
```

CPU pinning rejects ambiguous IRQ mappings. If `irqbalance` is active, pinning requires `--allow-irqbalance`. RSS changes require a representable original indirection table so rollback can restore its layout. A channel-count change may recreate IRQs: apply it separately before IRQ/RSS configuration.

Profiles are JSON files containing a `devices` object. Supported sections are `channels`, `irq`, `rss`, `rps`, and `xps`.

```sh
nic-doctor profile plan profile.json
sudo nic-doctor profile apply profile.json --accept-disruption
nic-doctor profile verify profile.json
sudo nic-doctor rollback
```

## Limitations

- Driver-specific NAPI-to-queue mapping may not be identifiable from the available kernel interfaces.
- Configuration changes are not persisted across resets or restarts by this release.
- Remote-host and switch-side statistics are not included in packet-loss analysis.
- Hardware/firmware may change NIC state after verification.

## Copyright and license

Copyright (C) 2026 Maxim Lyadvinsky. Licensed under the GNU General Public License v3 or later; see `LICENSE`.
