# Example: Explore mode — diagnosis without modification

## User request

> This project occasionally deadlocks under concurrency. Investigate the likely cause.

## Expected coding-max behavior

**Routing** — investigation requested without authorization to modify → Explore.

**Diagnosis**

- Search existing Bug patterns.
- Trace the lock paths in `order_service.py` and `inventory_service.py`.
- Confirm that one path holds lock A while waiting for B and the other holds B while waiting for A.
- Identify inconsistent lock ordering as the direct cause and cross-module lock ownership as an architecture risk.
- Describe the temporary `[BUG-TRACE]` observation points that Standard mode could add; do not edit code or project memory in Explore.

## Example output

```text
Diagnosis

Root cause: opposite lock acquisition order creates a cycle.
- order.create(): holds A -> waits for B
- inventory.deduct(): holds B -> waits for A

Recommended Standard repair:
1. Enforce one lock acquisition order.
2. Add bounded acquisition/timeout behavior only if the contract requires it.
3. Record arch-coupling for a separate decoupling decision.

No code or project memory was modified.
```
