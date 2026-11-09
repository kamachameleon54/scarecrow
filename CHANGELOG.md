# Changelog

## Unreleased

Offer guided and proposal-first onboarding paths, remember the selected approach in authorized progress records, and resume without repeating the welcome. Clarify that onboarding begins on first invocation unless an install-time launch has been verified in the host.

During first use, suggest an opt-in recurring gap check with guided-reminder or supported unattended-report delivery. Confirm timing, verify scheduling capability and folder access, and distinguish a real scheduled task from a saved upkeep date. Reuse standard health-check behavior and its repair approval boundaries.

Make ongoing development discoverable through ordinary-language requests, relevant milestones, and standard upkeep visits. Reuse ingest, capsule, handoff, health-check, and targeted setup extensions. Adapt through evidence, confirmed preferences, and approved small changes; keep successful ordinary work free of repeated onboarding. `health-check` 0.7.0 lets standard and deep visits raise one evidence-based development choice or fit question; quick checks, the checker script, and approval limits are unchanged. `setup` and `health-check` still work when installed without `using-scarecrow`.

Add conversational first use in `using-scarecrow` 0.2.0 and `setup` 0.7.0 for people moving from chat into file-based work. Start with one real task and source, confirm standing preferences, save a short progress record, and prepare a fresh-session retrieval check. Specific work requests and skipped walkthroughs proceed directly. Installation and cross-platform behavior remain separate validation targets.

Preserve the original outside encounter, checker findings, and focused instruction evaluations in `tests/evals/2026-11-08-first-encounter.md` so later revisions do not replace the initial evidence.

## 0.2.0 - 2026-10-28

Rules can now live beside the work that uses them. `capsule` 4.1.0 reads `_system/AGENTS.md` after the root rules file, `ingest` 1.2.0 reads `AGENTS.md` in the compiled-pages folder (default `wiki/AGENTS.md`), and `health-check` 0.6.0 accepts an Extra checks section in `_system/AGENTS.md`. `setup` 0.6.0 describes moving those sections out of the root file, each with a `CLAUDE.md` holding `@AGENTS.md` beside it, once the root passes about 150 lines, so they stop loading into every session. Root-file settings still work unchanged.

Also in this release: hardened the bundled `check_brain.py` (health-check 0.5.2, setup 0.5.1): no crashes on non-UTF-8 files, a BOM, impossible dates, or an unreadable manifest, and fewer false results for `%20` and `<...>` links, links inside code, index substring matches, and file timestamps reset by a clone or sync. Added behavior and parity tests under `tests/` with a CI workflow.

## 0.1.0 - 2026-10-26

First Scarecrow framework release. Includes the `using-scarecrow` front door and five focused components: `setup`, `ingest`, `handoff`, `capsule`, and `health-check`. Packages the six installable skill sets with a Scarecrow marketplace and plugin manifest for Claude Code and Codex.

