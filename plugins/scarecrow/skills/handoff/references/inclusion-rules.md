# Inclusion Rules

The handoff is a bridge, not a backup. Every line should earn its place by preventing the next chat from failing or asking a redundant question.

## Always include

1. The work product or task in concrete terms (not "the thing we were working on")
2. Decisions that the next chat would otherwise have to re-litigate
3. Open questions that block the next step
4. File references by path or name (so the next chat can load them)
5. The next concrete step, stated specifically
6. The chosen first instruction
7. When the handoff opens as a new Claude Code Desktop session and the project is a git repository: a note that the new session starts in a fresh worktree, so this session's uncommitted changes are not visible there. Either commit the work before delivering the handoff, or name the uncommitted files and where the new session must get them. Folders that are not git repositories need no note.

## Never include

1. Full file contents. Reference the path. The next chat can read it.
2. Code blocks over 20 lines. Reference where the code lives instead.
3. Reasoning chains longer than 2-3 sentences per decision. The decision matters more than the path to it, unless using deep depth.
4. Chitchat, process narration, or meta-commentary about how the conversation went
5. Anything already documented in a project knowledge file, only when the destination is confirmed to have access to that file. Reference the file by name; when access is unavailable or unknown, include the necessary context.
6. Memory-style context about the user, only when the destination is confirmed to have access to the same memory. Otherwise include the load-bearing user context needed to execute safely; do not assume memory access carries across hosts.
7. Restatements of the project's standing instructions, only when the destination is confirmed to have access to those same instructions. Otherwise include the standing instructions needed to execute safely; do not assume project instructions carry across hosts.

## When in doubt

Ask: would the next chat fail or ask a redundant question without this line?
- Yes, include it.
- No, cut it.

## Common mistakes to avoid

- Pasting a draft artifact in full when a path reference would do
- Listing every decision made in the conversation instead of only the load-bearing ones
- Including "we discussed X" without saying what was decided about X
- Vague next steps like "continue the work" instead of "draft section 3 of references/foo.md"
- Forgetting the first instruction at the end
