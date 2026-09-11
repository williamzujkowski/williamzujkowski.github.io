# Offline retention state model

An original educational model inspired by the frozen/countdown/free transition
in Timelock Drive (OSDI 2026), not the authors' implementation or a replication.

From the repository root:

```bash
python3 scripts/security-labs/timelock/timelock_model.py
python3 -m unittest discover -s scripts/security-labs/timelock -p 'test_*.py'
```

The runner emits eight deterministic cases with at most 1,000 total synthetic
operations. It uses only in-memory strings and integer ticks. It does not read
or write backups, open devices, access a network, or execute other programs.
The retained JSON output is `results-2026-09-11.json`.

An already-written, frozen value stays protected indefinitely. Unfreezing starts
the original seven-tick duration; this model conservatively permits mutation
only strictly after its expiry tick. Host clock updates cannot affect the trusted
checker clock. Backward checker updates fail without changing clock state.
`trust_host_clock=True` deliberately breaks that assumption for a positive control.

Python object fields are directly mutable. Thus this program enforces no security
boundary against its caller or host. It omits storage interfaces, persistent clocks,
power failures, protected metadata logs, cryptographic integrity, device firmware,
space reclamation, and recovery selection. Passing tests does not verify any of
those mechanisms, the paper's formal proof, or a backup product.

Source and claim provenance: [research note](../../../docs/research/2026-09-11-timelock-model.md).

A second deliberately broken control begins expiry at creation, allowing deletion
of a still-live value after sufficient time without an unfreeze operation.
