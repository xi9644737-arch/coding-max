# 示例: Quick 模式 — 常规 Bug 修复

## 用户输入

> 用户列表接口偶尔返回 500，日志里是 `KeyError: 'display_name'`，帮我修一下。

## AI 行为 (coding-max Quick 模式)

**模式路由** — 逻辑变更，单用户影响面 → Quick

**诊断:**
- 搜病历: 无匹配
- 5 Whys → 定位 `user_service.py:142`: `user["display_name"]` 直接索引，老用户缺少此字段
  1. 为什么报错？→ 老用户无 display_name
  2. 为什么没兜底？→ 直接索引而非 .get()
  3. 为什么其他调用方没问题？→ 另外2处已修过同一问题(用 .get 兜底)
  4. 为什么这处没修？→ 后来新增的调用，没注意到已有模式
  5. Why指架构 → **arch-代码重复**: 兜底逻辑分散在3处

**修复:**
- 冲击波: grep → `format_user` 被3处调用，2处已用 .get()，1处裸索引
- TDD: RED(测试缺字段用户→KeyError✓) → GREEN(`.get("display_name", user.get("username", "unknown"))`) → REFACTOR(提取 `get_display_name()` 统一3处)

**验证:**
- 三层自检: 代码层✓(非创可贴) / 思维层✓(无红旗) / 反事实✓(revert→KeyError重现)
- 全量: 14/14测试通过
- 病历: `2026-07-12 · user_service.py:142 KeyError — 老用户缺字段+兜底逻辑分散(arch-代码重复)`

## AI 输出

```python
# user_service.py — 修复后
def get_display_name(user):
    return user.get("display_name", user.get("username", "unknown"))

def format_user(user):
    return {"id": user["id"], "name": get_display_name(user)}
```

```
病历: 2026-07-12 · display_name KeyError
- 根因: 老用户数据缺少字段 + 兜底逻辑分散(arch-缺失抽象)
- 修复: 提取 get_display_name()，3处调用统一
- 标签: key-error, arch-missing-abstraction
```
