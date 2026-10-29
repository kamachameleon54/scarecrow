# AGENTS.md template

Fill every `<...>` from the interview. Delete guidance lines in parentheses. Keep the finished file under about 150 lines: it loads into every session, so each line costs tokens forever. Test each line by asking whether removing it would cause the agent to make a mistake; if not, cut it.

Contents: the AGENTS.md template, the CLAUDE.md pointer (always exactly this shape), and When the root file grows.

```markdown
# AGENTS.md: <name of this brain>

Rules for any agent working in this folder (Codex reads this file directly; Claude Code reads it through CLAUDE.md). Read this file before doing anything else in a session.

## Purpose

This folder is <owner>'s second brain for <role / practice>. It holds the background for <the two or three domains or clients>, and the work produced from it, so that a session can start from what is already known instead of being re-briefed.

## Folder map

| Folder | What lives here |
|---|---|
| `raw/` | Sources exactly as received. Never edited after they land. |
| `wiki/` | Pages compiled from `raw/`. `wiki/index.md` lists every page; `wiki/log.md` records every ingest, query worth keeping, and health check. |
| `projects/<name>/` | Work for one project or client: `status.md`, meeting notes, research, `deliverables/` (what we produced), and `received/` (what they sent, read-only). `_index.md` is the hub: its header says where the project stands, and its body lists what is there. |
| `projects/Archive/` | Finished projects that nothing in current use reads any more. |
| `open-questions.md` | Facts this brain does not know yet, each tagged with its project. |
| `_system/` | `corrections.md` (known-wrong facts) and `changelog.md` (structural changes). |
(Add one row per real top-level folder. In adopt mode, list the person's existing folders here too, with one line on what each holds.)

## Conventions

- Filenames: kebab-case, dates as YYYY-MM-DD.
- Every wiki page starts with frontmatter: `type`, `sources` (paths in `raw/` or elsewhere in this folder), `verified` (date last checked against sources).
- Link pages with relative markdown links. Keep links pointing at real files.
- Work products live in the project folder they belong to, beside the notes that produced them.
- Every project hub (`projects/<name>/_index.md`) opens with a five-field header: `status` (`active`, `paused`, `done`, or `reference`), `last-updated` (the date the header was last confirmed true, not the date the file was touched), `decision` (the latest decision only, one line starting `YYYY-MM-DD:`), `feedback` (open feedback or questions waiting on someone, with a count when there is more than one; `none` when nothing is open), and `log` (the file holding the full record, usually `status.md`). When `status.md` changes, check whether `decision` and `feedback` still hold, then bump `last-updated`. A session reads the header before the folder, so it must never fall behind the record it summarizes.
- A paused project's hub keeps a `## Parked` section: why it stopped, what would restart it, and who decides. A finished project gets `status: done` and moves to `projects/Archive/` only when nothing in current use reads it; working links into it are not the test.
- A repeatable procedure (how to run a monthly report, how to refresh a dataset) is a `runbook.md` beside the thing it operates, with frontmatter `type: runbook`, `status` (`draft`, `active`, `superseded`), and `operates` (what it runs). Never a central runbooks folder.
- Every settled rule or decision in this file carries its reason and the date it was decided: `<rule> (<reason>; decided YYYY-MM-DD)`. A fresh session reads the line and moves on instead of reopening a question already answered. When a rule changes, rewrite its line with the new reason and date and note the change in `_system/changelog.md`.
(Rules written at setup carry the setup date and the reason <owner> gave in the interview. Folder-map rows and procedure steps are not rules and need no date.)

## Ingest (adding a source)

1. Copy the source into `raw/` (kebab-case name). Do not move or edit the original.
2. Read it fully. Tell <owner> the three to five takeaways you would file, and wait for confirmation or corrections.
3. Write or update the wiki page(s) with frontmatter. Note any contradiction with existing pages instead of silently overwriting. Anything the source leaves unsettled goes into `open-questions.md`, not into a page as a guess.
4. Update `wiki/index.md` and append `## [YYYY-MM-DD] ingest | <title>` to `wiki/log.md`.
One source at a time.

## Answering questions

Look in `wiki/index.md` first, then the relevant project `_index.md` and `status.md`, then `open-questions.md` (if the answer is listed there as unknown, say so instead of guessing). Cite the page or file each answer comes from. If the answer is not in the folder, say so before using outside knowledge. A good answer worth keeping can be filed as a new wiki page.

## Received files and deliverables

Files a client or stakeholder sends go into that project's `received/` exactly as sent; never edit them. Work we produce goes into `deliverables/`. A revision is saved beside the original with a `-v2` style suffix, never over it. After adding files to `received/` or `raw/`, run the check script with `--record-raw`.

## Open questions

When an answer to a question turns up, move it out of `open-questions.md` into the page or `status.md` where it belongs, citing where it came from.

## Before anything leaves this folder

Check drafts against `_system/corrections.md`. Replace any listed wrong fact with its correction.

## Extra checks

(Report-only scripts the health-check skill runs on every visit, from the root, one command per bullet in backticks. Exit code 1 means findings. Leave the section empty at setup; add a check only when a convention here needs one that the bundled script does not cover.)

## Health check

Next health check: <YYYY-MM-DD> (then every <four> weeks).
Covers: pages whose `verified` date is older than <90> days, wiki pages missing from the index, orphan pages, broken links, pages that contradict `corrections.md`, capsule revision triggers that may have fired, open questions that have aged or been answered, project `status.md` files untouched for <30> days, project hub headers missing a field or confirmed before their `status.md` last changed, and folders that no longer match the folder map. Use the health-check skill when it is installed. Record the check in `wiki/log.md` and update the date above.

## Never

- Never edit files in `raw/` or any `received/` folder.
- Never delete or move files without <owner>'s approval; propose the change as a list first.
- Never restructure folders or rename files that other pages point to without asking.
- Never store <credentials, client-confidential material, or whatever the interview named> here.
(Add any never-touch folders the person named.)

## Capsules

Capsules (the reasoning behind finished work) go in the folder of the work they describe, with a `-capsule.md` suffix: project work in `projects/<name>/`, everything else beside the thing it explains. Never in `raw/` or a `received/` folder. Corrections register: `_system/corrections.md`. Pattern page: `wiki/patterns.md`, the one wiki page fed by capsules instead of `raw/` sources (create it on first use and add it to the index). Link style: relative markdown links.

## Change log

Record every structural change (new folder, renamed convention, new rule) in `_system/changelog.md` with the date.
```

## CLAUDE.md (always exactly this shape)

```markdown
# CLAUDE.md

Claude Code entry point for this second brain. The rules live in AGENTS.md.

@AGENTS.md
```

Why a pointer instead of a copy: two full rules files drift apart the first time one is edited. The `@AGENTS.md` line makes Claude Code load the same file Codex reads.

## When the root file grows

Past about 150 lines, move sections that only matter for one job into folder rules files, so they load only when that job runs: `## Ingest` to `wiki/AGENTS.md`, `## Capsules` and `## Extra checks` to `_system/AGENTS.md`. Put a `CLAUDE.md` containing exactly `@AGENTS.md` beside each (Claude Code loads it when a session reads a file in that folder; the ingest, capsule and health-check skills read the folder file on every run). Leave one line in the root file saying where each section went. Keep `raw/` immutability and the Never list in the root file.
