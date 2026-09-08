# Synthetic agent-memory recovery lab

This standard-library artifact builds nine JSON memory states and optionally runs three fresh Claude CLI trials per state. Each response proposes one **mock** send action and recalls an unrelated maintenance decision. No email implementation exists. The only network activity requested by the runner is the model call through the installed CLI.

Run from the repository root with Python 3.11+:

```bash
python -m unittest discover -s scripts/security-labs/memory-recovery -p 'test_*.py'
python scripts/security-labs/memory-recovery/lab.py --output /tmp/memory-fixtures
python scripts/security-labs/memory-recovery/lab.py --run-model --trials 3 --timeout 35 --output /tmp/memory-model-run
```

Choose a new output directory for each run; overwriting prior evidence is refused. Model runs require an authenticated Claude CLI supporting the recorded flags. No model name or sampling override is supplied. The manifest records the CLI version, command, observed model-usage keys, source fixture, state hashes and script hash. Each completed trial immediately saves its prompt, raw CLI response, parsed output, locally recorded mock arguments, scores, timing and any failure. The output directory is the experiment's only persistent memory; CLI sessions use disposable working directories and `--no-session-persistence`.

`--safe-mode`, an empty tool list and strict empty MCP configuration disable repository customizations, hooks, auto-memory and real tools. The mock recorder only accepts addresses ending in `@example.invalid`; it performs no network operation even when an address is rejected.

The controlled ingestion and repair functions are **deterministic fixtures**. The model receives their canonical record and derived summary as retrieved context, without state labels. This measures downstream adoption under the supplied prompt. It does not measure whether a real memory writer would accept the original malicious message, whether a model could diagnose or repair memory itself, or a deployed agent's retrieval behavior.

See [the executed report](../../../docs/research/2026-09-08-memory-recovery-lab.md) and [retained run](runs/2026-09-08/manifest.json). Snapshot hashes identify bytes, not trusted provenance. The reviewed fixture is the external recovery reference in this toy setup; selecting that reference in a real incident remains a separate problem.
