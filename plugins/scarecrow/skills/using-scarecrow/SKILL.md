---
name: using-scarecrow
description: "Routes work inside a Scarecrow second brain to the smallest focused skill: setup for creating or adopting the brain, ingest for compiling a source, handoff for continuing unfinished work, capsule for preserving finished-work reasoning, and health-check for scheduled upkeep. Use when a request concerns the Scarecrow framework as a whole, when the right component is unclear, or when beginning work in a Scarecrow-managed knowledge base. Read the local rules first and load only the component that owns the request."
metadata:
  status: draft
  version: 0.1.0
  last-updated: 2026-10-26
  decision: "2026-10-26: Use Scarecrow as the framework identity and route to its five focused components."
  feedback: "none"
  log: "#Changelog"
  tags: []
---

# Using Scarecrow

Scarecrow is a composable framework for building and caring for a durable, plain-markdown second brain. Read the knowledge base's root rules and any more-specific rules before choosing a component. Local rules override package defaults.

## Route the request

| Need | Load |
|---|---|
| Create a new brain or adopt an existing notes folder | `setup` |
| Compile one source into durable reference knowledge | `ingest` |
| Continue unfinished work in another session | `handoff` |
| Preserve the reasoning behind completed work | `capsule` |
| Inspect and maintain system health | `health-check` |

If a request spans components, use the fewest components that fully cover it and keep each component's stopping condition. Do not copy a component's procedure into this skill.

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

### 0.1.0 (2026-10-26)

Initial package bootstrap. Routes to the five focused components and carries only shared doctrine.
