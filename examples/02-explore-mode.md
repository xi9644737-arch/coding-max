# 示例: Explore 模式 — 只诊断不修改

## 用户输入

> 这个项目偶尔在并发场景下死锁，帮我看看可能是什么原因。

## AI 行为 (Explore 模式 — 不改代码)

**模式路由** — "看看/排查/分析" → Explore

**诊断:**
- 搜病历: 无匹配
- 5 Whys: 定位 `order_service.py` + `inventory_service.py` 互相持有对方锁
  1. 为什么死锁？→ order.create()持锁A等锁B，inventory.deduct()持锁B等锁A
  2. 为什么锁顺序不一致？→ 两个模块独立开发，没有统一锁约定
  3. Why指架构 → **arch-tight-coupling**: 两个服务在并发路径形成锁环

- 插桩: 在锁获取/释放点插入 `[BUG-TRACE]` 日志(时间戳+线程ID+锁名+等待时长)

## AI 输出

```
诊断报告
══════════
根因: order_service 和 inventory_service 在并发路径上形成锁环
- order.create() 持锁A → 等锁B
- inventory.deduct() 持锁B → 等锁A

建议:
1. 统一锁获取顺序(先A后B)
2. 或加超时机制 try_lock(timeout=5s)
3. 标记 arch-tight-coupling，安排独立解耦迭代

本次未修改任何代码。是否需要我进入修复模式？
```
