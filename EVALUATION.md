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
| Package size | Per-skill budgets, 4/3/2.5 KiB ceilings for max/untangle/tombstone entrypoints, and a 50 KiB suite ceiling |
| Repair closure | RED/GREEN, Bug report status, Review index, and report routing remain mandatory |
| Advanced debugging | Backward tracing, flaky classification, untrusted evidence, and performance routing remain reachable on demand |
| Structural handoff | `coding-max` owns Bug closure, `coding-untangle` owns safe structural migration, and `coding-pipeline` only enforces defined boundaries |
| Retirement handoff | `coding-tombstone` owns evidence-backed retirement and Tombstone state, then returns final Review to `coding-max` |
| Pipeline handoff | `coding-max` and `coding-pipeline` share the canonical `.project-memory/PHASE.json` protocol |
| CI templates | Required images, matrices, and syntax guards stay intact |
| Portability | Published skill directories contain no vendor-specific packaging |
| Release consistency | `VERSION`, README, and CHANGELOG agree |

All four skill folders are also checked with the reference Skill validator, while install scripts receive PowerShell and Bash syntax validation before release.

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

### coding-untangle companion fixture

`test-fixtures/coupled-python` contains duplicated normalization rules and shared mutable state with no behavior-owning boundary. A model-level run should be scored on whether it:

1. lets `coding-max` retain ownership of the observable bug and report;
2. proves contract and state coupling instead of citing import counts alone;
3. protects current behavior before structural edits;
4. introduces the smallest rule/state owner and migrates callers incrementally;
5. removes duplicated rules and direct shared-state writes without leaving permanent wrappers;
6. adds the cheapest useful architecture vaccine when justified;
7. returns to `coding-max` for the original symptom check and final Review.

### coding-tombstone retirement rubric

A release-cleanup run should be scored on whether it:

1. classifies candidates as safe-delete, deprecate, retain, or blocked;
2. checks dynamic loading, configuration, packaging, public APIs, and persisted data instead of trusting zero static references;
3. protects the replacement before deletion and retires one rollback-safe set at a time;
4. removes obsolete callers, tests, docs, configs, and compatibility paths without moving code into an archive folder;
5. verifies tests, build/package/install surfaces, and residue searches without inventing remote results;
6. records a searchable Tombstone with a replacement, evidence, rollback, anti-resurrection gate, and target release;
7. routes discovered defects, structural work, and verification gaps to the owning companion Skills.

## Current limitations

- No cross-model success rate has been published yet.
- No dedicated `coding-tombstone` fixture has been published yet; its rubric is contract-tested but still needs retained model-run artifacts.
- Fixture outcomes are not counted as wins unless the full run artifacts are retained and independently reviewable.
- Contract tests prove package integrity, not that every model will follow every instruction.
- GitHub stars and install counts measure distribution, not debugging quality.

Future benchmark reports should publish prompts, model/version, repository commit, commands, diffs, test output, reports, failures, and scoring criteria. Aggregate scores without those artifacts are not accepted as evidence.
