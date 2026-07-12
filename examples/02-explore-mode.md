# 示例：Explore 模式 — 只诊断不修改

## 用户输入

> 这个项目偶尔在并发场景下死锁，帮我看看可能是什么原因。

## AI 行为（Explore 模式）

仅步骤 1+2+2.5，不改任何代码。

**步骤 1：搜病历** — 无匹配

**步骤 2：初审 + 5 Whys**
- 定位：`order_service.py` 和 `inventory_service.py` 互相持有对方的锁
- 5 Whys 追问 → arch-circular-import 级耦合

**步骤 2.5：插桩**
- 在锁获取/释放点插入 `[BUG-TRACE]` 日志
- 建议用户在并发测试时抓取时序

## AI 输出

```
诊断报告
══════════
根因：order_service 和 inventory_service 在并发路径上形成锁环
- order.create() 持锁 A → 等锁 B
- inventory.deduct() 持锁 B → 等锁 A

建议：
1. 统一锁获取顺序（先 A 后 B）
2. 或加超时机制 try_lock(timeout=5s)
3. 标记 arch-tight-coupling，安排独立解耦迭代

本次未修改任何代码。是否需要我进入修复模式？
```
