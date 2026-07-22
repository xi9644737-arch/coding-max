# Adversarial evaluation

This suite evaluates behavior, not prompt-text presence. The operator gives the tested agent only one file from `cases/` and a copy of its declared `workspace/`. Files under `ground-truth/` and `rubric.json` remain evaluator-only.

For every run, retain the case id, model/version, repository commit, prompt, commands, transcript, diff, test output, Bug/Review reports, elapsed time, and rubric decision. A run with a fatal failure scores zero even when tests pass. Do not publish aggregate success rates without the retained run artifacts.

The suite does not invoke a model or grant repository authority. It defines isolated inputs and evaluator contracts so different hosts can run the same cases without coupling `coding-max` to an Agent harness.

## Protocol

1. Copy the selected workspace to a clean temporary repository.
2. Record the dirty/test baseline before sending the public prompt.
3. Expose only the public case and copied workspace to the tested agent.
4. Retain the complete run artifact set.
5. Run the evaluator commands from the matching ground-truth file.
6. Apply fatal failures first, then score the five weighted metrics.

The three initial cases target misleading diagnostics, unrelated baseline failures, and non-functional regression blindness.
