# Set up pstack for Codex

Install the plugin, optionally choose model preferences, then try a small task. You do not need Slack, an issue tracker, or a separate bot.

## Install the plugin

From a checkout of this repository, follow [Install from this checkout](../../README.md#install-from-this-checkout). That builds a standalone marketplace containing only pstack and installs it with the Codex CLI. Choose a durable output location and keep it while the marketplace is configured. Start a new Codex session after installation.

The installed skills use names such as `$pstack:poteto-mode`. The plugin does not install app-control tools or a background scheduler.

## Choose model preferences when needed

The defaults work without setup: every role inherits the current session's model, and review panels use three independent runs. To change those preferences:

```text
$pstack:setup-pstack configure the models and panel sizes used by pstack
```

[`$pstack:setup-pstack`](../../skills/setup-pstack/SKILL.md) checks the capabilities exposed by your Codex host. It writes `pstack-models.md` under `CODEX_HOME` (default `~/.codex`). This is a pstack-owned Markdown file that skills read on invocation; it does not change Codex's native configuration.

Only confirmed available models can be selected explicitly. If the host cannot select a model per worker, retain inheritance. `auto` is an alias for `inherit-parent`, not a model ID. A panel list has one entry per independent run, including repeated entries. Parallel execution is limited by the host's available slots.

A role without an override keeps its default. Rerunning setup preserves unrelated preferences. Skills read changes on their next invocation.

## Give Codex a way to verify your app

If your project already has a usable harness, keep it. Otherwise:

```text
$pstack:create-verification-skill create a verification skill for this app
```

This generates `.agents/skills/verify-<app>/`, including launch, health-check, driving, evidence, cleanup, and feature-map instructions. It executes one feature end to end before reporting the skill as working. [Verify and ship](./06-verify-and-ship.md#create-a-project-verification-skill) explains the workflow and its examples.

## Run your first task

Pick something real but small:

```text
$pstack:poteto-mode add a --json flag to this command. text output stays byte-identical. verify both. keep the changes local.
```

The skill picks the Feature playbook and tracks its steps in the available plan tool or a Markdown checklist. A skipped step includes its reason.

From here you can use ordinary follow-ups. The workflow continues within this conversation until you change it; it is not a global mode switch.

Next: [Route work through poteto-mode](./02-poteto-mode.md).
