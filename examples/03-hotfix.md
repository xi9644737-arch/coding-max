# 示例: Hotfix 模式 — 线上紧急修复

## 用户输入

> 线上炸了，支付回调接口全部 500，火烧眉毛赶紧修！

## AI 行为 (Hotfix 模式)

**模式路由** — "线上/紧急/hotfix/炸了" → Hotfix

**诊断:**
- 搜病历: 命中 "2026-07-10 · 支付签名校验失败"
- 5 Whys: 定位 `payment/callback.py:89`，上游支付网关改了回调字段名 `trade_no`→`transaction_id`

**修复:**
- 先用新字段回调取得 RED，再做兼容新旧字段名的最小止血
- 扫描所有回调消费者和签名校验，确认字段归一化位于拥有外部契约的边界

**验证:**
- 复现、相关测试和反事实通过后恢复服务
- 事后补全 `[HOTFIX]` 病历、回滚说明、监控疫苗与 Review

## AI 输出

```python
# payment/callback.py:89 — Hotfix
trade_id = data.get("transaction_id") or data.get("trade_no")
```

```
[HOTFIX] .project-memory/bugs/BUG-YYYY-MM-DD-payment-callback-field.md
- 根因: 上游支付网关字段重命名，未同步通知
- 修复: 兼容 transaction_id 和 trade_no 双字段
- 状态: resolved；终审和临时 trace 清理完成
```
