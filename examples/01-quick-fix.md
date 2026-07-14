# Example: Quick mode — routine defect repair

## User request

> The user-list endpoint intermittently returns 500 with `KeyError: 'display_name'`. Fix it.

## Expected coding-max behavior

**Routing** — a localized behavior change with a bounded blast radius → Quick.

**Diagnosis**

- Search existing Bug patterns and obtain a minimal reproduction.
- Trace backward from the formatter failure to the legacy-record hydration boundary.
- Prove that the boundary first violates the domain contract; the formatter is only a propagation point.

**Repair**

- Inspect the same hydration path and all consumers.
- RED: a legacy record fails before the change.
- GREEN: restore the contract at the boundary that owns it.
- REFACTOR: remove only duplication introduced or exposed by this repair.

**Verification**

- Run the reproduction, focused regression, related consumer tests, and a counterfactual.
- Report unrelated baseline failures separately.
- Close `.project-memory/bugs/BUG-...md` and update `BUG_PATTERNS.md`.

## Example output

```python
def hydrate_user(record):
    user = dict(record)
    user["display_name"] = record.get("display_name") or record["username"]
    return user
```

```text
Closed: .project-memory/bugs/BUG-YYYY-MM-DD-display-name-contract.md
- Root cause: legacy records entered the domain model without compatibility normalization
- Fix: restore the display_name contract at the data boundary
- Evidence: regression, related consumers, and counterfactual passed
```
