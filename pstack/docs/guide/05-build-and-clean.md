# Build the change and clean the diff

The build playbooks share one discipline. Say what you observed, let the playbook demand the evidence. This page shows what to put in the prompt for each common build task, then the cleanup habit that keeps diffs reviewable.

## Prompt each build playbook with what you know

A bug prompt states the symptom and asks for a reproduction first:

```text
$pstack:poteto-mode this command emits two records after a retry. repro first, then fix and verify.
```

A feature prompt states the behavior and what must not change:

```text
$pstack:poteto-mode add a --json flag. text output stays byte-identical. verify both forms.
```

A refactoring prompt pins behavior before structure moves:

```text
$pstack:poteto-mode move parsing into one module, zero behavior change. record the current output first and prove it's unchanged after.
```

A perf prompt states the measurement, not a vibe:

```text
$pstack:poteto-mode startup takes 1.8s on this fixture. trace it, fix the measured cause, show me before and after.
```

Each of these routes to its playbook ([Bug fix](../../skills/poteto-mode/playbooks/bug-fix.md), [Feature](../../skills/poteto-mode/playbooks/feature.md), [Refactoring](../../skills/poteto-mode/playbooks/refactoring.md), [Perf issue](../../skills/poteto-mode/playbooks/perf-issue.md)), and the playbook supplies the steps you didn't type: reproduce before fixing, name the data shape before implementing, pin behavior before restructuring, profile before optimizing.

For sustained improvement of one number, there's the [Hillclimb playbook](../../skills/poteto-mode/playbooks/hillclimb.md). Give it the metric, a target, and a floor on attempts, and it loops one hypothesis at a time with a frozen measurement harness. It keeps wins and reverts everything else.

## Write the failing test first with `$pstack:tdd`

When a bug has a cheap local test path, the whole prompt can be two words:

```text
$pstack:tdd implement
```

In context, that's enough. [`$pstack:tdd`](../../skills/tdd/SKILL.md) writes the smallest test that fails for the intended reason, then the fix, then reruns the test. If a test would need broad harness setup or brittle mocks, the skill says so and uses the closest executable check instead. Don't force a test where a real command is stronger evidence.

## Apply the TypeScript guidance

Invoke `$pstack:typescript-best-practices` when you want its TypeScript guidance, or let a routed workflow read it. It covers discriminated unions, `unknown` at boundaries, exhaustive variants, and schema-derived types. This port does not register a file-extension trigger; opening a `.ts` file alone does not load it.

## Clean before you commit

The [Opening a PR playbook](../../skills/poteto-mode/playbooks/opening-a-pr.md) reviews the diff before each commit and applies [`$pstack:unslop`](../../skills/unslop/SKILL.md) to the PR description and commit bodies. The code cleanup removes unsupported guards, dead compatibility paths, debug output, and unrelated edits. It needs no separate cleanup plugin.

For prose, `$pstack:unslop` takes a target and any extra rules you have:

```text
$pstack:unslop the readme changes, no emdashes
```

You'll develop your own shorthand. The skill reads intent fine from terse prompts like `unslop that, tighten it`.

## Strip the comments with `$pstack:no-comments`

Comments need their own pass, and not from the agent that wrote them. An author defends its comments the way you'd defend yours. So before review, hand them to fresh eyes:

```text
$pstack:no-comments the diff
```

[`$pstack:no-comments`](../../skills/no-comments/SKILL.md) uses [Comment Sicko](../../agents/comment-sicko.md) as the prompt for a read-only reviewer when delegation is available. The reviewer has a short keep list: license headers, doc comments on a public API, links that explain what code can't, behavior forced by an external dependency you can't reshape. Everything else goes. A surprise in your own code gets no such pass. The comment comes back as a refactor flag, and `$pstack:no-comments` fixes the flags it accepts at the root cause. When a comment claims a constraint, "do not remove", the skill offers to encode the claim as a type, test, or lint. Either way, the comment comes out.

The diff review handles code cleanup, `$pstack:unslop` handles prose, and `$pstack:no-comments` focuses on comments. A sequential fallback must disclose that its review was not independent.

**Pitfall:** cleanup is not optional polish. A diff with narrating comments and defensive dead weight reads as unfinished to reviewers, and the extra code is where the next bug hides. If the diff feels padded, ask for a diff cleanup before you commit, not after review calls it out.

Next: [Verify and ship](./06-verify-and-ship.md).
