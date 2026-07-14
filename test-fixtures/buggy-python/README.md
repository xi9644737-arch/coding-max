# buggy-python

A small Python fixture for evaluating `coding-max`. It contains three planted defects and only a static smoke-test layer, not behavior regressions for the defects.

## Planted defects

| # | Location | Type | Trigger |
|---|---|---|---|
| 1 | `app/main.py` | Contract/KeyError | Call `get_user(2)`; the legacy record has no `email` |
| 2 | `app/main.py` | Swallowed exception | Exercise an update path that raises inside the broad handler |
| 3 | `app/main.py` | Concurrency risk | Access the shared `_cache` from concurrent callers |

## Evaluation prompt

Copy the fixture to an isolated workspace and ask:

> This user-management module has incorrect behavior. Diagnose and repair it with coding-max.

Score the run using [`EVALUATION.md`](../../EVALUATION.md). Do not count a run as successful merely because it finds all planted comments; the agent should reproduce behavior, trace the owning contract, add regressions, and close the reports.
