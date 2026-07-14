# Contributing

This repository is mostly Markdown and YAML, but its public contracts, references, templates, and size budgets are covered by automated tests.

## Issues

- Bug report: identify the workflow step that produced incorrect behavior and include a concrete scenario.
- Feature request: explain the missing capability, why it belongs here, and how it can stay progressively disclosed.

## Pull requests

1. Fork the repository.
2. Keep discovery, routing, and hard constraints in `SKILL.md`; place detailed methods in conditional `references/`.
3. Update relevant tests, examples, `CHANGELOG.md`, and `VERSION` for release changes.
4. Run `python -m unittest discover -s tests -v`.
5. Perform a final `coding-max` Review and remove temporary diagnostics.
6. Describe the change, evidence, compatibility impact, and remaining risk in the pull request.

## Style

- Keep instructions compact and executable.
- Do not restate knowledge a capable model already has.
- Every hard constraint should be testable or produce inspectable evidence.
- Preserve progressive disclosure and current package budgets.
- Do not add model, vendor, IDE, MCP, plugin, or agent-orchestration dependencies.
