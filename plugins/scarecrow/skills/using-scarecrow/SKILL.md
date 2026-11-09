---
name: using-scarecrow
description: "Guides first use and ongoing development of a Scarecrow second brain, routing work to setup, ingest, handoff, capsule, or health-check. Use when getting started, exploring or adapting a setup, asking where something belongs or what to build next, when the right component is unclear, or when beginning work in a Scarecrow-managed knowledge base. Read local rules first and load only the component that owns the request."
metadata:
  status: draft
  version: 0.2.0
  last-updated: 2026-11-08
  decision: "2026-11-08: Make first use and ongoing development conversational, using existing components and confirmed local rules."
  feedback: "none"
  log: "#Changelog"
  tags: []
---

# Using Scarecrow

Scarecrow is a composable framework for building and caring for a durable, plain-markdown second brain. Read the knowledge base's root rules and any more-specific rules before choosing a component. Local rules override package defaults.

## Welcome and resume

For a getting-started request, an explicit request for a walkthrough, or a bare invocation with no task in a new brain, load `setup` and its `references/first-session.md`. Keep the welcome conversational and ask about one useful task before discussing folders or commands. This is a guided conversation inside the current session, not a separate agent or a new skill the person must learn.

When the local rules point to an onboarding record (default `_system/onboarding.md`), read it before offering another walkthrough. Resume its next step if the person asks to continue. A missing record alone does not mean an experienced person needs onboarding. For a specific work request, route directly below; for a bare invocation in an established brain, briefly offer help with its current work and ask what they want to do. Honor a request to skip the walkthrough without requiring a completion record.

## Route the request

| Need | Load |
|---|---|
| Create a new brain or adopt an existing notes folder | `setup` |
| Explore the setup, decide where something belongs, adapt to changed work, or choose what to build next | Read `references/develop-your-brain.md`, then load the component it selects |
| Compile one source into durable reference knowledge | `ingest` |
| Continue unfinished work in another session | `handoff` |
| Preserve the reasoning behind completed work | `capsule` |
| Inspect and maintain system health | `health-check` |
| Review gaps or run the agreed recurring maintenance visit | `health-check` in standard scope, unless the person asks for a quick or deep check |

If a request spans components, use the fewest components that fully cover it and keep each component's stopping condition. Do not copy a component's procedure into this skill.

## Keep the path visible

Explain the next useful action in the person's language rather than requiring component names. At a milestone or when the person expresses friction, briefly offer one relevant way to develop the setup; follow `references/develop-your-brain.md`. Finish a concrete work request first. During ordinary successful work, keep helping without repeating invitations or treating every correction as a redesign request. Routine exploration is available whenever requested, and a standard health-check can surface it at the agreed upkeep visit.

## Shared doctrine

- Preserve the knowledge base's source immutability, correction, privacy, and approval rules.
- Separate a possibility, confirmed finding, accepted decision, local implementation, validated implementation, deployed package, and observed live outcome.
- Prefer a proposal and explicit approval before moving, deleting, overwriting, or broadly reorganizing existing material.
- Keep platform behavior equivalent for Claude Code and Codex unless a host limitation is stated.

## Coordinates with

- setup: creates or adopts the knowledge base and writes the local rules every component follows
- ingest: compiles one source under the local ingest contract
- handoff: carries unfinished work to another session
- capsule: preserves reasoning behind completed work
- health-check: performs scheduled inspection and proposes repairs

## Changelog

### 0.2.0 (2026-11-08)

Add optional guided first use, continuity through a local onboarding record, and direct routing for returning users. Behavior evaluations are recorded separately from installation validation.

### 0.1.0 (2026-10-26)

Initial package bootstrap. Routes to the five focused components and carries only shared doctrine.

