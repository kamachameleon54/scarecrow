# Changelog

## Unreleased

Hardened the bundled `check_brain.py` (health-check 0.5.2, setup 0.5.1): no crashes on non-UTF-8 files, a BOM, impossible dates, or an unreadable manifest, and fewer false results for `%20` and `<...>` links, links inside code, index substring matches, and file timestamps reset by a clone or sync. Added behavior and parity tests under `tests/` with a CI workflow.

## 0.1.0 - 2026-10-26

First Scarecrow framework release. Includes the `using-scarecrow` front door and five focused components: `setup`, `ingest`, `handoff`, `capsule`, and `health-check`. Packages the six installable skill sets with a Scarecrow marketplace and plugin manifest for Claude Code and Codex.
