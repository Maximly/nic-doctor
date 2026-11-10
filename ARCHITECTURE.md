# Architecture

```text
nic-doctor-v1.1.1/
├── nic-doctor.sh          # Prebuilt standalone CLI and installer
├── build.sh
├── src/
│   ├── common.py         # Shared types, parsers and command helpers
│   ├── discovery.py      # Sysfs, procfs and ethtool NIC discovery
│   ├── topology.py       # Tree structure and output presentation
│   ├── tuning.py         # Plans, guarded changes, journal and rollback
│   ├── analysis.py       # Evidence-based checks and CPU placement
│   └── cli.py            # Commands and argument parsing
├── tools/build.py        # Deterministic embedded-payload builder
├── tests/
├── LICENSE
└── README.md
```

## Runtime

NIC data is read from sysfs, procfs and optional system commands. Inventory and sampled counters are collected separately. `check` evaluates observed state with bounded rules that preserve source and scope, instead of treating all counters as directly additive. Reports are available in text and JSON.

The CPU planner requires a demonstrable channel-labelled PCI MSI-X set, available NUMA locality and physical CPU topology. It does not assume that IRQs, NAPI instances and queues have a universal one-to-one mapping. Configuration writes are journaled and verified by the existing transaction subsystem.

## Build and install

`tools/build.py` combines source files in dependency order into a checked, compressed Python payload, embedded in `nic-doctor.sh` with a SHA-256 digest. The shell script invokes Python from its own payload without extracting files. Installation copies the same script to the chosen prefix and stores its checksum in an installation manifest. `nic-doctor remove` validates this manifest before removal.
