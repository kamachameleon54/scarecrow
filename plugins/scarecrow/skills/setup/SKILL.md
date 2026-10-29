---
name: setup
description: "Builds or adopts a durable second brain that Claude Code or Codex can read and maintain: a plain-markdown folder with a root rules file, immutable sources compiled into a wiki, project work kept beside its context, a corrections register, and dated upkeep. Use when creating a new Scarecrow brain, adding Scarecrow structure around an existing notes folder or Obsidian vault, or setting up AGENTS.md and its CLAUDE.md pointer for agent-maintained knowledge. Not for ingesting one source, session handoff, finished-work capsules, or routine health checks."
metadata:
  status: draft
  version: 0.6.0
  tags: [second-brain, llm-wiki, knowledge-base, claude-code, codex]
  feedback: ""
  decision: "2026-10-28: Document moving Ingest, Capsules and Extra checks to folder rules files when the root grows"
  log: "#Changelog"
  last-updated: 2026-10-28
---

# Setup

Set up the structure and local rules for a Scarecrow second brain. Existing knowledge lives in documents, notes, and finished work; this skill makes that background findable by Claude Code or Codex at the start of a session. Read the target folder's root rules and any more-specific rules before applying this skill. Local rules override these package defaults.

The result is a **hybrid second brain**: context (sources, compiled notes, meeting records, decisions) stored beside the work it produced (deliverables, reusable prompts, status files), governed by one rules file. The pattern comes from Andrej Karpathy's LLM Wiki idea file (https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and adds two parts his gist leaves open: work kept beside its context, and a corrections register with scheduled upkeep.

## Two modes

Pick the mode from the folder, not from the wording of the request:

- **Build new**: the target folder does not exist, is empty, or holds only a few loose files. Scaffold everything.
- **Adopt existing**: the folder already holds notes (an Obsidian vault, a docs folder, a pile of markdown). Add the structure around what is there and move nothing without approval. Read `references/adopt-mode.md` before touching anything.

List the folder first (`ls -la`, then a count of files by extension) so the mode decision rests on what is actually there.

## The four parts

Every brain this skill builds has these four parts. Explain them to the person in one or two sentences each before scaffolding, because they will maintain it and need to know why each piece exists.

| Part | What it is | Why it matters |
|---|---|---|
| Rules file | `AGENTS.md` at the root, with `CLAUDE.md` as a one-line pointer to it | The agent reads it at session start, so it never has to be re-briefed. Codex reads `AGENTS.md` natively; Claude Code reads `CLAUDE.md`, which imports it. One source of truth, no drift between two copies. |
| Sources to compiled notes | `raw/` holds sources that are never edited; `wiki/` holds pages the agent compiles from them, with `wiki/index.md` and an append-only `wiki/log.md` | Synthesis happens once and accumulates, instead of re-reading raw documents on every question. Immutable sources mean any compiled claim can be checked against what was actually said. |
| Work beside its context | `projects/<name>/` folders holding deliverables, a `status.md`, the meeting notes and research behind them, and a read-only `received/` folder for what the client or stakeholder sent, each with a short `_index.md` hub whose header gives the project's status, latest decision, and open feedback | When the agent drafts a follow-up, the decisions, open items, and the client's own documents are in the same folder, and the hub header says where things stand before anything else is opened. Keeping what was received separate from what was produced means the agent never confuses its own draft with the client's original. This is the part a plain notes app misses. |
| Corrections and upkeep | `_system/corrections.md` (known-wrong facts and their fixes), `open-questions.md` at the root (facts the brain does not know yet), and `_system/changelog.md` (structural changes), plus an upkeep date in the rules file | Compiled notes go stale and wrong facts propagate. Gaps get papered over with guesses unless there is a named place to put an unknown. Practitioners who left maintenance on-demand found it never happened; a dated cadence and a register checked before anything ships keep the brain trustworthy. |

## Workflow

### 1. Interview (short)

Ask one question at a time; stop as soon as you have enough. If the request already answers a question, do not ask it again.

1. What work will this brain support? (role, recurring tasks, the two or three domains or clients that matter most)
2. Which agents will use it: Claude Code, Codex, or both?
3. Where should it live, and is the folder under git or a synced drive?
4. What sources are already in hand to seed it?
5. Anything that must never be touched, shared, or stored here (client confidential material, credentials, another tool's folders)?

If the person cannot answer now, use sensible defaults, write them into the rules file, and list them in the final summary as assumptions to revisit.

### 2. Scaffold

Create this layout (build mode) or the missing pieces of it (adopt mode):

```
<root>/
├── AGENTS.md                 # authoritative rules (template in references/agents-md-template.md)
├── CLAUDE.md                 # exactly: a title line, a one-line purpose, and "@AGENTS.md"
├── open-questions.md         # facts the brain does not know yet, each tagged with its project
├── raw/
│   └── README.md             # "Sources land here and are never edited."
├── wiki/
│   ├── index.md              # catalog: one line per page, grouped by category
│   └── log.md                # append-only: ## [YYYY-MM-DD] <operation> | <title>
├── projects/
│   └── <name>/
│       ├── _index.md         # hub: header (status, last-updated, decision, feedback, log), then what lives here
│       ├── status.md         # current state, decisions, open items (to-dos)
│       ├── received/         # read-only: files the client or stakeholder sent, kept exactly as received
│       └── deliverables/     # what was produced for them; revisions saved beside originals (-v2), never over them
└── _system/
    ├── corrections.md        # known-wrong facts → correct facts, with dates
    └── changelog.md          # dated structural changes
```

Page and file formats are in `references/page-templates.md`. Keep to this layout. Extra folders, dashboards, tag taxonomies, embeddings, and connectors all add upkeep before the workflow has shown it needs them; mention them as later options, do not build them. The same goes for tooling around the hub header: an edit-time hook that warns when a header falls behind, or a notes-app view (such as an Obsidian Base) that lists every hub by status, earns its place once the brain holds more projects than the owner can scan by hand.

If the folder is a git repository, or the person agrees to make it one, commit after scaffolding. Version history is what makes agent writes reversible.

### 3. Write the rules file

Fill `references/agents-md-template.md` from the interview. The rules file is what the agent will obey for months, so make it specific: name the real domains and project folders, the real never-touch list, and the upkeep date. Keep it under about 150 lines; procedure that only matters occasionally can live in a referenced file. When it grows past that, move sections to folder rules files that load only when needed: the Ingest section to `wiki/AGENTS.md`, the Capsules and Extra checks sections to `_system/AGENTS.md`, each with a `CLAUDE.md` beside it containing `@AGENTS.md`, and a one-line pointer left in the root file. The ingest, capsule and health-check skills read those files. Every settled rule carries its reason and the date it was decided (template, Conventions); a rule with neither is the one a fresh session reopens. Fill each project hub's header from what the person said about that project; a field with no answer yet gets `none` or a line in `open-questions.md`, never a guess. Leave the Extra checks section empty.

### 4. First ingest, together

Ingest the person's first sources **one at a time with the person involved**, as Karpathy recommends. For each source:

1. Copy (never move) it into `raw/` with a kebab-case name, then run `python3 <skill-dir>/scripts/check_brain.py <root> --record-raw` so its checksum is on record. In adopt mode, existing notes can stay where they are and be cited in place.
2. Read it fully and tell the person the three to five takeaways you would file.
3. Let the person correct, cut, or confirm them. This is the step that keeps interpretation with the person; compiled pages tend to overstate their sources when nobody checks.
4. Write or update the wiki page(s), with frontmatter `type`, `sources`, and `verified` (today's date). Link related pages with relative markdown links.
5. Add or update the line in `wiki/index.md` and append an entry to `wiki/log.md`.
6. Anything the source leaves unsettled that matters for the work (a missing date, an unconfirmed eligibility rule, an unnamed owner) goes into `open-questions.md` rather than into a page as a guess.

Two to five sources is enough to prove the loop works. If the person is not available to confirm takeaways (for example, they asked you to run unattended), file them anyway but mark each page `verified: pending` and list them in the summary for review.

### 5. Set the upkeep cadence

Write a dated "next health check" into `AGENTS.md` (default: four weeks out) and describe what the check covers: stale `verified` dates, wiki pages missing from the index, orphan pages, broken links, entries in `corrections.md` that compiled pages still contradict, and drift between the rules file and the real folders. Offer to schedule a reminder; create one only if the person says yes.

### 6. Verify

Run the bundled check from the brain's root:

```bash
python3 <skill-dir>/scripts/check_brain.py <root> --structure   # add --adopt in adopt mode
```

`--structure` runs the checks a fresh brain must pass (the full run adds the upkeep checks that the health-check skill uses on later visits). It checks that the required files exist, that `CLAUDE.md` points to `AGENTS.md`, that every wiki page has frontmatter with a `type`, that each project hub carries the five header fields with valid values, that the index lists every wiki page, that relative links resolve, and that `raw/` files match the manifest recorded at ingest (so a later session that edits a source gets caught). It also warns when `AGENTS.md` runs past 150 lines. Fix anything it reports before handing over.

Then suggest the real test: open a fresh session in the folder and ask a background question about the person's work. A working brain answers without re-briefing and cites the page it used.

### 7. Hand over

End with a short summary: mode used, what was created (paths), sources ingested, assumptions made, the upkeep date, and two or three example prompts the person can try in a fresh session.

## Boundaries

These protect the person's existing work and the brain's trustworthiness:

- Never edit a file in `raw/` or in a project's `received/` folder after it lands. If a source is wrong, record the fix in `_system/corrections.md`. Run `--record-raw` after adding files to either so the check script can catch later edits.
- Never delete or move the person's files. Propose moves as a list; carry them out only after approval.
- Never overwrite an existing `AGENTS.md` or `CLAUDE.md`. Merge new sections into it with the person's approval, keeping their wording.
- Never store credentials, tokens, or anything the person marked never-store.
- Ask before restructuring folders; renames break every pointer to the old path.

## Common mistakes

| Mistake | Fix |
|---|---|
| Two full rules files (`CLAUDE.md` and `AGENTS.md`) with copied content | `AGENTS.md` holds the rules; `CLAUDE.md` is a pointer with `@AGENTS.md` |
| Bulk-ingesting a whole folder of sources in one pass | One source at a time with the person; the first few runs set the quality bar |
| Compiled pages with no frontmatter or sources | Every wiki page carries `type`, `sources`, `verified` |
| Building dashboards, tag schemes, and vector search on day one | Leave them out; note them as options once the index stops being enough (around a hundred sources) |
| Moving someone's notes into the new layout in adopt mode | Leave files in place; index and cite them where they are |
| Upkeep described as "periodically" | A real date in the rules file |
| Project state kept only in `status.md`, or a second state field beside `status` | The hub header gives status, latest decision, and open feedback at a glance; one field name, `status`, across the brain |
| Header lines that restate the whole status file | `decision` is the latest decision only; `log` points at the full record |

## Setup

Python 3.9 or later; `scripts/check_brain.py` uses the standard library only. The script is a copy of the health-check skill's canonical `scripts/check_brain.py`. The repository's `tests/test_vendored_script.py` checks parity, and CI runs it with the script's behavior tests. Edit the health-check copy and copy it here, never the reverse. No config file. The agent needs read and write access to the target folder.

## Coordinates with

- using-scarecrow: routes framework requests to this setup procedure; direct invocation also works
- capsule: files finished-work reasoning into the brain this skill builds, using the rules file's capsules section
- handoff: carries unfinished work to a new session; a brain lets it point at status.md and open-questions.md instead of restating them
- ingest: adds later sources one at a time after setup
- health-check: runs the dated upkeep visit this skill schedules, and owns the check script this skill ships a copy of

## Changelog

- 0.6.0 (2026-10-28): Step 3 and the template describe moving the Ingest section to `wiki/AGENTS.md` and the Capsules and Extra checks sections to `_system/AGENTS.md` (each with a `@AGENTS.md` CLAUDE.md beside it) once the root rules file passes about 150 lines; ingest 1.2.0, capsule 4.1.0 and health-check 0.6.0 read them. New brains still start with one root file. No eval run.
- 0.5.1 (2026-10-27): Refreshed the vendored `check_brain.py` from health-check 0.5.2 (robustness and false-positive fixes). No change to setup's steps.
- 0.5.0 (2026-10-26): Extracted the existing 0.5.0 setup procedure under the setup identity. using-scarecrow owns framework routing; health-check retains canonical check-script ownership. Setup reads local rules before applying package defaults.
- 0.5.0 (2026-10-25): Added project hub headers with `status`, `last-updated`, `decision`, `feedback`, and `log`, including the optional prompt and skill status set. Rules and page templates add paused-project notes, the Archive test, runbook conventions, Extra checks, and the line-by-line prune test. Adopt mode adds headers and lists clashing state fields without renaming them. Refreshed the vendored `check_brain.py` from health-check 0.5.0 for M9 header checks and M22 status-file freshness. No eval run yet.
- 0.4.1 (2026-10-17): Vendored `check_brain.py` refreshed from health-check 0.3.0 (new M21 secret-shape check; `.smart-env` skipped). No change to scarecrow's own steps.
- 0.4.0 (2026-10-12): Decision-reason-date convention. The AGENTS.md template's Conventions section now asks that every settled rule or decision carry its reason and the date it was decided, `<rule> (<reason>; decided YYYY-MM-DD)`, so a fresh session reads the line and moves on instead of reopening it; rules written at setup carry the setup date and the reason the owner gave in the interview. The build step points at it. Health-check 0.2.0 J8 lists rules that lack both. The dated-line practice is unmeasured; Naur's 1985 Programming as Theory Building supports the framing only.
- 0.3.1 (2026-10-12): Reference files over 100 lines now open with an inline Contents line listing their sections (release checklist item 14, from Anthropic's skill authoring best practices): `references/page-templates.md`. No behavior change.

- 0.3.0 (2026-10-08): `check_brain.py` is now a copy of the health-check skill's canonical script, enforced by `tests/test_vendored_script.py`. The verify step runs `--structure`, which keeps the build check to structure; the full run adds upkeep checks for health-check. The rules-length warning moved from 200 to 150 lines, matching the template's target.
- 0.2.0 (2026-10-08): Added a root `open-questions.md` for unknown facts (separate from a project's to-do open items) and a read-only `received/` folder per project for client or stakeholder documents, with `deliverables/` beside it; the check script now records and verifies `received/` files alongside `raw/`. Both ideas came from the no-skill baseline runs in iteration 1.
- 0.1.0 (2026-10-08): Pilot. Build-new and adopt-existing modes, four-part layout, AGENTS.md with CLAUDE.md pointer, bundled `check_brain.py`. Iteration-1 evals: 30/30 with skill vs 15/30 without (three cases).
