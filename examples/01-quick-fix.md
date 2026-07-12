# 示例：Quick 模式 — 常规 Bug 修复

## 用户输入

> 用户列表接口偶尔返回 500，日志里是 `KeyError: 'display_name'`，帮我修一下。

## AI 行为（coding-max 驱动）

**步骤 0：分级** — 逻辑变更，初审有信号 → Moderate → 走 Quick

**步骤 1：搜病历** — 无匹配病历，继续

**步骤 2：初审** — 定位到 `user_service.py:142`：
```python
def format_user(user):
    return {
        "id": user["id"],
        "name": user["display_name"],  # 某些老用户没有 display_name
    }
```
命名正常、复杂度低(函数 12 行)、同类一致性检查 → `format_user` 被 3 处调用，其余 2 处已用 `.get("display_name", user["username"])`。

**5 Whys:**
1. 为什么报错？→ 老用户数据没有 display_name 字段
2. 为什么没兜底？→ `format_user` 用了直接索引而非 .get()
3. 为什么其他调用方没问题？→ 另外 2 处已经修过同一问题
4. 为什么这处没修？→ 这处是后来新增的调用，没注意到已有模式
5. Why 指架构 → **arch-代码重复**：兜底逻辑分散在 3 处

**步骤 3：TDD**
- RED: 测试 `format_user({"id": 1})` → KeyError ✓
- GREEN: `.get("display_name", user.get("username", "unknown"))`
- REFACTOR: 提取公共函数 `get_display_name()` 统一 3 处调用

**步骤 4：自检**
- 代码层 ✓: 不是 if-else 壳，能解释为什么之前坏
- 思维层 ✓: 无红旗念头
- 反事实 ✓: revert → KeyError 重现

**步骤 5：墓碑** — 无临时调试代码

**步骤 6：验证** — 14/14 测试通过 ✓

## AI 输出

```python
# user_service.py — 修复后
def get_display_name(user):
    return user.get("display_name", user.get("username", "unknown"))

def format_user(user):
    return {
        "id": user["id"],
        "name": get_display_name(user),
    }
```

```
病历：2026-07-12 · display_name KeyError
- 根因：老用户数据缺少字段 + 兜底逻辑分散(arch-代码重复)
- 修复：提取 get_display_name()，3 处调用统一
- 标签：key-error, arch-missing-abstraction
```
