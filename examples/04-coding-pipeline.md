# Example: coding-pipeline — restoring a Monorepo test path

## Scenario

A Monorepo contains `packages/web` (Node.js) and `packages/api` (Python), but neither has a trustworthy test path. `coding-max` records `bootstrapping` in `.project-memory/PHASE.json` and hands verification setup to `coding-pipeline`.

## Expected workflow

1. Audit root and subproject manifests, lock files, existing tests, CI, and documented commands.
2. Verify repository-native commands first; add the smallest native framework only when required.
3. Use low-cost preflight checks without copying stale regexes from examples.
4. With authorization, install locked dependencies and obtain a reproducible local baseline.
5. Choose GitHub Actions, GitLab CI, or a provider-neutral template; use a matrix for subprojects and supported toolchains.
6. Record measured coverage or `unknown`, never an estimate.
7. Write the Pipeline report and index, set PHASE to `testing`, and return control to `coding-max`.

## Example output

```text
Verification infrastructure is operational:
- packages/web: test command and CI job verified
- packages/api: test command and CI job verified
- Coverage: measured output recorded; unavailable values are unknown
- PHASE: testing
- Report: .project-memory/pipelines/PIPELINE-YYYY-MM-DD-monorepo.md

coding-max can resume regression verification and final Review.
```
