# pstack for Codex

A Codex adaptation of [Lauren Tan's pstack](https://github.com/cursor/plugins/tree/main/pstack). It keeps the engineering principles, playbooks, review rubrics, and verification tools, and replaces Cursor-specific runtime instructions.

## Install from this checkout

Requires Python 3 and a Codex CLI with `codex plugin` support. From the repository root, build a standalone marketplace in a new directory outside `pstack`:

```bash
python3 pstack/scripts/package-codex.py /tmp/pstack-codex-marketplace
codex plugin marketplace add /tmp/pstack-codex-marketplace
codex plugin add pstack@pstack-codex
```

Keep the marketplace directory while it is configured. For a durable installation, choose a permanent output location. Rebuilding requires a new output directory; the packager refuses to overwrite an existing one. The package contains only pstack, so the fork's other plugins are not installed. Start a new Codex session after installation.

The supported manifest is `.codex-plugin/plugin.json`. The upstream `.cursor-plugin` manifest remains for repository catalog validation, but this fork's pstack skills target Codex. It is not a promise of dual-host compatibility.

## Start

```text
$pstack:poteto-mode Reproduce this bug, fix its cause, and verify the behavior.
$pstack:interrogate Review my current changes without editing them.
$pstack:setup-pstack Configure the models and panel sizes used by pstack.
```

Setup is optional. Every model role inherits the current session's model by default. Review panels use three independent runs unless configured otherwise. Different model families are used only when the host actually exposes them. Model preferences live in `pstack-models.md` under `CODEX_HOME` (default `~/.codex`) and are read explicitly by the skills.

The upstream explicit-only invocation settings are preserved in each skill's `agents/openai.yaml`. A routed workflow can still read another skill directly by its bundled path. `poteto-mode` persists as a requested style within the conversation; it does not install a native mode switch.

## Workflows

| Skill | Purpose |
| --- | --- |
| `poteto-mode` | Route engineering work through the appropriate playbook. |
| `how`, `why`, `recall` | Understand implementation, rationale, and prior work. |
| `architect`, `arena`, `swarm` | Explore designs, compare candidates, and distribute work. |
| `interrogate`, `no-comments`, `blast-radius` | Review changes and their consequences. |
| `tdd`, `typescript-best-practices` | Guide implementation and behavioral tests. |
| `figure-it-out`, `show-me-your-work` | Drive a complex task and leave evidence. |
| `create-verification-skill`, `maintain-verification-skill` | Build and maintain a project-specific behavior harness. |
| `unslop`, `bro`, `technical-writing`, `teach` | Write and explain clearly. |
| `reflect`, `automate-me` | Capture lessons and working preferences. |
| `make-bot-ui` | Build a server-backed UI for a configured webhook. |
| `setup-pstack` | Configure model preferences without changing native Codex settings. |

The `principle-*` skills retain the upstream engineering principles. The 23 playbooks remain under `skills/poteto-mode/playbooks/`.

## Runtime and dependencies

The [Codex runtime contract](skills/poteto-mode/references/codex-runtime.md) defines delegation, model fallbacks, history access, verification drivers, persistence, and authorization boundaries.

- Subagents use the tools exposed by the current Codex host, bounded by its concurrency limits. Writers get exclusive worktrees or disjoint files. There is no implicit cloud VM. Without subagents, workflows run sequentially and disclose missing independent verification.
- `agents/poteto-agent.md` and `agents/comment-sicko.md` are prompt resources, not registered agent types.
- Browser and CLI verification use available tools or a project harness. No `cursor-team-kit` installation is required.
- History workflows use scoped host history, supplied transcripts, the current conversation, or project checkpoints. They do not search global session storage.
- Long runs require an active session or a separately configured host scheduler. This plugin does not install a scheduler, webhook backend, or automatic restart mechanism.
- GitHub workflows require Git and authenticated `gh`. Optional Origin or Graphite workflows require their respective CLIs; the orchestration store's `frontier set` specifically uses Graphite metadata. Do not use that stack workflow when Graphite is absent.
- The orchestration and PR-watcher scripts require Bun. Their bootstrap installs locked dependencies on first use. The worktree audit also uses Python 3 and `jq`; it accepts an optional workspace-scoped transcript directory and treats missing history as unknown.

A skill does not expand permission to publish, message, merge, or deploy. Existing user authorization and host policies govern those actions.

## Validation

From the repository root:

```bash
python3 -m pip install pyyaml
python3 pstack/scripts/validate-codex.py
python3 -m unittest discover -s pstack/scripts -p 'test_*.py'
python3 pstack/scripts/smoke-codex.py
cd pstack/skills/poteto-mode/scripts
bun install --frozen-lockfile
bun test orch watch-pr
bun run typecheck
```

The Python validator checks manifest resources, skill frontmatter, invocation policy, and local Markdown links. Tests exercise packaging and worktree history behavior. The smoke test installs into a temporary `CODEX_HOME` and checks all 47 skills through Codex's app-server discovery API, without starting a model or modifying your Codex configuration. Structural validation and discovery do not prove agent behavior on real tasks.

## Upstream material and remaining platform integration

The illustrated `docs/guide/` is retained as historical Cursor documentation, not Codex setup instructions. Use this README and the runtime contract for Codex.

The dormant `automations/benny/` pack still targets Cursor's automation service. It is excluded from the Codex package. Its Slack triggers, credential setup, and automation editor handoff need a separate provider integration before Benny can run under Codex. `make-bot-ui` accepts an existing webhook; it does not create that backend.

This fork preserves the upstream MIT license and attribution. See `LICENSE`.
