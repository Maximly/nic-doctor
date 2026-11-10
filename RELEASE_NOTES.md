# NIC Doctor v1.1.0

- Added `status` for concise, automatic physical-NIC inventory.
- Added `check` with evidence-based PCIe, RSS, IRQ/NUMA/core placement, and sampled drop/error diagnostics.
- Added `explain` for PCIe/RSS/IRQ/CPU/XDP datapath relationships and mapping limitations.
- Added `optimize` for conservative NUMA/physical-core-aware IRQ affinity planning, explicit CPU reservations, SMT controls, JSON output, optional profile export, and guarded apply.
- Hardened channel IRQ validation to require PCI MSI-X membership.
- Preserved existing low-level commands, single-file installer, deterministic builds, and GPL-3.0-or-later licensing.
