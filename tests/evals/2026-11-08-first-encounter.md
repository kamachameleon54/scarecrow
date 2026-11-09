# Scarecrow: first outside encounter and onboarding observations

Recorded: 2026-11-08 (America/Los_Angeles). Original repository snapshot: `5d4822e5acf897f814b586f08bb81ff01fd86fb8` (0.2.0). Authoring context reported by the owner: the framework was written using Claude. Observer: the assistant in a ChatGPT Work/Codex session, approaching this repository for the first time in this conversation.

This record preserves that encounter before later edits make its sequence hard to reconstruct. The observer had the owner's conversation and general assistant context; this was not a blinded study, an installed plugin session, or a novice human trial. The owner initially asked about repository access, then invocation, distribution, testing, and training. The observer subsequently became an editor of the onboarding changes. Later forward-tests belong to the separate section below and cannot replace the first encounter.

## What happened before editing

| Encounter | Observed evidence | Limit of the observation |
|---|---|---|
| Owner supplied a GitHub URL and asked whether it was accessible | The connected GitHub integration returned the repository's root listing, then the README | Access through this account says nothing about a coworker's permissions or plugin installation |
| Observer read the README to explain how to invoke Scarecrow | It identified `using-scarecrow` as the entry point, five components, local rules, install commands for Claude Code and Codex, and explicit maturity limits | Reading instructions is not automatic skill discovery or observed execution |
| Owner asked whether sharing it would help others build their own second brain | Observer explained the six skills and install/invoke sequence, and said the framework supports that use case | That was a capability assessment from documentation, not an observed successful new-user experience |
| Owner requested testing | Direct GitHub clone returned a network-policy 403; files were instead retrieved at the pinned snapshot through the GitHub integration and reconstructed locally | This bypassed the normal acquisition route, so it cannot validate someone following the README |
| Observer examined the available CLI | Local CLI reported `codex-cli 0.167.0-alpha.4` and exposed the documented marketplace/add commands | Command availability alone does not establish package acceptance |
| Observer tried local marketplace registration | `codex plugin marketplace add <local snapshot> --json` failed because the marketplace directory was read-only | Registration, installation, automatic routing, and fresh CLI conversation remained untested; this did not establish a Scarecrow defect |
| Observer ran the repository suite | All 16 tests passed locally | These test the checker and vendored-copy parity, not model behavior or newcomer understanding |
| Observer used disposable checker fixtures | A modified immutable source failed; pending verification warned; absent project header fields warned with exit 0; nonexistent source metadata and an impossible verification date were not flagged | The missing-source and invalid-date runs also had an unrelated orphan warning after the fixture edit; they were not wholly clean outputs. These findings are distinct from onboarding and were not fixed in this change |

## What the encounter revealed

The README gave the observer a useful structural map quickly. It also clearly separated code checks from installation and live behavior. The observed gap was in the conversation between distribution and use: the owner repeatedly had to ask what invoking the framework would mean for another person, whether it would establish their own brain, and how to train someone familiar with chat. Those questions motivated guided first use; they do not prove that an unobserved novice would fail.

The observer's early "yes" about helping others was broader than the evidence justified. The careful formulation is: the instructions support the use case; successful installation, interpretation by a particular harness, and usefulness to a particular person each require their own observation. Keep these distinctions in future demonstrations.

The key transition is from conversation to selected, inspectable files. A person comfortable with chat needs to understand what is saved, which folder is accessible, what remains an assumption, and what they can ask next. The agent needs confirmed boundaries and preferences, plus a source it can interpret with the person. This is working-context adaptation through files, not model retraining or automatic access to old chats.

## Change prompted by the encounter

The owner asked to build this engagement into the loaded skill. The revision routes introductory requests through setup's `references/first-session.md`, keeps a short resumable onboarding record, and introduces the file workflow through one useful task. Specific work requests bypass the walkthrough. Standing preferences need confirmation; existing file protections remain in force. Setup checks and fresh-session retrieval have separate completion states.

## Forward-tests after the revision

Method: independent agents with no inherited conversation, given the revised entry-skill path and a task-local request. They share this host, available tools, and system instructions; they are not separate installed Codex/Claude harnesses. Scenario names below describe synthetic fixtures, not the owner's files. Skill activation was explicit, so these runs do not test automatic discovery.

### Newcomer, no project selected

Prompt: "I installed Scarecrow. I'm used to chatting with Claude, but I don't understand what I'm supposed to do here or whether I need to code. Can you help me get started?"

Observed first response:

> You don’t need to code. You can talk to me much as you would with Claude; here, I can also help work with files in the folder this session can access.
>
> Scarecrow keeps selected background, decisions, and working preferences in saved notes so future sessions can read them. It doesn’t automatically import your earlier chats or remember everything—we’ll choose what to keep together.
>
> Let’s start with something useful: what’s one project or recurring task you’d like help with, especially something you’re tired of explaining again in each new chat?

Assessment: the opening explains the transition, avoids a command tutorial, and asks one goal question. This initial response alone does not establish that scaffolding, preference storage, or retrieval works.

### Returning user, walkthrough skipped

Fixture: local rules, a skipped onboarding record, an index, and a garden-plan page. Task: "When do we water the garden beds, and who opens the shed?"

Observed answer: "Water the garden beds **Tuesday and Saturday at 7 a.m.** **Morgan opens the shed.**" It linked the fixture's `wiki/garden-plan.md` and did not restart onboarding. The answer matched the source. This verifies one explicit-load retrieval case on this host, not retrieval from a newly built brain or a second product.

### Adopt existing notes

Fixture: an existing `AGENTS.md` requiring approval for changes, plus `notes/client.md`. Request: a freelance designer, familiar with ChatGPT but new to Codex, asks for client-meeting help from that folder and asks to keep existing notes intact.

Observed response: inspected the folder and local rules; reported one client note; explained the four parts in meeting-preparation terms; proposed starting with one note; asked whether to use it as the first source. No files were changed. This supports the first-turn adoption boundary. Approval, later ingestion, and completed adoption were not exercised in this initial turn.

## Remaining validation and revision triggers

- Run the README's install path in an ordinary writable Codex installation and separately in Claude Code; record versions, invocation, package visibility, and any errors.
- Give a real new user the repository link without coaching. Preserve their questions, the actual assistant responses, and file outcomes with their permission. Do not replace raw observations with a polished reconstructed story.
- Exercise resumption, direct setup invocation, denied file access, declined preference storage, and a fresh session retrieving material generated during onboarding.
- Revisit the onboarding if it delays a concrete request, repeatedly asks answered questions, stores unconfirmed preferences, or calls a scaffold a completed experience.
- Preserve this first-encounter account when later behavior improves; append dated evidence rather than rewriting what originally happened.

## Appended: continuing the newcomer scenario

The same newcomer agent was subsequently given a synthetic garden-club goal, an explicitly selected empty folder, Codex-only use, no git or sync, an explicitly selected planning note, a privacy exclusion for member contacts and finances, and a request to remember concise answers. The source specified a March 13, 2027 seed swap at a community hall, Jules bringing envelopes, seed labels containing variety and harvest year, and an unconfirmed room booking.

Observed checkpoint: the agent created the scaffold, preserved the source with a checksum, ran structure checks, and kept onboarding at `started`. It presented four takeaways and proposed exact standing-preference wording for confirmation. It explicitly said nothing had yet been compiled into reference notes. The synthetic user then approved the takeaways and preference, reiterated that the booking must remain unconfirmed, and asked it to finish.

On continuation, the agent wrote `wiki/seed-swap.md`, indexed and logged it, created a project preparation checklist, recorded the approved preference in root rules, and kept the booking unconfirmed. It set the onboarding stage to `ready-for-retrieval-check`, provided a concrete next question for a fresh session, and still said retrieval was not tested. The observer independently reran structure verification: zero failures and zero warnings. Generated fixture dates used 2026-11-09 from the independent agent's session context, whereas this encounter record uses the owner's local date, 2026-11-08; these are synthetic test artifacts, not user event timestamps. Future cross-host testing should check date and timezone propagation explicitly.

A second independent agent, with no inherited conversation or supplied source facts, then received only the entry-skill path, this newly generated brain's folder, and the question: "What is planned for our seed swap, and is the room booking confirmed? Cite the saved note." It answered:

> The seed swap is planned for **March 13, 2027**, at the **community hall**. Jules will bring envelopes, and members should label seeds with **variety and harvest year**.
>
> The **room booking remains unconfirmed**.

It cited `wiki/seed-swap.md`, matching the generated page. This establishes one successful fresh-agent retrieval from files created during the revised onboarding, within this shared host. It does not establish plugin installation, a separately launched CLI session, automatic skill discovery, or Claude Code behavior. The retrieval agent was instructed to make no writes, so the fixture record was intentionally left at `ready-for-retrieval-check`; this appended observation is the evidence of the retrieval result.

## Appended: owner identifies the existing development path

The owner pointed out that Scarecrow already contains additional steps for developing the brain beyond initial setup. A closer review confirmed this: ingest's routing ladder grows reference knowledge selectively; capsules preserve organization decisions, reusable patterns, and revision triggers; health-check J3 and J5-J10 revisit decisions, status, folder fit, rule quality, contradictions, and consolidation. The observer's earlier explanation understated those existing capabilities by describing ongoing development as largely missing.

The resulting change is chiefly discoverability and coordination: ordinary-language requests now reach a development guide, setup can make a targeted extension, local rules describe evidence-based adaptation, and standard upkeep can surface an optional fit question. The existing components retain ownership and approval boundaries. Repeated usage is evidence only when present in the available record or supplied by the owner; the guide does not invent a history or silently turn one-off requests into standing preferences.

## Appended: recurring maintenance invitation

The owner requested that first use suggest a recurring gap check. The setup already had a four-week upkeep date and an offer to schedule a reminder; the revision makes this a dedicated conversational step after a useful result. It proposes a guided-review reminder or a supported unattended standard health-check report, asks for opt-in and missing timing details, checks host capability and folder access, and reports whether a real scheduled task was created. A saved date is explicitly not a timer. Installation does not itself enable background work. No recurring task for the owner was requested or created during this repository change.

Two further independent agents received the revised skill paths and synthetic requests, with no inherited conversation:

- **Explore growth:** the owner of the generated garden brain asks whether workshop planning should all go in the wiki, requesting options before changes. The response cited local rules and the seed-swap hub, distinguished reference knowledge from project work, offered three bounded options, and recommended starting with one workshop project. It labeled paths as proposals and changed no files. This checks one exploration response, not implementation of an extension.
- **Maintenance invitation:** the owner says the first useful notes are saved and asks how to remember maintenance. The response listed missing/outdated information, unresolved questions, broken links, conflicts, and setup fit; identified the saved December 7 review date; explicitly said no reminder was scheduled; and asked whether to set up a recurring reminder or review on demand. The test explicitly prohibited scheduler writes. It checks explanation and opt-in, not scheduler availability or task creation.

The existing 16 checker/parity tests passed again after these instruction changes. Skill frontmatter parsed and referenced files were present. No separate Codex/Claude installation or real scheduler execution was validated by these runs.

## Appended: proposal-first onboarding

The owner asked to continue developing onboarding in the repository. The first-session guide now supports guided steps or a proposed starting structure, reuses an already expressed choice, records the selected approach only when writes are authorized, and offers a handoff if the person pauses before authorizing files. It explicitly starts at first invocation unless an install-time launch is verified for that host.

An independent agent received the revised entry-skill path and a synthetic freelance-photographer request: organize clients, shoot plans and deadlines in a selected empty folder; propose the structure before creating anything; consider reminders later. The response offered shoot-specific project folders and shared reference notes, explained a fictional brief-to-plan-to-return workflow, stated no files had been created, deferred reminders, and asked whether to create the proposal. Inspection confirmed the folder remained empty. This supports the proposal/approval boundary for one explicit-load response, not installation or automatic activation. All 16 existing tests passed again after this revision.


## Planned scenario: refine Scarecrow across Codex, Claude, and shared project context

Requested by the owner after the first-encounter work. This is a proposed collaboration scenario and review contract, not an observed test result. Hina access, cross-assistant retrieval, and an installed-skill update have not been exercised here. Hina is this owner's optional shared knowledge space, not a requirement for Scarecrow users.

### User situation and prompt

The owner built Scarecrow using Claude, received a first outside review through Codex, and wants to preserve those observations while both assistants refine the experience.

Example request: "Help me continue refining Scarecrow with the Claude session that originally built it. Keep the skill and evaluations in the repository, use our Hina project note for shared goals and accepted decisions if both sessions can access it, and give Claude a short handoff to review the proposed changes."

### Where each part belongs

| Location | Authoritative content | How another session uses it |
|---|---|---|
| Scarecrow repository | Skill instructions, supporting resources, versioned implementation, evaluation evidence, and review discussion | Read the current branch/PR and named evaluation before proposing changes |
| Hina project note, if explicitly selected and accessible | Owner's goals, accepted design decisions, user feedback, and open questions, linked to the relevant PR | Read the selected note as project context; distinguish accepted decisions from suggestions |
| Short handoff | The next task, source links, current branch/commit, unresolved issues, and required stopping point | Continue without assuming access to the previous chat or model memory |
| Installed plugin or skill | A particular installed version of the repository instructions | Update through the host's supported mechanism after review/release; verify which version is actually available |

Keep detailed test evidence in the repository and link to it from Hina. Keep the project note concise rather than maintaining a second independently edited copy of the skill. If sources conflict, identify the conflict and ask the owner which decision applies; a note or review comment does not silently change executable instructions.

### Expected walkthrough

1. Inspect the current repository state and PR before describing the work as saved, merged, released, or installed. Name those states separately.
2. Preserve the original encounter and append later findings with dates and provenance. Do not rewrite the first observations to match the improved implementation.
3. If shared context is wanted, verify access to the specific Hina project note in each environment. A shared note does not guarantee shared GitHub access, file access, or plugin versions. If the note is unknown, resolve it through the available connection or ask for the selected location; do not invent a page or URL.
4. Before writing to Hina, establish the selected destination and authorization. Save only the agreed project context and links, following its local rules. A request to draft this scenario alone does not authorize publishing it to Hina or messaging Claude.
5. Draft a short handoff grounded in the current PR and evaluation. Give the other assistant a review task before further edits. The assistant can review work authored in another model; there is no requirement to return to the original model, and that model cannot be assumed to remember its earlier session.
6. Reconcile review findings in the repository, preserve observed results separately from proposed improvements, and record accepted product decisions in Hina only when authorized. Avoid simultaneous edits to the same branch; read the current head before applying changes and preserve intervening work.
7. After approved changes are merged or released, update and verify the installed version through the host. Feedback in chat, a handoff, a Hina note, or a merged PR does not by itself prove that an existing installation has received the change.

### Example handoff for the current review

This example points to draft PR #2. A future handoff should refresh the branch and commit before use.

> Review Scarecrow PR #2: https://github.com/kamachameleon54/scarecrow/pull/2
>
> Read `tests/evals/2026-11-08-first-encounter.md` on the PR branch before reviewing the changes. Assess whether conversational onboarding, ongoing development, and recurring gap checks fit the original framework. Identify conflicts, unnecessary complexity, and missing tests. Preserve the original observations and distinguish demonstrated behavior from unverified installation or scheduling claims.
>
> If a Hina Scarecrow project note has been explicitly selected and is accessible in this session, read its goals, accepted decisions, and open questions as supporting context. If it is unavailable, state that limitation and continue from the repository; do not imply that it was read.
>
> Return findings and proposed next steps before making further changes. Do not merge, publish, update a plugin installation, write to Hina, or send messages as part of this review.

### Evaluation cases to run

- **Shared note accessible:** supply a selected Hina project note and repository access. Check that the agent reads both, cites the sources actually used, preserves distinctions between proposals and accepted decisions, and gives a bounded review handoff.
- **Hina unavailable:** give repository access but no shared-note access. Check that the agent states the limitation, continues from the repo, and does not invent Hina content or make shared access a prerequisite.
- **Different installed version:** supply a plugin installation older than the PR. Check that the agent distinguishes proposed, merged/released, and installed behavior rather than claiming a feedback note updated the skill.
- **Concurrent work or conflicting decisions:** change the branch head or provide contradictory shared-note guidance. Check that the agent rereads current sources and surfaces the conflict before writing.

Completion evidence should include the actual handoff, sources read, any authorized writes, repository version, and observed outcomes. No cross-harness or Hina result should be marked passed solely because this scenario has been documented.
