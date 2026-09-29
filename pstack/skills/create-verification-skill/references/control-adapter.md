# Control-adapter contract

Use this contract when writing the Launch, Doctor, Drive, Evidence, and Cleanup sections of a project verification skill. An adapter is the available browser, computer-use tool, shell, HTTP client, or project harness plus instructions for this app; it is not a new tool supplied by pstack.

Keep the app-specific instructions in `.agents/skills/verify-<app>/SKILL.md` and the feature map under `features/`. The [feature-map checklist](feature-map.example.md) adds states, reset steps, and evidence requirements to the [worked directory example](feature-map-example/README.md).

Inspect capabilities before a run. Use only real exposed tools and their schemas. For a one-off bug, derive a scoped recipe from the app and report rather than requiring a complete map first. When a project map exists, read its matching entry and check it against the app.

## Test environment and work budget

Record the baseline revision, start command, readiness check, test account or fixture, isolated ports and data paths, reset procedure, and artifact directory. Keep credentials in the existing environment or secret store, never in a committed map. Do not introduce a separate configuration service.

Use the user's time or attempt budget when specified. Otherwise choose a bounded first pass appropriate to the task and report the chosen limit. Track failed startup attempts separately from attempts to reproduce the bug. At the limit, return what was tried, evidence, the missing capability or unresolved hypothesis, and a concrete next step. Do not retry indefinitely or weaken the success condition.

Requirements depend on the surface and the claim: a CLI needs command/output/exit-status proof; a UI needs actual interaction; a service needs real requests and responses. A missing required capability blocks that claim, not unrelated checks that remain useful.

## Capabilities to document

### Bring up

Start the requested app revision in the requested test environment.

Input:

- Repository and revision
- Build or start mode
- Workspace, account, fixture, and feature-state requirements
- Artifact directory
- Completed feature-map path or scoped reproduction recipe

Return:

- Session identifier
- How the adapter confirmed the correct app and environment
- Stable app markers
- Running process or target details needed by later calls
- Any missing capability

The adapter must distinguish the target app from a similar window, shell, or production instance.

### Drive the user-facing surface

For a UI, perform real user actions:

- Click
- Type
- Press keys
- Scroll
- Drag
- Resize
- Navigate through app controls

Prefer roles, labels, and stable selectors. Use coordinates only after a fresh screenshot.

For a CLI, invoke the real command and record stdout, stderr, and exit code. For an API or service, use its supported interface and record the request and response. A UI report must still be reproduced through the UI; an API check alone is not equivalent.

Return each action and the observed state change.

Do not set internal state, call hidden app methods, write directly to storage, or inject DOM changes to create the symptom.

### Drive mapped features and states

Read the relevant feature-map section before driving the app, or use the scoped recipe for a one-off run.

For the mapped features in scope, the adapter must expose ways to:

- Navigate every mapped feature through the user-visible path.
- Invoke the adapter action names listed for that feature.
- Interact with default, hover, focus-visible, active, disabled, loading, empty, error, selected, open, expanded, and feature-specific states when they apply.
- Arrange a state through safe fixture data, permissions, flags, service responses, or supported test controls.
- Reset the feature for a second independent repro attempt.
- Capture the evidence and read-only cross-check named by the feature map. Report required evidence that the environment cannot provide.

Use roles, accessible names, ARIA relationships, stable component markers, and purpose-named data attributes. Never use generated CSS or StyleX classes, dynamic hashes, child indexes, or brittle DOM position.

Arranging a precondition is not permission to inject the reported symptom. The repro itself must still come from real user interaction.

### Inspect state

Read state to confirm the user-visible result.

Examples:

- Accessibility tree
- DOM or view hierarchy
- Process state
- Local logs
- Network request status
- App-exposed debug state

Inspection is read-only. If a query changes state, it belongs in the driving procedure and must represent a supported user action.

### Screenshot

For a UI proof, capture the current app state to a requested path.

Return:

- File path
- Capture time
- App marker or window title
- Short description of what should be visible

The screenshot must show enough app chrome to prove that the correct app is under test.

### Recording

Use a screen recording when motion, timing, or a transient symptom makes it necessary to judge the result. Otherwise an action trace and before/after captures can be enough. State a recording capability gap when it prevents the required proof; do not block CLI or API work on video.

When recording, start and stop around the full repro path.

Return:

- File path
- Start and stop times
- Captured window or region
- Whether audio or sensitive overlays were omitted

The recording must show the discriminating final state, not only setup or a loading screen.

### Cleanup

Stop processes and sessions created by the adapter.

Remove disposable:

- Browser or app profiles
- Temporary workspaces
- Test accounts or fixtures when the adapter created them
- Debug ports and tunnels

Return what was stopped, removed, retained, or left for a person.

Cleanup must not delete user work or the evidence being reported. Retain captures at a named location for review; apply any configured retention policy separately from process and fixture teardown.

## Adapter behavior

The adapter must:

- Report capabilities before the repro starts.
- Report which feature-map sections it can drive and which are blocked.
- Use the same environment inputs for baseline and patched builds.
- Surface startup failures as failures.
- Bound retries.
- Keep secrets out of logs and artifacts.
- Keep captures outside the repository.
- Support a fresh or reset state between the two repro attempts.
- Avoid production changes unless the user explicitly configured a safe test action.

## Environment translation

Before declaring an environment block, restate the defect without platform-specific nouns and ask whether the same behavior can be tested safely in the available environment.

Examples:

- A named browser may mean any external browser.
- A named key may mean the configured shortcut.
- A named remote host may mean a delayed or disconnected remote target.

Use a translated attempt only when it tests the same underlying behavior. Label it as translated evidence. Do not call it an exact repro when the missing environment is part of the defect.

Hardware prompts, operating-system permission dialogs, device-only APIs, and unavailable account states may be real blocks.

## Setup check

Before reporting a generated verification skill as working, run one disposable check:

1. Bring up the app.
2. Confirm the stable app marker.
3. Load one completed feature-map section.
4. Navigate to that feature through its user path.
5. Exercise one disposable state through mapped adapter actions.
6. Inspect the resulting state.
7. Capture a screenshot.
8. Record a short clip if required by the feature's proof; otherwise capture an action trace.
9. Clean up.

For CLI or API skills, substitute the actual command or request and response for UI navigation and captures. Confirm evidence survives cleanup. Report the generated skill as working only after the applicable steps succeed; otherwise identify it as an unverified draft.
