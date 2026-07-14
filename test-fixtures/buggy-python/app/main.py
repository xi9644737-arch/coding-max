"""User-management API with three planted defects for coding-max evaluation."""

users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.test"},
    2: {"id": 2, "name": "Bob"},  # BUG-1: legacy record has no email field
    3: {"id": 3, "name": "Casey", "email": "casey@example.test"},
}


def get_user(user_id: int) -> dict:
    """Return a user record."""
    user = users_db.get(user_id)
    if not user:
        return {"error": "not found"}

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],  # BUG-1: user 2 raises KeyError
    }


def update_user(user_id: int, data: dict) -> dict:
    """Update a user — BUG-2: a bare except swallows failures."""
    user = users_db.get(user_id)
    if not user:
        return {"error": "not found"}

    try:
        user.update(data)
        users_db[user_id] = user
        return {"ok": True}
    except:  # BUG-2: catches and swallows every exception
        pass  # The caller cannot observe the failure.


# BUG-3: shared mutable cache without synchronization
_cache: dict = {}


def get_user_cached(user_id: int) -> dict:
    """Return a cached user — BUG-3: the cache path is not thread-safe."""
    if user_id in _cache:
        return _cache[user_id]

    result = get_user(user_id)
    _cache[user_id] = result  # Race window between the read and write.
    return result
