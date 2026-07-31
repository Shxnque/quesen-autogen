# Changelog

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
