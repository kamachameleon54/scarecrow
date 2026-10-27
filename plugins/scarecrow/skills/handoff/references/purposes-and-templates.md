# Purposes and Templates

This file contains the four handoff purpose templates and the depth modifiers. Apply the template matching the inferred purpose, then adjust section length using the depth modifier.

Contents: the four purposes · Template 1: Continuation · Template 2: Pivot · Template 3: Review · Template 4: Resume · depth modifiers. Every template carries an optional CONNECTORS section for connectors kept off by default.

## The four purposes

| Purpose | When to use | What changes in structure |
|---|---|---|
| Continuation | User wants to keep building the same work product | Emphasizes current state and next step |
| Pivot | User finished one thing and is starting a related new task | Emphasizes what the new task needs from the old |
| Review | User wants fresh eyes, gap analysis, or quality check | Emphasizes specific review questions |
| Resume | User is stopping and coming back later | Emphasizes re-orientation for the user's future self |

## Template 1: Continuation

```
PROJECT: [project name]
PURPOSE: Continuation of [work product]

WHERE WE ARE
[Current state of the work product. What exists, what is in progress.]

KEY DECISIONS MADE
- [decision and the reasoning if non-obvious]
- [decision and the reasoning if non-obvious]

OPEN QUESTIONS
- [unresolved question that affects next steps]
- [unresolved question that affects next steps]

FILES AND REFERENCES
- [path or name]: [what it is and why it matters]

CONNECTORS (only when some are off by default)
- [connector]: [what the next session uses it for]

NEXT CONCRETE STEP
[The specific next move, not a vague direction]

FIRST INSTRUCTION FOR YOU
[Chosen opening move from the candidates]
```

## Template 2: Pivot

```
PROJECT: [project name]
PURPOSE: Pivot from [completed work] to [new task]

BACKGROUND
[What was just built or decided. 2-3 sentences.]

WHY WE ARE PIVOTING
[The new task and how it relates to the completed work]

WHAT THE NEW TASK NEEDS FROM THE OLD
[Specific outputs, decisions, or artifacts that carry forward]

FILES AND REFERENCES
- [path or name]: [what it is]

CONNECTORS (only when some are off by default)
- [connector]: [what the next session uses it for]

DO NOT REDO
[List anything the next chat might mistakenly try to rebuild]

FIRST INSTRUCTION FOR YOU
[Chosen opening move]
```

## Template 3: Review

```
PROJECT: [project name]
PURPOSE: Review of [work product]

WHAT WAS BUILT
[Concise description of the artifact or decision under review]

WHAT I WANT FRESH EYES ON
[Specific areas where I want scrutiny]

KNOWN CONCERNS
- [weakness or uncertainty I already see]
- [weakness or uncertainty I already see]

FILES AND REFERENCES
- [path or name]: [what it is]

CONNECTORS (only when some are off by default)
- [connector]: [what the next session uses it for]

REVIEW QUESTIONS
- [specific question for the next chat to answer]
- [specific question for the next chat to answer]

FIRST INSTRUCTION FOR YOU
[Chosen opening move]
```

## Template 4: Resume

```
PROJECT: [project name]
PURPOSE: Resume work on [task]

WHAT I WAS WORKING ON
[Describe the task in plain terms, as if reminding yourself]

WHERE I LEFT OFF
[The last concrete action taken]

WHY I STOPPED
[Context only, e.g., end of day, waiting on something]

FILES AND REFERENCES
- [path or name]: [what it is]

CONNECTORS (only when some are off by default)
- [connector]: [what the next session uses it for]

WHAT I PLANNED TO DO NEXT
[The next move I had in mind before stopping]

FIRST INSTRUCTION FOR YOU
[Chosen opening move, often a re-orientation request]
```

## Depth modifiers

Apply after selecting a template.

| Depth | Target length | Per-section guidance |
|---|---|---|
| Quick | ~250 words | One sentence per section. Only the most critical decision. One open question maximum. Skip background context that the next chat can infer from project files. |
| Standard | ~500 words | 2-3 sentences per section. All key decisions. Top 2-3 open questions. Default mode. |
| Deep | ~900 words | Full reasoning for each decision including rejected approaches. All open questions with context. Use when architectural choices or design rationale need to carry forward. |

When in doubt, use standard. Quick handoffs that are too sparse force the next chat to ask redundant questions, which defeats the purpose.
