# Example: Hotfix mode — production recovery

## User request

> All payment callbacks are returning 500 in production. Restore service now.

## Expected coding-max behavior

**Routing** — active production incident → Hotfix.

**Diagnosis**

- Search incident history and reproduce with a captured, sanitized callback shape.
- Trace the failure to an upstream field rename from `trade_no` to `transaction_id`.

**Repair**

- Obtain RED using the new field shape.
- Add the smallest compatibility change at the boundary that owns the external contract.
- Scan signature validation and all callback consumers for the same contract.

**Verification and closeout**

- Run the reproduction, focused regression, affected consumer checks, and rollback check.
- Restore service, then complete the `[HOTFIX]` Bug report, rollback notes, monitoring vaccine, and final Review.

```python
trade_id = data.get("transaction_id") or data.get("trade_no")
```

```text
[HOTFIX] .project-memory/bugs/BUG-YYYY-MM-DD-payment-callback-field.md
- Root cause: upstream callback field changed without a synchronized contract update
- Fix: accept transaction_id and legacy trade_no at the integration boundary
- Status: resolved; final Review and diagnostic cleanup completed
```
