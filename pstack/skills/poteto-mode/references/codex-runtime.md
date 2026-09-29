# Codex runtime contract

This is the shared runtime for pstack's Codex skills. Resolve paths relative to the loaded skill file, not the working directory. The plugin root is three directories above this file. Read sibling skills by their paths when a routed skill is not in the discovery list. Invoke plugin-installed skills by their catalog names, such as `$pstack:poteto-mode` and `$pstack:arena`. Standalone copies may use unprefixed names. Use only tools and agent types exposed by the current host.

## Delegation and models

Use the subagent tools actually exposed in the current session. Common hosts expose `spawn_agent`, `send_input`, and `wait`; others expose `spawn_agent`, `send_message`, `followup_task`, and `wait_agent`. Read their schemas. These names are examples, not a command shim. Do not pass undeclared parameters or invent tools.

- Agents normally share the filesystem. Give each writer an exclusive worktree or disjoint output paths. A subagent is not automatically a cloud VM or an isolated checkout. Explicitly put the worktree path and base SHA in its brief.
- For the poteto-agent role, have the worker read `agents/poteto-agent.md` from the plugin root. For Comment Sicko, have it read `agents/comment-sicko.md`. These are prompt resources, not registered Codex agent types. Other roles use the prompt templates named in their skills.
- A read-only brief prohibits writes; it does not change tool availability or grant permissions. Check the worker's actual tools before assigning MCP work. Keep credentials out of briefs.
- Bound concurrency by the session's available slots and nesting limits. Queue excess work and refill as workers finish. Never assume all requested workers can start together.
- When delegation is unavailable or forbidden, carry out the phases sequentially yourself. Keep separate candidate artifacts where the workflow calls for alternatives. Report that independent review was unavailable; a self-review is not an independent verdict. Do not merge behind a gate that requires independent verification.
- Use status/wait tools for liveness, follow-up tools only for new work, and close or interrupt tools when supported. Inspect results and reconcile changes before accepting them. Do not claim a worker stopped without confirmation.

Read model preferences, when present, from `pstack-models.md` in `CODEX_HOME` (default `~/.codex`). This is a pstack-owned Markdown file explicitly read by the skills, not a Codex configuration file or an automatically applied rule.

Every role defaults to `inherit-parent`. Panels default to three independent runs on the parent model; design tasks still need at least two structurally different candidates. `auto` is an alias for `inherit-parent`. For either alias, omit model and reasoning overrides. A panel list's length sets its seat count, including repeated entries.

An explicit model override must be a model the current host confirms is available and must use the tool's actual schema. Read an optional `<role> reasoning: <effort>` preference for that override. Apply it only when the host supports the specified effort separately from the model; never append an effort suffix to a model ID. Inheritance aliases ignore effort overrides. In a host where overrides require a fresh context, use that context option and provide a complete brief. An unavailable or rejected override falls back once to the parent model, with a disclosed substitution. No model guessing or retry ladder. If the user requires cross-model review and only one model is available, report the missing capability before claiming that requirement satisfied.

## Questions, plans, and persistence

Use the available plan tool or a short Markdown checklist. For user questions, use the exposed input tool with its supported schema, or ordinary chat if no such tool is available. Do not rely on multi-select or confirmation-card parameters unless advertised.

An active session can monitor a yielding shell process or wait for a worker. Use the supplied watcher as the event source, poll through the host's process API, and keep updates responsive. A plugin does not provide a scheduler or keep Codex alive after the session exits. For unattended continuation use only an actually available, explicitly configured host scheduler. Otherwise checkpoint the predicate, worktree, progress, and resume command before ending. Do not promise an overnight wake or an automatic restart. A goal is created only when the user requests one and the host supports it; an exit-condition checklist needs no goal tool.

Store durable program state at a task-specific path in the repository's Git common directory (resolve with `git rev-parse --git-common-dir`), for example `pstack/orchestrate/<project>`. Pass that absolute path to workers and `orch --store`. Remote workers, if independently available, need reachable artifacts rather than local paths.

## History and verification tools

Use the current conversation, an explicitly supplied transcript, a host-provided scoped history tool, or a project checkpoint. Verify the workspace and session identity before reading history. Do not search global Codex sessions or other projects' chats. If history is unavailable, use a digest of the current conversation or ask for the relevant prior context. Never assume a transcript path or JSONL schema. Worktree audits accept an optional workspace-scoped transcript directory; missing history is unknown, not evidence of inactivity.

For skill authoring, use `$skill-creator` when installed. Otherwise create `SKILL.md` with `name` and `description`, preserve relative resources, and validate the frontmatter. Project skills live under `.agents/skills/`; personal skills under `~/.agents/skills/` or the host's configured skills directory. Preserve explicit invocation settings in `agents/openai.yaml` via `policy.allow_implicit_invocation: false`; normal discovery is the default.

For browser/UI verification, use the available browser, computer-use, Playwright, or project harness. For CLIs, use shell/PTY tools and observable output. Select a driver that exists and prove the user-visible behavior. If no driver exists, create a project verification skill or report the concrete missing capability.

Before a commit, inspect the diff for unnecessary abstractions, dead code, debug output, and unrelated edits, and run the repository's relevant checks. This replaces the upstream `deslop` dependency. Use the bundled no-comments and unslop workflows where the playbook calls for them.

## Scope and external actions

Follow the user's request, repository instructions, and host permissions. A playbook does not grant permission to message others, publish, merge, deploy, alter approvals, or widen the task. Reuse existing authorization and complete reversible preparation first. Open a PR only when the task calls for one. In an investigation, return findings without creating a branch or PR. Persistent mode means continuing the requested style in the current conversation until the user opts out; it is not a native mode toggle or a cross-session setting.
