# Changelog

## 0.2.0 - 2026-10-28

Rules can now live beside the work that uses them. `capsule` 4.1.0 reads `_system/AGENTS.md` after the root rules file, `ingest` 1.2.0 reads `AGENTS.md` in the compiled-pages folder (default `wiki/AGENTS.md`), and `health-check` 0.6.0 accepts an Extra checks section in `_system/AGENTS.md`. `setup` 0.6.0 describes moving those sections out of the root file, each with a `CLAUDE.md` holding `@AGENTS.md` beside it, once the root passes about 150 lines, so they stop loading into every session. Root-file settings still work unchanged.

Also in this release: hardened the bundled `check_brain.py` (health-check 0.5.2, setup 0.5.1): no crashes on non-UTF-8 files, a BOM, impossible dates, or an unreadable manifest, and fewer false results for `%20` and `<...>` links, links inside code, index substring matches, and file timestamps reset by a clone or sync. Added behavior and parity tests under `tests/` with a CI workflow.

## 0.1.0 - 2026-10-26

First Scarecrow framework release. Includes the `using-scarecrow` front door and five focused components: `setup`, `ingest`, `handoff`, `capsule`, and `health-check`. Packages the six installable skill sets with a Scarecrow marketplace and plugin manifest for Claude Code and Codex.
