# Verify an existing fix

Use this mode when the user asks whether a patch works, or a concrete PR or commit plausibly fixes the reported symptom. Verify that artifact without editing it or opening a competing patch. Report in the current conversation; no tracker or messaging integration is required.

## Qualify the artifact and baseline

Read the patch and connect its changes to the reported behavior. A branch name, ticket status, or claim that something is fixed is not proof.

Record the artifact URL or commit, baseline SHA, patched SHA, exact user path, expected result, observed defect, and shared environment inputs. For an open PR, choose a reproducible baseline from its base history and pin the SHA; confirm it actually exhibits the defect. For a merged fix, normally use the revision before the fix. If that revision cannot run or later changes obscure the comparison, explain the limitation instead of treating a passing patched build as proof.

Use isolated worktrees or clean checkouts. Preserve user edits and give each build its own fixtures, profiles, ports, and data directories, or run them sequentially with a documented reset. Do not switch revisions underneath a running process.

## Measure both builds

Read the project's verification skill and matching feature-map entry when present. Otherwise derive a scoped recipe from the report and app; the [control-adapter contract](../../create-verification-skill/references/control-adapter.md) explains environment and evidence requirements.

1. Start the baseline and verify the app identity, revision, and test environment.
2. Exercise the reported path through the actual user-facing surface. Observe the state that distinguishes the defect from correct behavior. For a repeatable bug, reset and reproduce twice; record both attempts.
3. Save the steps, output or captures, and an appropriate read-only state cross-check.
4. Start the patched build with equivalent environment, data, and observation rules. Reset between runs and execute the same path twice.
5. Confirm that the expected result replaces the broken result. Preserve comparable before-and-after evidence.

For an intermittent or performance defect, choose a repeated workload and a pass criterion before comparing builds. Record attempts, failures, and measurements on both. Two clean attempts alone do not establish that a flaky failure is fixed. Respect the task's work budget; insufficient samples mean inconclusive.

A UI claim requires real UI interaction. CLI and API claims require the real command or supported request. Compilation and unit tests are supporting evidence, not a replacement for the reported path. Label a translated environment and explain why it tests the same behavior; if the missing platform is part of the defect, the exact fix remains unverified.

## Report the outcome

- **Confirmed:** the baseline exhibits the symptom and the patched build meets the predeclared criterion under equivalent conditions. Link the artifact and evidence, with the limits of the comparison.
- **Insufficient fix:** the same symptom remains on the patched build. Return the failing steps and evidence; do not author a competing patch unless the user requests further fix work.
- **Inconclusive:** the baseline cannot reproduce, a build cannot run, the environment differs materially, or observations are insufficient. State the missing half and the next useful check. Do not claim success.

Stop the builds and remove only temporary resources created for this comparison. Retain evidence at its reported location for review; do not commit captures, recordings, credentials, or debug logs by default.
