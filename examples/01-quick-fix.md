# 示例: Quick 模式 — 常规 Bug 修复

## 用户输入

> 用户列表接口偶尔返回 500，日志里是 `KeyError: 'display_name'`，帮我修一下。

## AI 行为 (coding-max Quick 模式)

**模式路由** — 逻辑变更，单用户影响面 → Quick

**诊断:**
- 搜病历并取得最小复现
- 从 `KeyError` 反向追踪：失败点是 formatter，直接生产者是旧版用户记录的反序列化边界
- 证明该边界首次违反“展示名可选、用户名必有”的领域契约；formatter 只是传播点

**修复:**
- 影响面：检索同一反序列化入口及所有消费者
- TDD：RED（旧记录读取失败）→ GREEN（在拥有契约的边界归一化）→ REFACTOR（仅消除本次引入的重复）

**验证:**
- 相关测试和反事实通过；全量结果与既有基线分开记录
- 关闭 `.project-memory/bugs/BUG-...md` 并更新 `BUG_PATTERNS.md`

## AI 输出

```python
# 用户记录读取边界 — 修复后
def hydrate_user(record):
    user = dict(record)
    user["display_name"] = record.get("display_name") or record["username"]
    return user
```

```
已关闭: .project-memory/bugs/BUG-YYYY-MM-DD-display-name-contract.md
- 根因: 旧记录进入领域模型时未执行兼容归一化
- 修复: 在数据边界恢复 display_name 契约
- 验证: 回归测试、相关消费者测试、反事实均通过
```
