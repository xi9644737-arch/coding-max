# coding-max + coding-pipeline

> Vendor-neutral Agent Skills for root-cause debugging, regression-safe fixes, code review, and test/CI infrastructure recovery.

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-v0.1.3beta-orange">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue">
  <img alt="Skills" src="https://img.shields.io/badge/skills-2-brightgreen">
  <a href="https://skills.sh/xi9644737-arch/coding-max"><img alt="skills.sh installs" src="https://skills.sh/b/xi9644737-arch/coding-max"></a>
</p>

Most debugging prompts stop at “the tests pass.” This package goes further: it finds the first broken contract, proves the fix with a regression, reviews the resulting diff, cleans temporary diagnostics, and records the result so the same failure is easier to solve next time.

`coding-max` is the primary product. When a valuable codebase has no trustworthy test path, its lightweight companion `coding-pipeline` builds or repairs that path, then returns control so `coding-max` can close the bug safely.

## Core skill and verification companion

| Role | Skill | Job |
|---|---|---|
| Core maintenance skill | `coding-max` | Diagnose, repair, verify, review, and retain defect knowledge in high-value codebases |
| Conditional safety net | `coding-pipeline` | Restore tests, CI, coverage, and pre-commit only when reliable verification is missing |

They coordinate through `.project-memory/PHASE.json` only when pipeline work is required. `coding-pipeline` deliberately returns control instead of expanding into a general Agent Harness.

## Quick install

Install both skills with the universal Skills CLI:

```bash
npx skills add xi9644737-arch/coding-max -g --skill coding-max coding-pipeline
```

Or install to an explicit Agent Skills directory without guessing the host:

```bash
git clone https://github.com/xi9644737-arch/coding-max.git
./coding-max/install.sh /absolute/path/to/skills

# Windows PowerShell
# .\coding-max\install.ps1 -Destination C:\absolute\path\to\skills
```

The repository is discoverable as two independent `SKILL.md` packages. The custom installers back up existing copies before replacement.

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

Contract tests cap `coding-max/SKILL.md` at 4 KiB and enforce total package budgets. New capabilities belong in conditional references instead of inflating the always-loaded prompt.

## Evidence, not marketing claims

The repository ships deterministic contract tests and two scenario fixtures:

- `test-fixtures/buggy-python`: root-cause and review behavior against planted defects;
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
