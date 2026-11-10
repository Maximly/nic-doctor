# Architecture

```text
nic-doctor-v1.0.7/
├── nic-doctor.sh           # Prebuilt CLI and installer
├── build.sh                # Build entry point
├── src/
│   ├── common.py           # Shared utilities and parsers
│   ├── discovery.py        # Sysfs, procfs, ethtool discovery
│   ├── topology.py         # Topology model and output formatting
│   ├── tuning.py           # Configuration, transactions, rollback
│   └── cli.py              # Command definitions and dispatch
├── tools/
│   └── build.py            # Standalone script generator
├── tests/                  # Unit and integration tests
├── README.md
└── LICENSE
```

## Build

`tools/build.py` combines the five source files in dependency order, validates the combined Python program, then compresses and embeds it into `nic-doctor.sh`. A SHA-256 digest verifies the embedded payload at runtime. Source extraction is not required.

## Installation

`nic-doctor.sh install` installs a copy of the script under the selected prefix. The installation manifest stores the installed path, version, and SHA-256. Upgrade and removal verify the manifest and installed file before changing files.

## Discovery

Hardware and interface metadata come from sysfs and procfs. Optional commands supply additional link, driver and queue information. PCIe topology is assembled from actual device ancestry, grouped by NUMA node and PCI domain.

## Configuration

Changes use explicit plans and transactions under `/var/lib/nic-doctor`. Supported actions include sysfs and procfs writes, ethtool channel changes, and representable RSS-table changes. Each action records its previous state for rollback and verifies the applied state when possible.
