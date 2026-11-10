# NIC Doctor v1.1.1

- Select PHY, complete vPort or Linux netdev counters for packet and bandwidth rates, preferring physical counters when available.
- Show the counter source for each interface, including port-wide versus PF/host scope.
- Report hardware traffic absent from netdev traffic counters without classifying it as packet loss.
- Show rates with adaptive units to distinguish low traffic from zero.
- Add `--traffic-source` to `check` and `watch` and use actual elapsed sample time for `watch`.
- Preserve standalone installation, deterministic source build, and GPL-3.0-or-later licensing.
