# Safe structural untangling

Use when a confirmed defect or repeated maintenance cost points to structural coupling rather than a local implementation error.

```text
Use coding-max to retain ownership of the observable bug. The CLI and API duplicate the same rule and write directly to shared state. Keep the Bug report active, load coding-untangle, protect the current behavior, establish the smallest rule/state owner, migrate one caller at a time, and remove the old paths. If an architecture gate is justified, let coding-pipeline implement only the already-defined rule. Return to coding-max for symptom verification and final Review. Do not push.
```

Expected routing:

1. `coding-max` reproduces and records the observable defect.
2. `coding-untangle` proves the coupling, protects behavior, and performs a reversible migration.
3. `coding-pipeline` is used only if verification infrastructure or a defined fitness gate is missing.
4. `coding-max` verifies the original symptom, reviews the final diff, cleans diagnostics, and closes the report.
