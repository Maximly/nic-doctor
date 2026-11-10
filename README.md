# NIC Doctor v1.1.1

Topology-aware Linux NIC diagnostics, problem-oriented checks, and guarded configuration.

Copyright (C) 2026 Maxim Lyadvinsky. Licensed under GNU GPL version 3 or later.

## Requirements

- Linux, Python 3.9+ (standard library only).
- Optional utilities: `ethtool`, `ip`, `lspci`, `systemctl`.
- Root for installation, configuration changes, rollback, and removal.

## Installation

`nic-doctor.sh` is the complete executable and installer. It runs without installation or access to `src/`.

```sh
./nic-doctor.sh status
sudo ./nic-doctor.sh install
nic-doctor --version
```

The install prefix can be changed with `--prefix /path`. To uninstall, use `sudo nic-doctor remove`. Saved transactions under `/var/lib/nic-doctor` are not deleted by removal.

## Quick start

```sh
nic-doctor                         # Help
nic-doctor status                  # Concise inventory (PCI NICs by default)
nic-doctor check                   # Check all PCI NICs, one sampled interval
nic-doctor check eth0 --duration 15
nic-doctor check eth0 --focus loss
nic-doctor check --json
nic-doctor explain eth0            # Packet path and mapping evidence
nic-doctor optimize                # Preview IRQ placement for all PCI NICs
nic-doctor optimize eth0 --goal max-pps
nic-doctor optimize eth0 --avoid-cpus 0-7
nic-doctor optimize eth0 --profile-out profile.json
nic-doctor topology                # Merged NUMA/PCIe hardware tree
```

When no PCI-backed interfaces exist, `status`, `check`, and `optimize` fall back to non-loopback interfaces. Use `--all` to include all network interfaces, including virtual interfaces and loopback.

## Problem-oriented commands

### `status [DEVICE]`

Shows interface, driver, link state, negotiated NIC speed, NUMA, channel count, and RX/TX queue counts without sampling traffic. It does **not** infer that packets are being delivered correctly just because the link is up.

### `check [DEVICE]`

Reports actionable findings with severity, supporting evidence, explanation, recommended next step, and confidence. Checks include:

- PCIe link negotiated below endpoint capability (potential limitation, not proof of saturation).
- RSS table references outside the current combined-channel range; uneven indirection weights are informational, not equivalent to traffic skew.
- NIC-local NUMA versus IRQ effective CPU affinity.
- Multiple channel-labelled IRQs sharing physical cores while other local cores are unused.
- Increasing standard and driver-specific drop/error counters over a single shared measurement interval.
- Traffic rate source selection: physical-port counters (preferred, port-wide), complete vPort counters, or standard netdev counters; the active source is reported.
- Missing or ambiguous mapping information, without guessing IRQ-to-queue relationships.

`--traffic-source auto|phy|vport|netdev` selects the rate-counter domain (default `auto`). For mlx5/XDP traffic, PHY counters can increase while netdev counters stay at zero. The `watch` command accepts the same option. A PHY rate measures a physical port, not necessarily traffic delivered to a particular PF or XDP program.

`--focus` accepts `all`, `loss`, `rss`, `placement`, `pcie`, or `link`. `--duration 0` disables counter-delta sampling. `--strict` exits with status 2 if the report contains warnings. `--json` writes machine-readable findings.

Counters are not added across different scopes. Only nonnegative deltas are used. A zero delta is **not** proof that upstream packet loss is absent. Counter sampling cannot establish the throughput or PPS capacity of a device without a controlled workload.

### `explain DEVICE`

Shows PCIe ancestry, NUMA locality, NIC RX/TX queues, RSS indirection weights, channel-labelled PCI MSI-X vectors and their effective CPU affinities, and XDP attachment state (where reported). Channel labels do not independently prove queue/NAPI/IRQ identity.

### `optimize [DEVICE]`

Plans **only IRQ CPU placement**. It selects NUMA-local online physical cores, uses one distinct physical core per completion IRQ where possible, preserves already valid mappings, and avoids cores assigned to other known NIC completion IRQs for a single-device plan. It refuses plans with unproven channel/IRQ association, missing NUMA/core information, or insufficient eligible physical cores.

| Option | Purpose |
| --- | --- |
| `--goal balanced\|max-pps\|max-throughput\|low-latency\|cpu-efficient` | Intent label; no performance gain is asserted without measurements. |
| `--cpus 4-11` | Explicit ordered CPU selection, overriding automatic NUMA placement. |
| `--avoid-cpus 0-3` | Reserve CPUs from automatic placement. |
| `--allow-smt` | Permit SMT siblings only when physical cores are insufficient. |
| `--profile-out profile.json` | Save the plan as an existing JSON `profile` configuration. |
| `--json` | Structured plan. |
| `--apply` | Perform supported IRQ-affinity changes after validation, transaction journaling and verification. |
| `--allow-irqbalance` | Explicitly acknowledge active irqbalance when applying. |

Use `nic-doctor optimize` without `--apply` first. Any blocked device prevents a multi-device apply rather than allowing partial changes. Plans intentionally do not resize queues, rebalance RSS, disable RPS, or change offloads.

**Remote safety:** IRQ affinity writes can affect a management interface. This release has no independent connectivity watchdog or boot persistence. Use out-of-band access for potentially disruptive remote operations. The existing transaction mechanism attempts rollback if a write or verification fails while the process is running, and records configuration state for manual `sudo nic-doctor rollback`.

## Additional commands

| Command | Purpose |
| --- | --- |
| `list`, `show [DEVICE]` | Device inventory and detailed information. |
| `topology [--view hardware\|network\|cpu\|datapath]` | Merged Unicode tree; JSON and DOT exports. |
| `cpu-map DEVICE` | IRQ labels, effective/configured CPU affinity, interrupt counts. |
| `rss DEVICE`, `channels DEVICE` | Inspect or change hardware queues and RSS (guarded). |
| `pin DEVICE`, `rps DEVICE`, `xps DEVICE` | Low-level steering and IRQ configuration. |
| `stats DEVICE`, `watch DEVICE`, `diagnose DEVICE` | Counters, sampling, and previous diagnostic report. |
| `snapshot`, `diff` | Capture and compare host state. |
| `profile plan\|apply\|verify FILE` | Plan, apply, and verify a JSON profile. |
| `rollback [ID]` | Restore an earlier journaled transaction. |
| `help [COMMAND]`, `remove` | CLI help and uninstall. |

Low-level mutating commands default to dry run and require `--apply`. Channel and RSS modifications also require `--accept-disruption`.

## Build and test

The source archive includes the prebuilt script and a readable source tree; no examples directory is included.

```sh
./build.sh
python3 -m unittest discover -s tests -v
```

The build is deterministic. `tools/build.py` verifies the Python payload, compresses it and embeds it inside the single executable `nic-doctor.sh`; the embedded program checks a SHA-256 digest at runtime. No `nic-doctor` companion executable or runtime source directory is required.

## Limitations

- A channel-labelled IRQ is not a verified NAPI/queue identity. Unlabelled or ambiguous devices may be rejected by the optimizer.
- Automatically inferred optimal channel counts, RSS distributions, coalescing settings, and application performance are not supported.
- Collector coverage depends on driver, kernel and installed utilities. Some NICs lack RSS data or expose physical-port counters shared by multiple interfaces.
- Counter deltas from the receiver alone cannot explain packets lost before reaching the receiver MAC.
- Configuration is not automatically made persistent across driver reset or reboot.
- Physical ConnectX/Intel/Broadcom hardware tuning has not yet been validated for this release.
