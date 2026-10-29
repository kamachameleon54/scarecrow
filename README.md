# Scarecrow

Scarecrow is a composable framework for building and caring for a durable, plain-markdown second brain with Claude Code or Codex. Sources, compiled notes, decisions, and project work live together under local rules the agent reads first. Obsidian is optional.

The structure builds on Andrej Karpathy's [LLM Wiki idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), adding project work beside its context and a corrections register with dated upkeep.

## Skills

Start with `using-scarecrow`, the framework front door. It reads local rules and selects the smallest component that owns the request. You can also invoke a component directly.

| Skill | Purpose |
|---|---|
| `using-scarecrow` | Routes framework requests to the appropriate component and carries the shared doctrine. |
| `setup` | Creates a new brain or adopts an existing notes folder, with root rules, immutable sources, a linked wiki, project context, corrections, and upkeep. |
| `ingest` | Reads one source, checks its takeaways with the owner under the local ingest rules, and compiles durable reference knowledge. |
| `handoff` | Drafts a self-contained prompt for continuing unfinished work in another session. |
| `capsule` | Preserves the reasoning behind completed work in a durable record. |
| `health-check` | Checks structure and upkeep candidates, records the visit, and proposes repairs for approval. |

Local rules govern folder layout, source immutability, privacy, corrections, and approval gates. Read them before applying a component. Adopting existing material calls for a proposal and approval before moving, deleting, overwriting, or broadly reorganizing it.

## Install

These commands use the repository at `kamachameleon54/scarecrow` and require it to be available on GitHub.

### Claude Code

```bash
claude plugin marketplace add kamachameleon54/scarecrow
claude plugin install scarecrow@scarecrow
```

Invoke `/scarecrow:using-scarecrow` to enter through the framework. Direct component invocations are `/scarecrow:setup`, `/scarecrow:ingest`, `/scarecrow:handoff`, `/scarecrow:capsule`, and `/scarecrow:health-check`.

### Codex

```bash
codex plugin marketplace add kamachameleon54/scarecrow
codex plugin add scarecrow@scarecrow
```

Invoke `$using-scarecrow`, or a component by name: `$setup`, `$ingest`, `$handoff`, `$capsule`, or `$health-check`. If the host offers a skill picker, select the corresponding Scarecrow skill there.

### Individual skill folders

Copy a folder from `plugins/scarecrow/skills/` into `~/.claude/skills/` for Claude Code or `~/.agents/skills/` for Codex. Install all six for framework routing and component handoffs. With individual Claude Code installs, invoke `/using-scarecrow` or the component's unprefixed skill name.

## Requirements

The bundled `check_brain.py` checker requires Python 3.9 or later and uses only the standard library. Both `setup` and `health-check` include a copy so each can run independently. The other skills are instructions and need no Python packages. Agents need the filesystem access required by the selected workflow and its local approval rules.

## Maturity and validation limits

Version `0.2.0` follows the first release, `0.1.0`. The framework front door, setup, and health-check are draft components; ingest and capsule are testing components; handoff is stable. Component versions are recorded in their skill metadata and can differ from the plugin version.

The repository's tests (`python -m unittest discover -s tests`, run in CI on Linux, macOS, and Windows with Python 3.9 and 3.13) cover the bundled checker's behavior and the parity of its two copies. They do not establish installation, automatic routing, behavior in a fresh Claude Code or Codex session, deployment, or observed results in a live knowledge base. Fresh cross-platform evaluations and a supervised pilot remain necessary before treating the framework as broadly validated.

## License

MIT. See [LICENSE](LICENSE).
