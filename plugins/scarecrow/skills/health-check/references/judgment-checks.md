# Judgment checks

The script finds candidates; these checks decide what the candidates mean. Each check starts from script results (by check ID), reads the files named there, and ends in a verdict plus a proposed action for the fix list. Every proposal cites the evidence it rests on: a path, and a line or a short quote. A verdict with no evidence is a guess; write "can't tell" instead and say what would settle it.

Nothing in this file authorizes a change. Every proposed action waits for the owner's approval.

## Standard scope

### J1. Stale pages (from M12 and M13)

For each page past its verified date or long pending, oldest first, up to 15 per visit:

1. Read the page and every file in its `sources`.
2. Check each key point against the sources, then against anything newer in the brain on the same subject: later sources in `raw/`, project notes, `status.md` decisions, the corrections register.
3. Verdict:
   - **still holds**: every key point traces to a source and nothing newer contradicts it. Propose a new verified date.
   - **needs update**: a point is contradicted by newer material or by the corrections register. Name the point, the newer file, and the proposed wording.
   - **can't tell**: the sources do not settle it and nothing newer speaks to it. Propose asking the owner; if the owner does not know either, propose an open-questions row.

For a `verified: pending` page the question is different: the owner never confirmed the takeaways. List the page's key points so the owner can confirm them in one reply.

Pages beyond the 15 go on the fix list as "carried to next visit", by name.

`verified` records the owner's confirmation. The agent proposes a date; it writes one only after the owner says yes. Keep the page's existing style: a plain `verified: YYYY-MM-DD` stays a date, and an OKF-style list gets a new `{ by: human:<owner>, at: <now> }` entry.

### J2. Corrections contradictions (corrections register, M18 hits)

For each row in the corrections register:

1. Start from the M18 hits, which are literal matches only.
2. Then read the pages most likely to restate the wrong fact in other words: pages whose title, sources, or index line share the row's subject, and project notes that cite those pages.
3. A hit counts when the page asserts the wrong statement as true. A page that quotes it in order to correct it, or a capsule that explains how the correction was found, does not count.

Proposed action: the corrected sentence for the page, with the correction row's source. Never propose editing a file in `raw/` or a `received/` folder; the register already covers those.

### J3. Capsule revision triggers (M19 inventory)

For each trigger in each capsule ("If X changes, reconsider Y"):

1. Identify the condition X.
2. Search the brain for evidence about X dated after the capsule was written: project notes, `status.md`, the log, newer sources, the corrections register, open questions.
3. Verdict:
   - **fired**: evidence shows X happened. Quote it with its path. Propose reconsidering Y and name the files that depend on Y.
   - **not fired**: evidence shows X still holds as it did.
   - **can't tell**: nothing speaks to X. This is the usual verdict and needs no action, unless the trigger is about something the owner would know offhand; then list it as a question for the owner.

Report fired triggers near the top of the fix list. They are the clearest sign that a past decision now rests on changed ground.

### J4. Open questions (open-questions.md, M16)

For every row, not only aged ones:

- Search for an answer that has landed since the row was added: a newer source, a project note, a status decision. If found, propose moving the answer into the page or status file where it belongs, citing where it came from, and deleting the row.
- For rows older than the threshold with no answer, ask the owner whether the question still matters. Propose keeping it, or retiring it with a one-line reason.

### J5. Stale project status and hub headers (M15, M22, M9 header warnings)

- **Status lagging**: files in the project changed after "Last updated". Read them and draft the status update (current state, new decisions, open items) for the owner to approve.
- **Project dormant**: nothing changed since "Last updated". Ask whether the project is paused, finished, or still live. A paused project's hub gets `status: paused` and a `## Parked` section (why it stopped, what restarts it). A finished project gets `status: done` and becomes an archive candidate only when nothing in current use reads it; propose the move, never make it without approval.
- **Header behind its record** (M22): `status.md` changed after the hub's `last-updated`. Read the status file and draft the new `decision` and `feedback` lines (latest decision only, dated; open feedback with a count, or `none`), plus today's `last-updated`, for the owner to approve. Draft the header and the status update together so they agree.
- **Header missing or invalid** (M9 WARN): propose the five fields, drawn from `status.md`, never invented. A field with no source waits for the owner.

### J6. Orphan pages (M14)

Read each orphan and its likely neighbors (pages that share a source, the project that cites its sources). Propose either one or two specific links (from which page, at which sentence) or, if nothing should point to it, flag it as a candidate to merge or retire. A merge or retirement is an owner decision.

### J7. Folder drift (M17)

For each mismatch, decide which side is wrong:

- A folder that exists but is not in the map: propose a map row with one line on what it holds. If it looks like misfiled material, propose a move instead.
- A map row with no folder: propose removing the row, or creating the folder if the rules still call for it.

Both are rules-file or structure changes. Note them in `_system/changelog.md` after the owner approves and the change is made.

### J8. Rules file: length (M10) and undated rules (every visit)

When M10 flags the length, read the rules file and propose specific cuts: sections that repeat what the folder already shows, worked examples that could move to a reference file the rules point to, and rules that no longer apply. Give the line count after the cuts. The owner decides.

On every standard visit, whether or not M10 fired, read each line of the rules file that states a rule or a settled decision. A rule that carries neither a reason nor a date is the one a fresh session reopens, so it goes on the fix list with a proposed rewrite in the form `<rule> (<reason>; decided YYYY-MM-DD)`. Take the reason and date from `_system/changelog.md`, a capsule, or the log; where none of them settles it, ask the owner and write "reason unknown" in the proposal. Never invent a reason or a date. Folder-map rows, section headings, and procedure steps are not rules. List at most ten per visit, starting with rules the log shows were questioned or re-decided.

## Deep scope (opt-in only)

Run these only when the owner asks for a deep check. They read many more pages, so state the page count before starting.

### J9. Page-to-page contradictions

Compare pairs of wiki pages that share a source or link to each other. Flag a pair when they state incompatible facts (different numbers, dates, owners, or rules for the same thing). For each, say which page the sources support and propose the fix to the other. Cap at 40 pairs per visit, prioritizing pairs where either page was updated since the last visit.

### J10. Consolidation

Look for pages with overlapping titles, mostly shared sources, or index lines that answer the same question. Propose merges (which page survives, what moves into it, which links need repointing). A merge is always an owner decision; never carry one out unasked.
