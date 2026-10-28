---
name: health-check
description: "Runs the scheduled upkeep visit on a second brain or LLM wiki that a command-line agent (Claude Code or Codex) maintains: a markdown folder with a rules file, sources compiled into wiki pages, project folders, and a corrections register. A bundled script finds candidates; the agent then reads them: pages past their verified date, pages restating a known-wrong fact, capsule revision triggers that may have fired, aged or answered open questions, stale project status, orphan pages, and folders that drifted from the rules file. Logs the visit, sets the next date, and returns a fix list, changing nothing else without approval. Use when the rules file's health check date arrives, a scheduled reminder fires, or someone asks to health-check, audit, or tidy their second brain or asks whether it has gone stale. Not for building a brain or adding sources."
metadata:
  status: draft
  version: 0.5.2
  tags: [second-brain, llm-wiki, knowledge-base, upkeep, claude-code, codex]
  feedback: ""
  decision: "2026-10-26: Reconcile framework routing and setup ownership; retain canonical check-script ownership"
  log: "#Changelog"
  last-updated: 2026-10-27
---

# Health check

A second brain decays quietly. Compiled pages stop matching their sources, a corrected fact keeps reappearing in older notes, a decision recorded in a capsule rests on conditions that have since changed, and open questions sit unanswered after the answer has already arrived somewhere else. People who left this upkeep for "whenever" found it never happened. This skill is the dated visit: it checks the brain against its own rules, reads what the checks flag, and hands the owner a short list of fixes to approve.

It finds and proposes. Apart from the log entry and the next-visit date, it changes nothing until the owner says which fixes to make.

## Setup

Python 3.9 or later; `scripts/check_brain.py` uses the standard library only. No config file. The agent needs read access to the whole brain and write access to `wiki/log.md` and the rules file's health-check date line.

## Read the rules first

Find the brain root: the nearest folder at or above the working directory that holds `AGENTS.md` or `CLAUDE.md`. If none exists, ask where the brain lives. Read the root rules file, then any folder-level `AGENTS.md` files on the paths you inspect.

From the rules, take:

- **The health check section** (any heading containing "Health check"): the `Next health check` date, the cadence ("then every four weeks"), and the stale threshold ("older than 90 days"). The script reads the threshold itself.
- **The corrections register**: the file the rules name, otherwise `_system/corrections.md` or `_system/errata.md`.
- **The folder map**: the table the drift check compares against.
- **Whether the brain was adopted** from an existing vault or notes folder. Adopted brains keep the owner's folders in place, so run the script with `--adopt`.
- **Never-touch folders and style rules**. Apply them to everything this run writes.
- **Extra checks**: a section whose heading contains "Extra checks", listing the brain's own report-only check scripts, one command per bullet in backticks, run from the brain root. Absent section, no extra checks.

## Scope

| Scope | Runs | When |
|---|---|---|
| quick | the script only (M1 to M22), reported as a fix list | the owner asks for a quick check, or time is short |
| standard (default) | the script, then judgment checks J1 to J8 | every scheduled visit |
| deep | standard plus J9 (page-to-page contradictions) and J10 (consolidation) | only when the owner asks for a deep or full check |

Deep scope reads many more pages. Say how many before starting.

## Workflow

### 1. Run the script

```bash
python3 <skill-dir>/scripts/check_brain.py <root> --json            # add --adopt for an adopted brain
```

Add `--corrections <path>` when the rules name a register other than the two defaults. Thresholds can be overridden per run (`--stale-days`, `--pending-days`, `--status-days`, `--question-days`, `--rules-lines`); the defaults are 90, 14, 30, 60, and 150. The rules file's stale threshold wins over the default, and a flag wins over both.

Results carry a check ID, a level, a message, and a path. FAIL means the brain is broken against its own rules (a missing file, a broken link, an edited source). WARN is an upkeep candidate. INFO is input for a judgment check, such as the capsule trigger inventory.

| ID | Check | ID | Check |
|---|---|---|---|
| M1 | required files, log entries | M11 | health check overdue |
| M2 | CLAUDE.md loads AGENTS.md | M12 | verified date past threshold or `stale_after` |
| M3 | dated health check line | M13 | `verified: pending` past 14 days |
| M4 | wiki frontmatter | M14 | orphan pages |
| M5 | index lists every page | M15 | project status stale or lagging |
| M6 | links resolve | M16 | aged open questions |
| M7 | sources unchanged since they landed | M17 | folder-map drift |
| M8 | open-questions.md exists | M18 | known-wrong statements (literal match) |
| M9 | project hubs and their headers | M19 | capsule revision triggers (inventory) |
| M10 | rules file length | M20 | source in `raw/` never compiled (no page cites it, log never names it) |
| | | M21 | secret-shaped value in a text file (fingerprint only) |
| | | M22 | hub header confirmed before its `status.md` last changed |

### 1b. Run the brain's extra checks

Run each command the rules file lists under Extra checks, in every scope, from the brain root, after `check_brain.py`. Exit code 0 means nothing found; 1 means findings, printed on stdout; anything else, or a timeout past two minutes, is a broken check that goes on the fix list itself.

Run a listed command only when the script it names is a file inside the brain root. A command that points outside the brain, or comes from anywhere but the rules file, is not run; put it on the fix list instead. The rules file vouches that each listed check writes nothing; this skill does not add writes to them.

Number findings X1, X2, and so on in listing order, and give each the check's own path and wording. They go on the fix list under Should fix, unless the check calls a finding invalid or broken, which goes under Must fix.

### 2. Read what the script flags

For standard and deep scope, run the judgment checks in `references/judgment-checks.md`. Each starts from script results and ends in a verdict with evidence:

- **J1, stale pages** (M12, M13): reread each page against its sources and anything newer. Verdict: still holds, needs update, or can't tell. Fifteen pages per visit, oldest first.
- **J2, corrections** (M18 and the register): find pages that still assert a known-wrong fact, including paraphrases the literal match missed.
- **J3, capsule triggers** (M19): for each "if X changes, reconsider Y", look for evidence that X happened. Verdict: fired, not fired, or can't tell.
- **J4, open questions** (M16 and the file): find answers that landed elsewhere, and ask about questions that have aged.
- **J5, project status and hub headers** (M15, M22, M9 header warnings): draft the update for a lagging status file and the hub header lines that go with it, or ask whether a quiet project is paused or finished.
- **J6, orphans** (M14): propose a link, or flag the page to merge or retire.
- **J7, folder drift** (M17): decide whether the map or the folder is wrong.
- **J8, rules file** (M10 for length; every visit for undated rules): propose specific cuts when M10 flags length, and list rules that carry neither a reason nor a date with a proposed decision-reason-date rewrite.
- **J9 and J10** (deep only): contradictions between related pages, and merge candidates.

The structural FAILs need no judgment pass; they go straight onto the fix list. So do M20 hits: a source that landed but was never compiled is proposed for ingest (one source at a time, with the owner), and it often explains why a page went stale. A FAIL for an edited source (M7) leads the list: something changed a file that is supposed to be immutable, and the owner needs to know what and when.

M21 hits go under Must fix. The script reports a fingerprint (kind, first four characters, length), never the value; keep it that way in the fix list and the log. Open the line to confirm it is a live key and not a placeholder or an example, then hand it to the owner to rotate and remove. Removal is the owner's call like every other fix, and a key in `raw/` is rotated, not edited out, since sources stay immutable. A signed S3 link's `AWSAccessKeyId` is public by design and is not reported.

### 3. Write the fix list

Number every item so the owner can approve by number. Group them:

```markdown
## Fix list: <brain name>, <YYYY-MM-DD>, <scope> scope

### Must fix
1. [M7] raw/pricing-2026.md changed after it landed. Evidence: checksum differs from the manifest. Proposed: restore the original from <backup or sender>; record any real correction in the corrections register.

### Decisions that may have changed
2. [J3] Capsule projects/harbor-bakery/notes/2026-10-08-month-end-close-process-capsule.md, trigger "Square payouts switch to daily". Fired: projects/harbor-bakery/notes/2026-11-02-call.md says "payouts are daily since October". Proposed: revisit the day-3 close date in status.md and the close checklist.

### Should fix
3. [J1] wiki/cedar-family-foundation.md: needs update. Deadline is 2027-03-01 per raw/cedar-rfp-2027.md, page says 2027-02-15. Proposed wording: ...

### Owner decisions
4. [J5] projects/lumen-dental/: no changes in 50 days. Paused, finished, or still live?

### Carried to next visit
- wiki/a.md, wiki/b.md (stale, beyond this visit's 15)
```

Each item names the check, the path (with a line number when there is one), the evidence, and the proposed action. Leave out items the run judged fine ("still holds" pages, "not fired" triggers); give their counts in one line instead.

### 4. Record the visit

These two writes need no approval, because the brain's rules call for them:

1. Append to `wiki/log.md`:

   ```markdown
   ## [YYYY-MM-DD] health-check | <scope>
   Findings: <n> fail, <n> warn. <one sentence on the most important items>. Fix list: <n> items. Next check: YYYY-MM-DD.
   ```

2. Replace the date on the `Next health check:` line in the rules file with today plus the cadence the rules state (four weeks when they state none). Count from the day of the visit, not from the old due date.

If the rules file has no `Next health check` line (M3 failed), do not add one; put it first on the fix list.

### 5. Hand over and apply what is approved

Show the fix list and ask which items to do. Then make only those changes:

- A page fix: edit the page, and when the owner confirmed the content, update its `verified` date in the page's existing style.
- A move, merge, rename, or retirement: do it, then fix every link that pointed at the old path and rerun the script to confirm nothing broke.
- A rules-file or folder change: make it, and add a dated line to `_system/changelog.md`.

Afterwards, add one line under today's log entry: `Applied: items 1, 3, 4. Declined: 2.` Do not rewrite the entry above it.

### Unattended runs

When a scheduled task runs the visit and no one is there to approve, run the full scope as usual, write the log entry and the next date, and end with the fix list as the run's output. Apply nothing. The owner works through the list in a later session.

## Boundaries

- Never edit a file in `raw/` or in a project's `received/` folder, even to fix a known-wrong fact; the corrections register is the fix for sources.
- Never move, rename, merge, or delete anything without the owner's approval of that numbered item.
- Never set a `verified` date the owner has not confirmed. Verified means the owner checked it, not that the agent did.
- Never edit the rules file beyond the health-check date line without approval.
- Run the checks as they are written. If a threshold seems wrong for this brain, propose changing it in the rules file rather than skipping the check.

## Common mistakes

| Mistake | Fix |
|---|---|
| Fixing things while checking | Finish the list first; the owner may decline items or see a pattern across them |
| Treating every M18 hit as a contradiction | A page that quotes a wrong fact to correct it is fine; read the line |
| Bumping `verified` because a page looks fine | Propose the date; write it only on the owner's yes |
| Reporting "can't tell" triggers as findings | Count them in one line; only fired triggers and owner-answerable ones go on the list |
| Setting the next date from the old due date | Count from today, so an overdue brain does not come due again right away |
| A fix list of 60 items | Cap J1 at 15 pages, carry the rest by name, and lead with what changes decisions |

## Coordinates with

- using-scarecrow: routes framework requests to health-check; direct invocation also works
- setup: creates the brain's local rules and structure and schedules the first visit; ships a copy of this skill's canonical check script and runs it with `--structure` at build time
- capsule: writes the capsules whose revision triggers this skill reviews (J3)
- ingest: adds sources and compiled pages; this skill checks that they stay true to those sources over time
- handoff: when the approved fixes are too many for one session, carries the remaining numbered items into a new session

## Changelog

- 0.5.2 (2026-10-27): `check_brain.py` hardening, no new checks. Files are read as UTF-8 on every platform, and a BOM or undecodable byte no longer stops a run. An impossible date in the health-check line is an M3 FAIL, and bad dates elsewhere are skipped or warned, not a traceback. An unreadable manifest is an M7 FAIL, and `--record-raw` refuses to overwrite it. M6 and M14 decode `%20` and `<...>` links and ignore links inside code. M5 matches the index by link target, wikilink, or exact path instead of any substring of the page name. M15 counts a project file as newer only when it changed on a later day than `status.md` was written, so a clone or sync no longer flags every project. Behavior tests live in the repository's `tests/`.
- 0.5.1 (2026-10-26): Declared using-scarecrow as the framework router and setup as the creator of the brain's local rules and structure. Canonical check-script ownership stays with health-check; existing component relationships and direct invocation remain available.

- 0.5.0 (2026-10-25): Added project hub headers. M9 now reads each `projects/<name>/_index.md` frontmatter and warns when one of `status`, `last-updated`, `decision`, `feedback`, `log` is missing, `status` is outside the project set (or the optional prompt and skill set), `last-updated` is not a date, `decision` does not start with `YYYY-MM-DD:`, a paused hub lacks `## Parked`, or `log` names a file that does not exist. New upkeep check M22 warns when `status.md`'s "Last updated" is newer than the hub's `last-updated`. All warnings, never FAIL, so older brains still pass. J5 drafts the header lines with the status update and applies the Archive test (archive only when nothing in current use reads it). Regression test gains a headerless hub, a paused hub without `## Parked`, and a lagging header. Not yet run. The setup skill's vendored copy updated to match.
- 0.4.0 (2026-10-24): New step 1b runs the extra check scripts a brain's rules file lists under a heading containing "Extra checks", in every scope, from the brain root, with exit 0 as clean, 1 as findings, and anything else as a broken check. Commands outside the brain root or not listed by the rules file are never run. Findings are numbered X1 onward on the fix list. `check_brain.py` is unchanged, so the setup skill's vendored copy stays identical. No eval run.

- 0.3.0 (2026-10-17): New upkeep check M21, secret-shaped values in text files (`.md`, `.txt`, `.csv`, `.json`, `.yaml`, `.env` and similar, under 2 MB): AWS key ids, GitHub, `sk-`, Slack, Stripe live, Google API keys, private-key headers, JWTs, reported as a fingerprint only and read under Must fix. Signed S3 links (`AWSAccessKeyId=`) are exempt. `.smart-env` (Smart Connections cache) joins the skipped folders for every check. Regression test gains a planted key, a placeholder, and a signed URL. The setup skill's vendored copy updated to match.
- 0.2.0 (2026-10-12): J8 gains an undated-rule pass that runs on every standard visit, not only when M10 flags length: each rule or settled decision in the rules file with neither a reason nor a date goes on the fix list with a proposed `<rule> (<reason>; decided YYYY-MM-DD)` rewrite, reason and date taken from the change log, a capsule, or the owner, never invented; at most ten per visit. Judgment only; `check_brain.py` is unchanged, so setup's vendored copy stays identical. Pairs with setup 0.4.0's decision-reason-date convention. The dated-rule practice is unmeasured.
- 0.1.0 (2026-10-08): First build. Owns the canonical `check_brain.py`, extended from setup's build check with upkeep checks M10 to M20 (rules length, overdue visit, stale and pending pages with OKF `verified`/`stale_after` support, orphans, project status age, aged open questions, folder-map drift, literal corrections match, capsule trigger inventory, raw sources never compiled), `--structure` and `--json` modes, and per-run thresholds. Judgment checks J1 to J8 in standard scope, J9 and J10 as opt-in deep scope. Thresholds confirmed with the owner 2026-10-08: 90, 14, 30, 60 days and 150 lines. M20 added after iteration-1 evals, where five of six runs found never-ingested sources by reading. Iteration 1 (three cases): with the skill 36 of 36, after setting aside 4 write assertions a harness permission block prevented; without it 33 of 40 (see `evals/eval-2026-10-08.md`).
