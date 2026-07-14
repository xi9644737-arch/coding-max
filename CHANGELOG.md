# Changelog

> A new Beta release line starts at `v0.1.3beta`. Existing `v1.0.0`, `v1.0.2`, and `v2.0.0` tags remain immutable early-history snapshots.

## [0.1.3beta] - 2026-07-15

### coding-max

- Added a conditionally loaded advanced-diagnostics layer for backward data-flow tracing, flaky-failure classification, untrusted diagnostic input, and performance/resource routing.
- Distinguished the first broken contract (origin) from later propagation points.
- Preserved single-agent, host-neutral execution without model or tool-protocol dependencies.
- Added a 4 KiB contract for the main `SKILL.md` router.

### Distribution and evidence

- Rebuilt the public documentation and examples around the current Explore, Review, Quick, Standard, and Hotfix workflows.
- Added a machine-readable `VERSION` and release-consistency tests.
- Added an English discovery surface, universal Skills CLI installation, scenario evidence, and an explicit evaluation boundary.
- Kept local Bug, Review, and Pipeline records out of the published package.

## Historical snapshots

### [2.0.0] - 2026-07-12

- Expanded the original single skill into the `coding-max` + `coding-pipeline` pair.
- Added early test-infrastructure, CI-template, and PHASE handoff workflows.

### [1.0.2] - 2026-07-12

- Refined root-cause analysis, routing, TDD, review, instrumentation, and Hotfix constraints.
- Expanded Python, Node.js, Go, Rust, and Java test/CI guidance.
- Fixed workflow leakage in discovery metadata, legal-syntax false positives, and dangling references.

### [1.0.0] - 2026-07-12

- Initial `coding-max` release.
- Introduced Explore, Quick, Standard, and Hotfix modes.
- Added RED/GREEN repair, project Bug records, and recovery checkpoints.
