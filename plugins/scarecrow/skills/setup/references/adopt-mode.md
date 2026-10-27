# Adopt mode: adding a brain to an existing notes folder

The person already has notes. Their folders, names, and habits are the starting point; the goal is to make them findable by an agent without rearranging them.

## 1. Inventory before touching anything

- List top-level folders and count files by extension.
- Read any existing `AGENTS.md`, `CLAUDE.md`, `README.md`, or index/home note in full.
- Note the tool in use (an `.obsidian/` folder means Obsidian; leave it alone).
- Note whether the folder is a git repo (`git status`).

Report the inventory to the person in a few lines before writing anything.

## 2. Existing rules files

- If `AGENTS.md` exists: keep every line the person wrote. Add the missing sections from the template under clear headings and show the person the diff.
- If only `CLAUDE.md` exists with real content: move its content into a new `AGENTS.md` (keeping wording), then replace `CLAUDE.md` with the pointer shape. Do this only with the person's approval, since it changes a file they wrote; if they decline, add `@AGENTS.md` as a line at the end of their `CLAUDE.md` instead.
- If neither exists: write both from the template.

## 3. Map, do not move

- Describe each existing top-level folder in the rules file's folder map.
- Create `raw/`, `wiki/`, and `_system/` alongside the existing folders. Create `projects/` only if the person's work does not already have a home; if it does, treat their existing work folders as the project folders and add `_index.md` and `status.md` there. Where a folder already has a hub note (`_index.md`, `README.md`, or a home note), add the five-field header (`references/page-templates.md`, Project hub) to that note instead of creating a second hub, and keep the person's existing frontmatter keys. If a key they already use clashes (a `status` holding free text, or a second state field such as `lifecycle`), list it in the proposal rather than renaming it: one field name for state across the brain is the goal, and the rename is theirs to approve.
- Existing notes can be cited in place as sources. Copy a note into `raw/` only when the person wants it frozen.
- `wiki/index.md` may list existing notes that already work as compiled pages, under their real paths.

## 4. Proposed changes go in a list

Anything that would move, rename, merge, or delete a file goes into a numbered proposal in the hand-over summary, each with the reason. Carry out none of them until the person approves specific items.

## 5. Verify

Run `scripts/check_brain.py`. In adopt mode it checks only the scaffolded parts plus the person's files that the index links to; it does not judge the person's own note formats.
