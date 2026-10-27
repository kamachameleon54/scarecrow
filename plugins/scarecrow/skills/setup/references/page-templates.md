# Page and file templates

Contents: Wiki page (`wiki/<kebab-name>.md`) · Index (`wiki/index.md`) · Log (`wiki/log.md`) · Project hub (`projects/<name>/_index.md`) · Project status (`projects/<name>/status.md`) · Open questions (`open-questions.md`, at the root) · Received folder (`projects/<name>/received/README.md`) · Corrections register (`_system/corrections.md`) · Change log (`_system/changelog.md`) · raw/README.md

## Wiki page (`wiki/<kebab-name>.md`)

```markdown
---
type: concept            # or: entity, summary, comparison, how-to, decision
title: <Title>
sources:
  - raw/<source-file>.md
verified: YYYY-MM-DD     # or "pending" if the owner has not confirmed the takeaways
---

# <Title>

<Two to four sentence summary of what this page knows.>

## Key points
- <takeaway, traceable to a source>

## Open questions
- <what the sources do not settle>

## Related
- [<other page>](other-page.md)
```

`type` is the one field the Open Knowledge Format (Google, v0.2) requires for conformance; `verified` mirrors its freshness fields. Keeping both makes the brain easy to check now and easy to share later.

## Index (`wiki/index.md`)

```markdown
# Index

## <Category>
- [<Page title>](<page>.md) - <one-line summary>
```

One line per page. The agent reads this first, so the summaries should say what question each page answers.

## Log (`wiki/log.md`)

```markdown
# Log

## [YYYY-MM-DD] ingest | <source title>
Pages touched: <page>.md, <page>.md. Owner confirmed takeaways: yes | pending.

## [YYYY-MM-DD] health-check | <scope>
Findings: <short list>. Next check: YYYY-MM-DD.
```

Append only. The fixed prefix makes the log searchable with `grep "^## \["`.

## Project hub (`projects/<name>/_index.md`)

```markdown
---
status: active            # active | paused | done | reference
last-updated: YYYY-MM-DD  # the date this header was last confirmed true
decision: "YYYY-MM-DD: <latest decision, one line>"
feedback: "<open feedback or questions waiting on someone, with a count>"   # or: none
log: "status.md"          # where the full record lives
---

# <Project name>

<One sentence: what this project is and who it is for.>

- [status.md](status.md) - current state, decisions, open items
- received/ - what they sent (read-only)
- deliverables/ - what we produced
- <file> - <one line>
```

The header is the one-glance answer to "where does this stand?", so a session (or the owner, in a notes app that shows frontmatter as properties) reads it before opening anything else. It summarizes; it never replaces the record. `decision` holds only the latest decision, because the history already lives in `status.md`. `feedback` uses `none` when nothing is open, so an empty field always means it was never filled. `last-updated` changes when someone confirms the header still matches `status.md`, which is why the check script compares the two dates.

Use one field name, `status`, with one value set per kind of hub. Project, event, and reference hubs use `active | paused | done | reference`. A brain that also keeps reusable prompts or skills can give their hubs `draft | testing | stable | deprecated`: maturity and activity are different questions, since a stable prompt can sit idle and an active project can hold nothing stable. A reference hub (a folder of background material, not a project) may leave `decision` and `feedback` as `none`.

A paused hub adds a section at the end:

```markdown
## Parked

Stopped YYYY-MM-DD because <reason>. Restarts when <condition>. Decided by <owner>.
```

## Project status (`projects/<name>/status.md`)

```markdown
# <Project name>: status

Last updated: YYYY-MM-DD

## Current state
<Two or three sentences.>

## Decisions
- YYYY-MM-DD: <decision and who made it>

## Open items
- [ ] <item> (owner, due date if any)
```

## Open questions (`open-questions.md`, at the root)

```markdown
# Open questions

Facts this brain does not know yet. Answer one by moving it into the page or status file where it belongs, with its source.

| Added | Project | Question | Why it matters | Who might know |
|---|---|---|---|---|
| YYYY-MM-DD | <project or "general"> | <question> | <what it blocks or changes> | <person or document> |
```

Open questions are unknown facts; a project's `status.md` open items are to-dos. Keep them apart so neither list hides the other.

## Received folder (`projects/<name>/received/README.md`)

```markdown
# received

Files <client or stakeholder> sent, exactly as sent. Never edited. Our own work goes in ../deliverables/.
```

## Corrections register (`_system/corrections.md`)

```markdown
# Corrections

Known-wrong facts that may appear in sources or older notes. Check drafts against this list before they leave the folder.

| Added | Wrong | Correct | Source of the correction |
|---|---|---|---|
| YYYY-MM-DD | <wrong statement> | <correct statement> | <where the right answer came from> |
```

## Change log (`_system/changelog.md`)

```markdown
# Change log

## YYYY-MM-DD
- <structural change and why>
```

## raw/README.md

```markdown
# raw

Sources land here exactly as received and are never edited. If a source turns out to be wrong, record the fix in `_system/corrections.md`. `.manifest.json` records a checksum for each source so a later edit can be caught.
```
