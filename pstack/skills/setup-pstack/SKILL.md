---
name: setup-pstack
description: Configure pstack's Codex model preferences and review panel sizes. Use for $pstack:setup-pstack, configuring pstack models, or changing reasoning budgets.
---

# Setup pstack

Read the [Codex runtime contract](../poteto-mode/references/codex-runtime.md). Write pstack's optional `pstack-models.md` in `CODEX_HOME`, default `~/.codex`. Do not edit Codex's `config.toml`.

1. Inspect the current session's subagent schema and any available model catalog. Record whether delegation, model selection, and reasoning overrides are supported. Do not infer entitlement from a model's name or the plugin's examples.
2. Read the existing preference file if present. Preserve existing choices unless the user wants to change them.
3. Present the current choices. Offer parent-model inheritance as the working default; explicit overrides may only use confirmed available model IDs. Ask about panel size or effort only when the user's request leaves a material choice open. If no model catalog is exposed, keep inheritance. Model IDs and effort are separate fields, not combined slugs.
4. Write the file with one role per line. Single roles take a model ID or `inherit-parent`. Panel roles take comma-separated entries. Repeated entries create independent seats. Omit effort lines to inherit; for explicit supported model overrides use `<role> reasoning: <advertised effort>`. Inheritance aliases ignore effort overrides. Show any substitutions before writing. Preserve unrelated roles during a partial update; remove retired roles only with an explanation.

Default file:

```text
# pstack model preferences
# Read explicitly by pstack skills; not native Codex configuration.
feature, refactoring: inherit-parent
bug-fix: inherit-parent
perf-issue: inherit-parent
hillclimb: inherit-parent
judgment and prose: inherit-parent
hardest tasks: inherit-parent
how explorer: inherit-parent
how explainer: inherit-parent
why investigators: inherit-parent
why synthesizer: inherit-parent
reflect tooling: inherit-parent
reflect judgment, divergent, synthesizer: inherit-parent
arena runners: inherit-parent, inherit-parent, inherit-parent
arena cross-judge pool: inherit-parent
swarm workers: inherit-parent
architect runners: inherit-parent, inherit-parent, inherit-parent
interrogate reviewers: inherit-parent, inherit-parent, inherit-parent
```

5. Read back the file and report its path, chosen panel sizes, and unsupported features. Skills read it on their next invocation; no automatic global-rule registration is needed.
6. If the project lacks a way to exercise real behavior, mention `$pstack:create-verification-skill` as an optional next step.
