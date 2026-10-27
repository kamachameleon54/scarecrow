---
name: capsule
description: "Writes a capsule: a markdown document filed inside the user's knowledge base (an Obsidian vault, a second-brain folder, any markdown notes folder with a rules file) that preserves the reasoning, dead ends, constraints, and revision triggers behind a finished piece of work, so the chats or sessions that produced it can be cleared without losing what was learned. Covers built artifacts, research, project chapters, negotiations, debugging arcs, and meeting debriefs. Use when the user says \"capsule this\", \"make a capsule\", \"time capsule this\", \"distill this thread\", \"compact this before I delete it\", \"preserve what we learned\", or \"save the reasoning here\", or wants to clear chat clutter while keeping the lessons. Not for summaries, status updates, or task capture (\"log\", \"save\", \"capture\", \"track\" as the verb), and not for continuing unfinished work in a new session, which is handoff."
metadata:
  version: 4.0.2
  status: testing
  tags: [capsule, archival, knowledge-base, second-brain]
  feedback: ""
  decision: "2026-10-26: Reconcile framework routing and setup ownership while retaining direct capsule invocation"
  log: "#Changelog"
  last-updated: 2026-10-26
---

# Capsule

Produce one durable document that captures the reasoning behind a finished body of work, filed where that work's context lives, so the conversations that produced it can be deleted without loss.

## Setup

Stdlib only; no scripts and no config file. The skill needs read and write access to a markdown knowledge base. Everything specific to a particular knowledge base (where capsules go, which corrections file to check, link style, writing style) comes from that knowledge base's rules file, described under "Read the rules first".

## Why this skill exists

When a piece of work finishes, the threads that produced it become baggage. Deleting them clears the baggage, but only if the lessons survive somewhere first. The finished output (a skill, a report, a deck, a decision) encodes conclusions. The capsule encodes what the output cannot: the reasoning that produced it, the dead ends not worth re-walking, the constraints that shaped the design, and the conditions under which the conclusions should be revisited. Its reader is a future session or person who has the output but not the conversations.

## Scope

Any conversation that produced reasoning the final output does not already encode:

- Building a skill, prompt, script, or other artifact
- A research effort or an idea pressure-tested against evidence
- A long debugging arc where the cause was finally found
- A partnership, vendor, or client negotiation working through tradeoffs
- A meeting debrief where the value is reasoning, not action items
- A decision about how to organize the knowledge base itself

## When to run

Only when the user asks for a capsule or describes wanting to preserve learnings before clearing conversations. Capsuling is deliberate, not a passive summary.

If the work is still changing, say so: a capsule written on a moving target is wrong within a day. Suggest coming back when it settles. If the user still wants it, proceed and flag the risk once in the output.

## Read the rules first

Find the knowledge base root: the nearest folder at or above the working directory that holds `AGENTS.md` or `CLAUDE.md`. If none exists, ask where the knowledge base lives. Read the root rules file, then any folder-level `AGENTS.md` files along the path to the destination, broadest to most specific.

Look in the rules for a section about capsules (any heading containing "Capsule"). When it exists, it wins over the defaults below. It may set:

- **Routing**: where each capsule type goes
- **Corrections register**: the file of known-wrong facts to check
- **Pattern pages**: where generalizable lessons accumulate
- **Skill backlog**: where skill candidates are listed
- **Link style**: Obsidian double-bracket links or relative markdown links
- **Style**: writing rules for the owner's documents

When the rules are silent on a point, use the default for that point. When the default needs a folder the knowledge base does not have, skip that step and say so in the summary rather than inventing structure.

## Routing: co-locate with the context

A capsule lives where it will be found the next time the same context is touched, so its reasoning resurfaces beside the work instead of sitting in a folder nobody opens. Default routing when the rules give none:

| Capsule type | Default destination |
|---|---|
| `project`, `partnership` | the project's own folder (in a scarecrow-style brain, `projects/<name>/`) |
| `skill`, `prompt` | inside the artifact's own folder, next to its main file |
| `research`, `debugging` | the folder of the work it served; debugging capsules use the `-debug-capsule` suffix |
| `meeting` | the project or organization folder the meeting belongs to; filename `<YYYY-MM-DD>-<topic>-capsule.md` |
| `method` | a portable technique extracted from project work: the folder the rules name for methods; if none, ask |
| no clear home | ask; never create a dump folder |

Rules that hold everywhere:

- Never write a capsule into a sources folder that the rules mark immutable (often `raw/`) or into a project's `received/` folder. Capsules are not sources.
- Every capsule filename ends in `-capsule.md`, wherever it lands, so capsules can be found as a group by a filename search.
- Create a missing project subfolder if the project clearly exists. Never create a new top-level folder.

### Paired capsules

If a conversation spans several types, pick the dominant one and link the other in Connections. One split is supported by design: when a conversation produced both a project-specific record and a portable method worth reusing, write both. Each half routes on its own and links the other. Patterns are appended once per half, never duplicated. Do not split one body of reasoning into two capsules just because it is long.

## What every capsule contains

- **The job.** One or two sentences on what the work was and what done looks like.
- **Build context.** Model, tools, platform constraints, and the state of the world at capsule time.
- **What worked and why.** Decisions that survived into the final output, with reasoning.
- **What did not work and why.** Abandoned approaches and why, so nobody re-walks them.
- **Known edge cases.** Things that came up and stayed unresolved.
- **Revision triggers.** "If X changes, reconsider Y."
- **Patterns discovered.** Lessons that generalize beyond this work.
- **Connections.** Links to related notes in the knowledge base.

### Conditional sections

**Source snapshot (artifact capsules only).** When the work produced a buildable artifact (a skill with references, a prompt with variants, a script project), preserve the source at the exact version the capsule documents, or the reasoning eventually disconnects from the code it describes. Write every text source file into a folder named `<capsule-name>-files/` (beside the capsule unless the rules name a snapshot location; never inside a folder that gets packaged or published, where it would ship a second copy of the artifact), flattened one level (`references/notes.md` becomes `<capsule-name>-files/notes.md`). Then rebuild the original directory structure in a temporary folder, zip it as `<artifact>_v<version>_capsule.zip`, and hand it over however the surface allows (a download where possible, otherwise report the path).

**Inputs and sources consulted (non-artifact capsules).** Replace the snapshot with a record of what was consulted (transcripts, web pages, documents in the knowledge base, connector queries, people) with enough detail to find each again: paths, URLs, dates and titles, tool names with what was queried.

## Pattern aggregation

If the rules name pattern pages, append the capsule's Patterns discovered there. If they do not but the knowledge base has a `wiki/` folder, default to `wiki/build-patterns.md` (skill, prompt, method), `wiki/research-patterns.md` (research), `wiki/decision-patterns.md` (project, partnership, meeting), and `wiki/debug-patterns.md` (debugging). With neither, keep the patterns in the capsule only.

Entry format (match existing entries if the page already has a different shape):

```markdown
### From <link to the capsule> (<YYYY-MM-DD>)

- **<Pattern title stated as a sentence.>** <one-paragraph description>
```

The bold title ends with a period inside the bold, and the prose follows with no separator. If a pattern page does not exist, create it using the knowledge base's local wiki frontmatter contract, followed by a one-line preamble on what it collects, and add it to the wiki index if there is one. When local rules are silent, use this default frontmatter and preamble (shown for the build-patterns page; set a specific title and preamble matching the selected page):

```markdown
---
type: pattern
title: Build patterns
sources: []
verified: pending
---

Generalizable lessons from finished artifact builds.
```

Capsules are records of finished work, not raw sources. Keep `sources: []` in the default pattern page; link the capsules in the pattern entries rather than listing them as raw sources.

## Skill candidates

When the work is extractable as a future skill, add `skill-candidate` to the capsule's tags. If the rules name a skill backlog, add a one-line entry there linking the capsule; a tag alone sits unfound until someone searches for it. If the rules route skill-candidate method capsules to a future skill folder, follow that.

## Output format

Markdown with YAML frontmatter. Adapt by type:

```
---
title: <topic> capsule
type: capsule
capsule-type: skill | prompt | project | research | meeting | partnership | debugging | method | general
created: <YYYY-MM-DD>
status: archived
artifact-version: <if applicable>
source-chats:
  - title: "<chat title>"
    url: "<chat URL>"
model-version: <model used during the work>
snapshot-path: <relative path to the -files folder, if applicable>
sources-consulted: <yes | no>
tags:
  - capsule
  - <domain tags>
---

# <topic> capsule

## The job
## Build context
## What worked and why
## What did not work and why
## Known edge cases
## Revision triggers
## Patterns discovered
## Connections
## <Source snapshot | Inputs and sources consulted>
```

Write "None identified at capsule time." under Known edge cases or Revision triggers when there are none. Omit Patterns discovered entirely if none surfaced. In Connections, link only notes you have confirmed exist; invented links pollute the knowledge base.

Surfaces without a chat URL (Claude Code, Codex, Cowork) use this instead of `source-chats`, never both, and never a placeholder URL:

```
source-session:
  surface: <claude-code | codex | cowork>
  date: <YYYY-MM-DD>
  description: "<one-line description of the session>"
```

## What to leave out

No transcripts, quoted exchanges, timestamps beyond the frontmatter, or notes on how the capsule was assembled. Do not duplicate what other systems carry: if the artifact is published with its own install notes, or the project's next actions live in a task system, the capsule covers only the reasoning those systems never see.

## Length

About one page of body. If it runs longer, the content is probably already encoded in the final output; cut to what the output cannot say on its own. Revision triggers and patterns may extend it modestly when they carry real insight.

## Style

Follow the style rules in the knowledge base's rules file. When it has none: prose over bullets except where a list is functional (revision triggers, file lists), active voice, direct sentences, no emoji.

## Execution order

1. Find the knowledge base root and read the rules, including any capsules section and folder-level rules on the path to the destination.
2. Read the corrections register (the one the rules name, or `_system/corrections.md` or `_system/errata.md` if present) and apply any active corrections silently in everything the run writes and says.
3. Determine the capsule type from context. Ask once only if it is ambiguous.
4. Route to the destination. Create a missing project subfolder if needed.
5. Write the capsule with the surface's file-write tool.
6. If the destination folder has an index hub (`_index.md` or similar), add a one-line entry for the capsule. Never create a hub that does not exist.
7. Artifact capsules: write the source snapshot folder and hand over the zip.
8. Append patterns per "Pattern aggregation".
9. Skill candidates: tag, and add the backlog line if the rules name a backlog.
10. Summarize for the user: the capsule's path; the snapshot or sources-consulted handling; pattern pages, index hubs, or backlog entries touched; any default skipped because the knowledge base lacked the folder; and a reminder to check the capsule before deleting the source conversations. Do not mention the corrections register or any applied correction in the summary unless the user asks.

Do not offer to publish the artifact or to delete conversations; both are the user's call.

## Coordinates with

- handoff: packages unfinished work for a new session; capsule preserves finished work's reasoning
- using-scarecrow: routes framework requests to capsule; direct invocation also works
- setup: creates the knowledge base's local rules and structure; capsule files into it
- ingest: compiles sources into the wiki; capsules are not sources and never go to the sources folder
- health-check: finds capsules with stale revision triggers during upkeep

## Changelog

### 4.0.2 (2026-10-26)

Declared using-scarecrow as the framework router and setup as the creator of the knowledge base's local rules and structure. Existing component relationships and direct invocation remain available. New pattern pages follow the local wiki frontmatter contract, with default pattern-page frontmatter (`type`, a specific `title`, empty `sources`, and `verified: pending`) when local rules are silent.

### 4.0.1 (2026-10-17)

Corrections stay silent in the closing summary too: step 2 applies them in everything the run writes and says, and step 10 never mentions the register or an applied correction unless the user asks. Fix 1 from the 2026-10-17 eval (case 4).

### 4.0.0 (2026-10-08)

Portability rewrite. The skill no longer assumes one owner or one vault: it finds the knowledge base root, reads its rules file, and takes routing, corrections register, pattern pages, skill backlog, link style, and writing style from a capsules section there, with generic defaults when the rules are silent. Owner's name, the vault-specific routing table, the fixed errata path, the backlog path, and task-system and publishing references removed. New guards: never write into an immutable sources folder or a project's received folder. `source-session` gains Codex as a surface. The previous vault-specific behavior now lives in that vault's own rules file. Status set to testing until a live run in each kind of knowledge base.

### 3.1.1 (2026-09-29)

Portability pass: added `## Setup` and `## Coordinates with`, and a `.skillbuild.json` marking the skill vault-resident. No behavior change.

### 3.1 (2026-08-26)

Skill-candidate method capsules route to the future skill's folder, creating it ahead of the build; non-candidate method capsules keep their earlier route.

### 3.0 (2026-08-23)

Major rewrite after a live-run audit: co-location routing, `method` capsule type, paired capsules, skill-candidate convention, fixed pattern-entry format, `source-session` fallback, index-hub append, rules read from AGENTS.md with folder layering, errata check as step 1.

### 2.1 and earlier

Pre-changelog. See shipped snapshots in this folder.
