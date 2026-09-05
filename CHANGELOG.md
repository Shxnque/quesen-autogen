# Changelog

## [0.5.0] — 2026-09-05 · SDK 0.6.0 parity · offline verdict replay

### Added
- **`quesen_firewall(..., recompute=True)`** — REPLAY the verdict offline against the
  exact context and merge `receipt_recomputed` + `receipt_verification` into the
  returned envelope (BEA criticism-ledger C-003 / C-004).

### Changed
- Bumped `quesen-sdk` dependency floor to `>=0.6.0`.

## [0.4.0] — 2026-09-05 · SDK 0.5.0 parity · enforcement + verifiable receipts

### Added
- **`quesen_guard(...)`** — async fail-closed enforcement decorator: the wrapped
  coroutine runs ONLY on a PASS verdict, otherwise `TscBlocked` is raised and the
  body never runs. Verdict attached as `.last_decision`. Uses the shared
  env-configured client unless an explicit `client` is passed.
- **Independent receipt verification** on `quesen_firewall(...)`: pass
  `verify_receipt=True` (+ optional `engine_public_key_hex`) to merge
  `receipt_verified` + `receipt_verification` into the returned envelope.

### Changed
- Bumped `quesen-sdk` dependency floor to `>=0.5.0`.
- Refactored context construction into a shared `_build_context` helper reused by
  both `quesen_firewall` and `quesen_guard`.

## [0.3.0] — 2026-08-27 · Agent Firewall tool (TSC v2)

### Added
- **`quesen_firewall(...)`** — AutoGen async function tool wrapping the Quesen
  Agent Firewall (`POST /tsc/validate`): deterministic PASS/REVIEW/BLOCK/SKIP +
  audit receipt before a high-risk action. Set `QUESEN_SANDBOX=1` to self-serve
  a free key.

### Changed
- Bumped `quesen-sdk` dependency floor to `>=0.4.1`. `_client()` is now async.

## [0.2.0] — 2026-07-31 · Tracks engine v1.10.0 receipt provenance

### Changed
- Bumped `__version__` `0.1.0` → `0.2.0`.
- Bumped `quesen-sdk` dependency floor to `>=0.2.0`.
- README documents that the raw response dict from `quesen_validate(...)` now
  carries `input_snapshot_hash` and `commit_sha` when the engine is v1.10.0+.

### Notes
- No code change to the async function wrappers. Fields flow through
  automatically from `quesen-sdk` 0.2.0's `AsyncQuesenClient.validate(...).raw`.

## [0.1.0] — 2026-07-16 · Initial release
- Three async function tools for AutoGen v0.4+.

[0.2.0]: https://github.com/Shxnque/quesen-autogen/releases/tag/v0.2.0
[0.1.0]: https://github.com/Shxnque/quesen-autogen/releases/tag/v0.1.0
