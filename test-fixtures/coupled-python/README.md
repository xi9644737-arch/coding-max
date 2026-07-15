# Coupled Python fixture

This fixture models a small brownfield service where two entry points own copies of the same normalization rule and write directly to shared mutable state.

Run:

```bash
python -m unittest discover -s tests -v
```

The API behavior is intentionally inconsistent with the CLI contract. A model-level evaluation should keep the observable bug under `coding-max`, use `coding-untangle` for the structural repair, and return to `coding-max` for final verification and Review.
