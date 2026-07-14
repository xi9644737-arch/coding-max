# Evaluation and Evidence

This document separates deterministic evidence from behavior that still requires model-level evaluation. It intentionally avoids claiming a success rate that has not been measured.

## Deterministic contract gates

Run:

```bash
python -m unittest discover -s tests -v
```

The suite verifies:

| Area | Enforced evidence |
|---|---|
| Discovery | Valid `name` and `description` frontmatter |
| Progressive disclosure | Every declared direct reference exists |
| Package size | Per-skill budgets and a 4 KiB `coding-max/SKILL.md` ceiling |
| Repair closure | RED/GREEN, Bug report status, Review index, and report routing remain mandatory |
| Advanced debugging | Backward tracing, flaky classification, untrusted evidence, and performance routing remain reachable on demand |
| Pipeline handoff | Both skills share the canonical `.project-memory/PHASE.json` protocol |
| CI templates | Required images, matrices, and syntax guards stay intact |
| Portability | Published skill directories contain no vendor-specific packaging |
| Release consistency | `VERSION`, README, and CHANGELOG agree |

Both skill folders are also checked with the reference Skill validator, while install scripts receive PowerShell and Bash syntax validation before release.

## Scenario fixtures

### coding-max fixture

`test-fixtures/buggy-python` contains planted contract, exception, and concurrency defects. A model-level run should be scored on whether it:

1. reproduces the target failure before editing;
2. distinguishes the origin from propagation points;
3. adds a regression that fails before the fix;
4. makes the smallest contract-correct change;
5. verifies relevant callers and boundaries;
6. completes Review and removes temporary diagnostics;
7. closes a searchable Bug report without inventing results.

### coding-pipeline companion fixture

`test-fixtures/monorepo-no-tests` represents a Python/Node.js Monorepo where `coding-max` cannot yet prove a safe repair. The companion run should be scored on whether it:

1. discovers both subprojects and their existing commands;
2. reuses existing infrastructure before adding dependencies;
3. establishes low-cost preflight checks;
4. creates independent test/CI paths for each subproject;
5. records measured coverage or `unknown`;
6. updates PHASE state and returns control to `coding-max`.

## Current limitations

- No cross-model success rate has been published yet.
- Fixture outcomes are not counted as wins unless the full run artifacts are retained and independently reviewable.
- Contract tests prove package integrity, not that every model will follow every instruction.
- GitHub stars and install counts measure distribution, not debugging quality.

Future benchmark reports should publish prompts, model/version, repository commit, commands, diffs, test output, reports, failures, and scoring criteria. Aggregate scores without those artifacts are not accepted as evidence.
