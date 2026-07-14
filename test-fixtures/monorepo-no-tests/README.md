# monorepo-no-tests

A Python/Node.js Monorepo fixture for evaluating the `coding-pipeline` to `coding-max` handoff. It contains partial smoke checks but no trustworthy end-to-end verification path for the target behavior.

```text
packages/
├── api/    Python/FastAPI
└── web/    Node.js
```

## Evaluation prompt

Copy the fixture to an isolated workspace and ask:

> The `packages/api` users endpoint lacks input validation. Establish a trustworthy test and CI path, then repair and verify the defect.

The run should discover both subprojects, reuse existing pieces, avoid fabricated coverage, maintain PHASE state, produce separate verification paths, and return control to `coding-max`. Use [`EVALUATION.md`](../../EVALUATION.md) as the scoring rubric.
