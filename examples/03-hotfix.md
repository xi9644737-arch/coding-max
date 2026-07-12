# 示例: Hotfix 模式 — 线上紧急修复

## 用户输入

> 线上炸了，支付回调接口全部 500，火烧眉毛赶紧修！

## AI 行为 (Hotfix 模式)

**模式路由** — "线上/紧急/hotfix/炸了" → Hotfix

**诊断:**
- 搜病历: 命中 "2026-07-10 · 支付签名校验失败"
- 5 Whys: 定位 `payment/callback.py:89`，上游支付网关改了回调字段名 `trade_no`→`transaction_id`

**修复:**
- 冲击波: grep全仓 → `payment/callback.py`(2处) + `order/confirm.py`(1跳间接依赖)，无共享状态
- TDD: RED(测试新字段名→500✓) → GREEN(兼容新旧字段名) → 跳过REFACTOR

**验证:**
- 三层自检: 反事实✓(revert→500重现)
- `[HOTFIX]` 前缀 + 事后待补: 疫苗(字段变更监控) + 胶囊(记录弯路)

## AI 输出

```python
# payment/callback.py:89 — Hotfix
trade_id = data.get("transaction_id") or data.get("trade_no")
```

```
[HOTFIX] 2026-07-12 · 支付回调字段名变更
- 根因: 上游支付网关字段重命名，未同步通知
- 修复: 兼容 transaction_id 和 trade_no 双字段
- 事后待补: 疫苗(接入字段变更监控)、胶囊
```
