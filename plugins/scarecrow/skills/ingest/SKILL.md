---
name: ingest
description: "Compiles one source into a knowledge base's wiki: decides first whether the file belongs in the wiki at all, then reads it fully, confirms the takeaways with the owner, and writes or updates the compiled page, the index, and the log, leaving the source untouched. Works in any markdown knowledge base with a rules file (AGENTS.md or CLAUDE.md), an immutable sources folder, and a wiki folder, such as a scarecrow-style second brain or an Obsidian vault. Use when the user says \"ingest this\", \"run ingest on\", \"add this to the wiki\", \"compile this into the wiki\", \"wiki this source\", mentions that a new file landed in raw/, asks to promote a project file into reference knowledge, or asks whether something belongs in the wiki. Not for capsules, general note filing, project tracking, summarizing when no source file exists, or setting up a new knowledge base, which is setup."
metadata:
  version: 1.2.0
  status: testing
  tags: [ingest, wiki, knowledge-base, second-brain]
  decision: "2026-10-28: Read ingest settings from wiki/AGENTS.md as well as the root rules file"
  feedback: "Testing gate: one live ingest run must pass under the knowledge base's local rules"
  log: "#Changelog"
  last-updated: 2026-10-28
---

# Ingest

Compile one source file into a knowledge base's wiki, or route it to a cheaper home when the wiki is the wrong container. The wiki is compiled reference knowledge, and this skill is the mechanism that grows it: every page and every cross-link in it exists because an ingest run wrote it during synthesis.

## Setup

Stdlib only; no scripts and no config file. The skill needs read and write access to a markdown knowledge base. Everything specific to a particular knowledge base (folder names, page frontmatter, link style, the corrections file, whether to log, the cheaper routes) comes from that knowledge base's rules file, described under "Read the rules first". If the knowledge base records source checksums, the skill uses the check script owned by health-check and also bundled by setup; see step 9.

## Why this skill exists

Synthesis done once and kept beats re-reading raw documents on every question, but only if the compiled pages stay traceable and correct. Three things go wrong without a fixed procedure: sources get edited after the fact, so a compiled claim can no longer be checked; working files (trackers, meeting logs, task lists) get pulled into the wiki and bury the reference material; and a source that overstates or misreads something gets filed as fact before anyone looks. This skill holds the line on all three: the source stays immutable, the first decision is whether the wiki is the right home, and the owner confirms the takeaways before anything is filed.

## Read the rules first

Find the knowledge base root: the nearest folder at or above the working directory that holds `AGENTS.md` or `CLAUDE.md`. If none exists, ask where the knowledge base lives. If it has no wiki folder at all, stop and say so; setting up a knowledge base is setup's job. Read the root rules file, then `AGENTS.md` in the compiled-pages folder when it exists (`wiki/AGENTS.md` unless the root rules name another folder; a knowledge base whose root file has grown keeps the ingest procedure and settings there), then any folder-level `AGENTS.md` files along the path to the source, broadest to most specific.

Look in those rules for a section about ingesting (any heading containing "Ingest"). When it exists, it wins over the defaults below, point by point. It may set:

- **Folders**: where sources live (default `raw/`) and where compiled pages live (default `wiki/`)
- **Cheaper routes**: the knowledge base's own ladder for files that should not be ingested
- **Intake**: how a source lands in the sources folder (default: copy with the file-write tool)
- **Confirm gate**: whether the owner confirms takeaways before filing (default: yes)
- **Page frontmatter**: the fields a compiled page carries (default: `type`, `title`, `sources`, `verified`)
- **Link style**: double-bracket wiki links or relative markdown links (default: relative markdown)
- **Log**: the ingest log and its entry format (default: `wiki/log.md`)
- **Open questions**: where facts the source leaves unsettled go (default: `open-questions.md` at the root)
- **Corrections register**: the file of known-wrong facts (default: `_system/corrections.md`, else `_system/errata.md`)
- **Checksums**: whether and how sources are recorded after landing
- **Style**: writing rules for compiled pages

When the rules are silent on a point, use the default for that point. When the default needs a file the knowledge base does not have (no log, no open-questions file, no corrections register), skip that step and say so in the summary rather than inventing structure. The one exception is the index: if the wiki folder exists but has no index, create `index.md` there with a one-line preamble, because a page nobody can find is not worth compiling.

## First decision: does this belong in the wiki at all?

Most context-rich files should not be ingested. The wiki is the heaviest layer, reserved for reference knowledge that cuts across projects and is worth synthesizing once. Before writing anything, walk the cheaper routes, using the rules' ladder if they give one and this default if not:

1. **Leave it where it is.** Search, embeddings, or the folder it sits in already make it findable. The default for most project material.
2. **One line in the folder's index hub** (`_index.md` or similar) when the file will be deliberately navigated to.
3. **One short cross-reference** (a Related line with one to three links) when a specific connection has concrete retrieval value.
4. **Full ingestion** only for reference knowledge that earns synthesis.

Also read the wiki index before deciding. If it records routing decisions (a section listing sources deliberately kept out of the wiki), honor them; do not ingest a source the index says was routed elsewhere unless the owner explicitly overrides it.

If the request fails this test (a project tracker, task list, status file, meeting log, daily note, or a client's working document), say so, name the container that fits (the project folder, its status file, its index hub, the open-questions file), and stop. The wiki never holds project tracking or working artifacts.

## Corrections check

Before synthesizing, read the corrections register. Compiled pages are durable; if a listed correction touches the source's subject, apply it silently in the synthesis (use the correct fact or omit the contaminated passage). Do not annotate what was corrected in the page.

## The Ingest operation

One source per run. If the user hands over several, take them one at a time, each through the whole loop, unless the user explicitly asks for a batch, in which case run unattended per step 3.

1. **Locate the source.** It should be a file in the sources folder. If it is elsewhere in the knowledge base, use the escalation path below first. If it is not a file at all (pasted text, a conversation, something remembered), save it into the sources folder as a file first; every compiled page traces to a source file.
2. **Read it completely.** No skimming; synthesis from a partial read produces confident gaps.
3. **Confirm the takeaways.** Tell the owner the three to five takeaways you would file, and which page or pages they would go to (new or existing), then wait for confirmation or corrections. Sources overstate, and a misreading caught here never reaches the wiki. If the owner cannot confirm (they asked for an unattended run or a batch), file anyway, mark each touched page `verified: pending`, and list them in the summary for review. If the rules turn the gate off, file without waiting.
4. **Write or update the compiled page.** Use the rules' frontmatter, or match the shape existing pages use, or the default: `type` (concept, entity, summary, comparison, how-to, or decision), `title`, `sources` (paths to the source files), and `verified` (today's date once confirmed, or `pending`). Every page cites at least one source file. Add links to other wiki pages only where the synthesis genuinely connects; links serve retrieval, not graph density. When the source contradicts an existing page, note the contradiction on the page and in the summary; never silently overwrite what an earlier source said.
5. **Park what the source leaves unsettled.** A missing date, an unconfirmed rule, an unnamed owner: add it to the open-questions file, tagged with the project or topic, rather than writing a guess into the page.
6. **Update the index** with a one-line entry for any new page, or a refreshed line for an updated one, saying what question the page answers.
7. **Append to the log**: `## [YYYY-MM-DD] ingest | <source title>`, then one line naming the pages touched and whether the owner confirmed the takeaways. The log is append-only.
8. **Record source errors.** If the source itself contains a factual error worth correcting downstream, add it to the corrections register. Never edit the source.
9. **Record the checksum** if the knowledge base keeps one (a `.manifest.json` in the sources folder): run the check script the rules name, or `scripts/check_brain.py <root> --record-raw` from an installed health-check skill or setup's identical bundled copy. If no check script is available, say the manifest is now behind.
10. **Summarize**: the source; the page or pages created or updated; the index line; the log entry; contradictions noted; open questions added; corrections logged; any step skipped because the knowledge base lacked the file; and two or three follow-up questions the source raises.

## Escalation: a file from elsewhere in the knowledge base

When a file in a project folder (or anywhere outside the sources folder) has proven to be cross-cutting reference knowledge:

1. Copy it into the sources folder with a kebab-case name. Copy, never move: the original stays where its project uses it. Use the file-write tool; if the harness or a hook blocks the copy, or the file is binary and cannot be written that way, ask the owner to copy it in.
2. Run the Ingest operation against the copy.
3. Optionally add a cross-reference in the original pointing at the new page, if that aids retrieval.

A file in a project's `received/` folder is a source as sent and is never edited; escalate it the same way. If the rules allow citing files in place, the copy step can be skipped and the page cites the original path.

## Hard rules

- **Sources are immutable.** Never edit, rename, move, or overwrite a file in the sources folder or in any `received/` folder, including the one being ingested. Corrections go to the corrections register.
- **No ingesting from conversation or memory.** Save it as a source file first.
- **No bulk-link retrofit.** Links come from this synthesis, not from sweeps over existing notes.
- **Wiki scope is reference knowledge only.** No project tracking, task lists, status, or daily notes.
- **Graph density is never the goal.** If a link does not serve retrieval, leave it out.
- **Never create new top-level folders.** Missing optional files are skipped and reported.

## Style

Follow the rules' style section. When it has none, match the existing wiki pages; with no pages to match, write prose-first synthesis, functional lists only, active voice, no emoji.

## Coordinates with

- using-scarecrow: routes framework requests to ingest; direct invocation also works
- setup: creates the knowledge base's local rules and structure; ingest adds later sources one at a time
- capsule: capsules are not sources and never land in the sources folder; capsule pattern pages are the one wiki page not fed by ingest
- handoff: a handoff can point the next session at a source waiting for ingest
- health-check: owns the checksum script and identifies sources waiting for ingest, pages left `verified: pending`, wiki pages missing from the index, and changed source checksums

## Changelog

### 1.2.0 (2026-10-28)

Settings lookup also reads `AGENTS.md` in the compiled-pages folder (default `wiki/AGENTS.md`) on every run, so a knowledge base can move its ingest section out of the always-loaded root rules file. Root-file settings still work unchanged. No eval run.

### 1.1.0 (2026-10-26)

Moved the new-knowledge-base description boundary to setup and declared using-scarecrow as the framework router. Updated live coordination and checksum-script references to setup and health-check; direct invocation remains available.

### 1.0.0 (2026-10-08)

Portable successor to the vault-ingest skill (1.0.1). Finds the knowledge base root, reads its rules file, and takes folders, cheaper-route ladder, intake, confirm gate, frontmatter, link style, log, open-questions file, corrections register, checksums, and style from an Ingest section there, with scarecrow-brain defaults when the rules are silent. Kept from vault-ingest: the first decision (does this belong in the wiki at all), the routing-decision read of the index, the silent corrections check, escalation from project folders, and the hard rules. New: owner confirms takeaways before filing (`verified: pending` when unattended), unsettled facts go to the open-questions file, an append-only ingest log entry, checksum recording through scarecrow's check script, and `received/` files treated as immutable sources. Owner's name, vault folder names, the embedding plugin, and the fixed errata path removed.
