_history: list[bytes] = []


def process(payload: bytes) -> int:
    _history.append(payload)
    if sum(map(len, _history)) > 1_000_000:
        raise TimeoutError("downstream request timed out")
    return len(payload)


def reset() -> None:
    _history.clear()
