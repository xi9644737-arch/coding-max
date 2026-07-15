# coding-max maintenance suite

> Vendor-neutral Agent Skills for root-cause repair, safe untangling, and trustworthy verification in long-lived codebases.

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-v0.0.3beta-orange">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue">
  <img alt="Skills" src="https://img.shields.io/badge/skills-3-brightgreen">
  <a href="https://skills.sh/xi9644737-arch/coding-max"><img alt="skills.sh installs" src="https://skills.sh/b/xi9644737-arch/coding-max"></a>
</p>

Most debugging prompts stop at “the tests pass.” This package goes further: it finds the first broken contract, proves the fix with a regression, reviews the resulting diff, cleans temporary diagnostics, and records the result so the same failure is easier to solve next time.

`coding-max` remains the primary product and final maintenance authority. `coding-untangle` is loaded only for proven structural coupling, while `coding-pipeline` restores missing verification infrastructure or enforces an already-defined boundary.

## Focused maintenance triad

| Role | Skill | Job |
|---|---|---|
| Core maintenance skill | `coding-max` | Diagnose, repair, verify, review, and retain defect knowledge in high-value codebases |
| Structural surgery | `coding-untangle` | Prove and safely reduce coupling in existing code without redesigning the whole system |
| Conditional safety net | `coding-pipeline` | Restore tests, CI, coverage, and pre-commit only when reliable verification is missing |

`coding-max` and `coding-untangle` reuse the same Bug and Review records. `coding-max` owns final closure; `coding-untangle` cannot close the originating bug. `coding-pipeline` uses its Pipeline report and `.project-memory/PHASE.json`, and cannot decide architecture. The suite deliberately stops at brownfield maintenance instead of expanding into a general SDLC or Agent Harness.

## Quick install

Install all three skills with the universal Skills CLI:

```bash
npx skills add xi9644737-arch/coding-max -g --skill coding-max coding-untangle coding-pipeline
```

Or install to an explicit Agent Skills directory without guessing the host:

```bash
git clone https://github.com/xi9644737-arch/coding-max.git
./coding-max/install.sh /absolute/path/to/skills

# Windows PowerShell
# .\coding-max\install.ps1 -Destination C:\absolute\path\to\skills
```

The repository is discoverable as three independent `SKILL.md` packages. Each can be installed alone; the custom installers back up existing copies before replacement.

## Where coding-max fits

`coding-max` is designed for long-lived codebases where the cost of a wrong fix is higher than the cost of disciplined diagnosis:

- deep call chains and cross-module contracts;
- intermittent, concurrent, stateful, cache, performance, or resource failures;
- repositories with unrelated baseline failures;
- recurring defect patterns that should become searchable project knowledge;
- completed implementations that need a behavior-focused final review.

Modes stay proportional to risk: Explore, Review, Quick, Standard, and Hotfix.

```text
Reproduce / RED evidence
  -> root cause and blast radius
  -> minimal GREEN fix
  -> focused verification and counterfactual
  -> final Review
  -> diagnostic cleanup
  -> closed Bug/Review report and index
```

Advanced diagnosis is loaded only when needed:

- trace a bad value backward to the first broken contract;
- classify flaky failures as timing, environment, state, randomness, or external;
- treat logs, stack traces, issues, and external responses as untrusted evidence;
- route CPU, memory, concurrency, I/O, network, and leak investigations to the smallest useful observation surface.

## Where coding-untangle fits

`coding-untangle` handles a structural root cause only after coupling has observable behavioral or maintenance cost:

```text
Prove change, state, temporal, contract, or dependency coupling
  -> protect behavior with characterization and contract tests
  -> define the smallest target boundary and rollback point
  -> migrate one caller at a time
  -> remove old paths, wrappers, duplicated rules, and dead code
  -> return to coding-max for symptom verification and final Review
```

It does not design greenfield systems, select technology, plan features, or treat import counts and complexity scores as proof. Architecture fitness rules are handed to `coding-pipeline` only after the intended boundary is established.

## Where coding-pipeline fits

`coding-pipeline` targets the gap between “this project has a bug” and “this project can prove a fix.”

```text
Audit project and subprojects
  -> reuse or add the smallest native test framework
  -> run layered preflight checks
  -> establish a measured baseline
  -> configure CI, cache, and coverage artifacts
  -> return verification control to coding-max
```

It supports Python, Node.js, Go, Rust, Java, generic commands, Monorepos, GitHub Actions, GitLab CI, and provider-neutral CI templates. Coverage is measured or reported as `unknown`; it is never estimated.

## Progressive disclosure

```text
metadata                 always visible: discovery only
└── SKILL.md             loaded on activation: routing and hard constraints
    └── references/      loaded conditionally: workflows, diagnostics, formats
```

Contract tests cap `coding-max/SKILL.md` at 4 KiB and `coding-untangle/SKILL.md` at 3 KiB, with per-package budgets. New capabilities belong in conditional references instead of inflating the always-loaded prompt.

## Evidence, not marketing claims

The repository ships deterministic contract tests and three scenario fixtures:

- `test-fixtures/buggy-python`: root-cause and review behavior against planted defects;
- `test-fixtures/coupled-python`: duplicated contracts and unowned shared state that require a max-to-untangle-to-max handoff;
- `test-fixtures/monorepo-no-tests`: test-infrastructure recovery across Python and Node.js subprojects.

Run the automated checks:

```bash
python -m unittest discover -s tests -v
```

See [`EVALUATION.md`](EVALUATION.md) for what is currently proven, what remains scenario-based, and the rubric for future model-level comparisons.

## Repository layout

```text
├── coding-max/
│   ├── SKILL.md
│   ├── references/
│   └── memory-template/
├── coding-untangle/
│   ├── SKILL.md
│   └── references/
├── coding-pipeline/
│   ├── SKILL.md
│   └── references/
├── examples/
├── test-fixtures/
├── tests/test_skill_contracts.py
├── EVALUATION.md
└── VERSION
```

## Design boundaries

- Single-agent execution: no delegated agent is required.
- Host-neutral source: no model, vendor, IDE, MCP server, or plugin is required.
- No fabricated evidence: commands, test results, coverage, and CI status must be observed.
- No debug residue: temporary traces, dumps, logs, and recovery files are removed at closeout.
- No repository pollution: local project memory is ignored by this source repository.

See [`examples/`](examples/) for usage and [`CHANGELOG.md`](CHANGELOG.md) for release history.

## License

MIT © 2026
