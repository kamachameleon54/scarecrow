---
name: handoff
description: Drafts a self-contained handoff prompt that captures the current conversation's work state so the work can continue in a new chat or session in the same project, when context is closing or the next task deserves its own session. Use when the user says "handoff," "draft a handoff," "package this for the next chat," "I need to start a new chat," "spin this off," "make this a task," "run it here," or any variation indicating they want to migrate work to a fresh conversation, including from a phone. Infers purpose and depth, offers a multiple-choice pick of first instructions, then drafts a structured prompt with work state, decisions, open questions, file references, and the chosen first instruction embedded. Do NOT use for preserving the reasoning behind finished work (capsule) or general conversation summarization.
metadata:
  status: stable
  version: 1.8.1
  feedback: ""
  decision: "2026-10-26: Reconcile framework routing and setup ownership while retaining direct handoff invocation"
  log: "#Changelog"
  last-updated: 2026-10-26
---

# handoff

## When to use this skill

The user is approaching context limits in a long working conversation, or has finished one piece of work and wants the next piece in its own session, and needs to migrate work to a fresh chat in the same project. Confirm the destination's access to project knowledge files, project instructions, installed skills, and MCP connectors; never assume access carries across hosts. When access is unavailable or unknown, the handoff carries the load-bearing context and instructions needed to execute safely. Do not assume the destination can retrieve this conversation's transcript. The handoff prompt is the bridge.

This skill is reactive only. It does not proactively suggest handoffs.

## Reference file routing

| If you need | Read |
|---|---|
| The four purpose templates and depth modifiers | references/purposes-and-templates.md |
| Rules for what to include and exclude | references/inclusion-rules.md |
| Examples of first-instruction candidates by purpose | references/first-instruction-patterns.md |
| How to run a handoff here through native delegation and relay its report | references/subagent-brief.md |

## Workflow

1. **Infer purpose.** Read the conversation context and decide which of the four purposes fits best. Default reasoning:
   - Unfinished work product, user wants to keep building it: continuation
   - Finished one thing, user is starting a related new task: pivot
   - User wants fresh eyes, quality check, or gap analysis: review
   - User is stopping for the day or coming back later: resume
   - If genuinely unclear, default to continuation and note the assumption

2. **Infer depth.** Default to standard. Use quick only if the work is stable and the next move is obvious. Use deep only if architectural decisions, rejected approaches, or design rationale need to carry forward.

3. **Ask which first instruction to embed.** Load references/first-instruction-patterns.md. Generate 2-3 candidate opening moves tailored to the work state, and present them as a multiple-choice question before drafting anything: numbered options plus an explicit "or write your own." Use the harness's question tool (e.g. AskUserQuestion) if one exists; otherwise ask in chat and wait for the reply. This one question is asked upfront on purpose: embedding the chosen instruction in the draft means the handoff is generated exactly once, which matters when context is nearly exhausted; regenerating a full handoff costs far more than one short exchange. Skip the question only if the user has already named the next move or said to just pick; in that case choose the best-fit candidate and label the choice.

4. **Draft the handoff.** Load references/purposes-and-templates.md and use the template matching the inferred purpose. Apply the depth modifier. Embed the chosen first instruction in the FIRST INSTRUCTION FOR YOU section. Follow references/inclusion-rules.md to keep the handoff scannable. Fill CONNECTORS per the connector paragraph under How to apply this context; leave the section out when nothing is off by default.

5. **Deliver the handoff.** First state the inferred purpose and depth in one sentence. Then pick the delivery path by checking the session's tool list, not by guessing the surface:
   - **`spawn_task` is present** (Claude Code Desktop exposes it as `mcp__ccd_session__spawn_task`): deliver the handoff as a task chip. Call `spawn_task` with `prompt` set to the complete handoff text, `title` and `tldr` per step 6, and no `cwd` unless the work belongs in a different repo. Before `spawn_task`, switch on any CONNECTORS entry that is off (the session connector tool, `set_session_connector_enabled`, where the harness has it); that switch is also the default for new sessions, so the chip's session opens with the tools loaded. Then print one line naming the chip title and saying the new session opens with the handoff loaded. Do not also print the code block. Before printing that line, check whether the user is away from the desktop: call `get_session` with `self` (`mcp__ccd_session_mgmt__get_session`, load it with ToolSearch if it is deferred) and read `remoteControlActive`, or take the user's word ("I'm on my phone," "I'm remote"). Chips do not render in Remote Control, so a remote user cannot see or click the chip. If the user is remote, still create the chip (it waits at the desktop) and end the note with the offer: say "run it" and the handoff runs here through native delegation, with its report relayed into this session and background execution used when supported (step 7). If the user already asked for that ("run it," "run it here," "start it," "just do it here"), skip the chip and go straight to step 7. The tool's own description talks about flagging out-of-scope issues; a handoff is exactly that shape, a self-contained prompt for a separate session, so it is the right tool even though it does not say "handoff." Print the code block only if the call fails or the user asks for it.
   - **`spawn_task` is absent** (claude.ai chat, Cowork, the CLI, any other harness): if the user asked to run it here, go to step 7. Otherwise show the complete handoff in a single code block ready to copy.
   Either way the chosen first instruction is already embedded; do not list alternative candidates after the draft. End with a short note that the user can ask for a different purpose, depth, or first instruction and the skill will regenerate.

6. **Name the chip** (chip delivery only). `title` comes from the purpose: continuation and pivot titles are an imperative phrase naming the next move ("Scan 7 candidate skills with SkillSpector"); review titles start with "Review"; resume titles start with "Resume". Keep it under 60 characters; it becomes the chip label and the new session's title. `tldr` is one or two plain sentences on why this is being handed off now, with no file paths. When the user asks for several handoffs in one turn, draft each one and make one `spawn_task` call per handoff in the order drafted; chips keep creation order. If the `spawn_task` result shows an existing chip on the same job, say so in the one-line note and leave it alone; withdraw a chip with `dismiss_task` only when the user asks or when replacing one you created in this same turn. If the project is a git repository, the new session starts in a fresh worktree, so apply the worktree rule in references/inclusion-rules.md before spawning.

7. **Run it here** (subagent rung, only when the user asks or accepts the offer in step 5). Load references/subagent-brief.md. Choose an available native delegation tool or API from the host's tool list and follow the local coordination rules. Dispatch one subagent with the complete handoff as its brief plus the brief's standing rules and report shape. Inherit the host's or project's model defaults unless local coordination rules specify otherwise; use background execution only when supported. Say in one line that it is running. If delegation is unavailable, deliver the complete handoff in a single copyable code block and explain that this host cannot delegate it here. After a successful dispatch, withdraw any chip created for the same handoff this turn with `dismiss_task`, if available; it is superseded. When the result is available, relay the report's substance to the user in this session, since the host may not display the subagent's report. Delegation does not guarantee a separately reopenable chat; say so if the user later wants to pick the work up independently. Launching a provider CLI from the shell is not a substitute for this rung.

## Quick reference (standard continuation handoff structure)

```
PROJECT: [project name]
PURPOSE: Continuation of [work product]

WHERE WE ARE
[2-3 sentences on current state]

KEY DECISIONS MADE
- [decision 1]
- [decision 2]
- [decision 3]

OPEN QUESTIONS
- [question 1]
- [question 2]

FILES AND REFERENCES
- [path or name]: [what it is]
- [path or name]: [what it is]

CONNECTORS (only when some are off by default)
- [connector]: [what the next session uses it for]

NEXT CONCRETE STEP
[one sentence]

FIRST INSTRUCTION FOR YOU
[the chosen opening move]
```

The other three purposes use different section headings. See references/purposes-and-templates.md.

## How to apply this context

The handoff prompt has to stand alone. Do not assume the next chat can retrieve this conversation's transcript or has memory of the work; access and refresh behavior depend on the host. Everything the next chat needs has to be either in the handoff text, in a project knowledge file you can reference by name, or in a skill the next chat will load.

When in doubt about whether to include something, ask: would the next chat fail or ask a redundant question without this? If yes, include it. If no, leave it out.

Reference files and artifacts by path or name, never by pasting full contents. The handoff is a bridge, not a backup.

**When the work lives in a second brain.** If the working folder has a root `AGENTS.md`, an `open-questions.md`, and project folders holding a `status.md` (the layout setup builds), the brain already carries most of the work state. Point at it instead of restating it: under FILES AND REFERENCES, name `projects/<name>/status.md` as the current state and `open-questions.md` as the unknowns, and make the first instruction start by reading both. Keep WHERE WE ARE to what this session changed, and list only the open questions this session raised. If this session produced state the files do not hold yet, put it in the handoff, and offer to write it into `status.md` or `open-questions.md` first so the next session finds one source.

**When some connectors are off by default.** A session only sees the tools of connectors that are switched on, so a handoff that needs a switched-off connector opens in a session that cannot do the work. Before drafting, check the user's or project's rules for a list of connectors kept off by default, and note any connector this session switched on for the work. Name each one the next session needs under CONNECTORS with its use. With chip delivery where the harness can switch connectors, switch them on before creating the chip, and end the handoff's first instruction with switching them back off when the work is done, so the defaults stay lean. With code-block delivery, the first instruction starts by switching them on; the tools arrive on the following turn.

A handoff is not a file, an Artifact, or a download. In Claude Code Desktop the chip is the delivery: the user clicks it and the new session opens with the handoff as its first message. Printing a code block when `spawn_task` exists makes the user copy and paste what the harness would have loaded for them. Launching the `claude` CLI from Bash is not a substitute; that session never appears in the desktop sidebar. A chip is only useful to someone at the desktop: Remote Control (the phone or claude.ai/code view of this session) does not show chips, and no tool in a desktop session can start a new session on its own, so the subagent rung is the only way to make progress for a remote user.

If the user says "handoff" without other context, infer aggressively from the conversation state. Do not ask the user to specify purpose and depth upfront; infer those, label the inference clearly, and let the user redirect if wrong. The only upfront question is the first-instruction choice in step 3, because that answer changes the draft's content and asking after the fact forces a regenerate.

## Setup

No scripts or configuration.

## Coordinates with

- capsule: preserves finished work's reasoning; handoff packages unfinished work for a new chat
- prompt-documenter: publishes finished artifacts; handoff never does
- using-scarecrow: routes framework requests to handoff; direct invocation also works
- setup: creates the brain's local rules and structure, including the `status.md` and `open-questions.md` a handoff points at instead of restating
- ingest: receives sources a handoff identifies as waiting for ingestion
- health-check: hands remaining approved numbered fixes to handoff when work continues in a new session

## Changelog

- **1.8.1 (2026-10-26)**: Declared using-scarecrow as the framework router and setup as the creator of the brain's local rules and structure. Reconciled reciprocal coordination with ingest and health-check; direct invocation remains available. Made delegation portable across hosts through available native tools, local coordination rules and model defaults, optional background execution, and a copyable handoff fallback. Removed assumptions about next-session transcript and memory access. Require destination-access confirmation before relying on project files, instructions, skills, or connectors; carry load-bearing context when access is unavailable or unknown.

- **1.8.0 (2026-10-12)**: Connector-aware handoffs. Templates gain an optional CONNECTORS section; the drafting session checks the rules for connectors kept off by default and names the ones the next session needs; chip delivery switches them on before `spawn_task` so the new session opens with them, and the first instruction switches them back off at the end; code-block delivery starts by switching them on.

- **1.7.0 (2026-10-08)**: Brain-aware handoffs. When the working folder is a Scarecrow second brain (root `AGENTS.md`, `open-questions.md`, `projects/<name>/status.md`), the handoff names those files as the state of record, keeps WHERE WE ARE to this session's changes, lists only newly raised questions, and offers to write unrecorded state into the files first. Added brain coordination and portable inclusion rules; trimmed the description's do-not list to capsule and general summarization (prompt-documenter and Notion logging dropped).

- **1.6.0 (2026-09-29)**: Description trimmed from 992 to 893 characters. Primary triggers kept ("handoff," "draft a handoff," "package this for the next chat," "start a new chat," "spin this off," plus "make this a task" and "run it here"); redundant phrasings ("handoff prompt," "hand this to a new session") and the purpose and depth enumerations cut. The do-not boundary now names both prompt-documenter and capsule. Em dashes removed from the body. Version normalized to three-part semver. Setup and Coordinates-with sections added; `.skillbuild.json` excludes the eval record.
- **1.5 (2026-09-26)**: Remote awareness and a subagent rung. Step 5 now checks `remoteControlActive` (or the user's word) after creating a chip, states that chips do not render in Remote Control, and offers to run the handoff here; new step 7 runs the handoff as a background subagent from `references/subagent-brief.md`, withdraws the superseded chip, and relays the report. Description gains "run it here" and the phone case. Probed and rejected alternatives recorded in the eval: ad-hoc scheduled task run-now (works, but unattended and archives on delete) and the `claude://code/new` deep link (no effect).
- **1.4 (2026-09-26)**: Chip delivery. When the harness exposes `spawn_task` (Claude Code Desktop), the handoff is delivered as a task chip that opens a new session with the prompt loaded; the code block remains the delivery everywhere else and the fallback if the call fails. Chip title and tldr rules keyed to purpose; multiple handoffs in one turn produce one chip each in order. Worktree caveat added to inclusion-rules.md for git repositories. Description gains "spin this off," "make this a task," and "hand this to a new session" triggers. Templates, purpose inference, and the first-instruction question are unchanged.
- **1.3 (2026-08-04)**: First-instruction selection moved before drafting. Candidates are now offered as a multiple-choice question upfront (with a write-your-own escape) and the chosen instruction is embedded in the single generated draft, eliminating the regenerate step when the user picked a candidate other than the skill's guess. v1.2 was a packaging-only rebuild of v1.1.
- **1.1 (2026-06-02)**: Shipped baseline (see shipped-v1.1.md).
