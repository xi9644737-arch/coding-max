"""用户管理 API — 包含 3 个已知 bug 用于测试 coding-max"""

users_db = {
    1: {"id": 1, "name": "张三", "email": "zhang@test.com"},
    2: {"id": 2, "name": "李四"},  # BUG-1: 缺少 email 字段
    3: {"id": 3, "name": "王五", "email": "wang@test.com"},
}


def get_user(user_id: int) -> dict:
    """获取用户信息"""
    user = users_db.get(user_id)
    if not user:
        return {"error": "not found"}

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],  # BUG-1: user[2] 没有 email → KeyError
    }


def update_user(user_id: int, data: dict) -> dict:
    """更新用户信息 — BUG-2: 裸 except 吞异常"""
    user = users_db.get(user_id)
    if not user:
        return {"error": "not found"}

    try:
        user.update(data)
        users_db[user_id] = user
        return {"ok": True}
    except:  # BUG-2: 裸 except，吞掉所有异常
        pass  # 静默失败，调用方不知道发生了什么


# BUG-3: 全局变量当缓存，并发不安全
_cache: dict = {}


def get_user_cached(user_id: int) -> dict:
    """获取用户（带缓存）— BUG-3: 非线程安全"""
    if user_id in _cache:
        return _cache[user_id]

    result = get_user(user_id)
    _cache[user_id] = result  # 竞态条件：读写之间有窗口
    return result
