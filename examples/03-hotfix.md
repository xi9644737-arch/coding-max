# 示例：Hotfix 模式 — 线上紧急修复

## 用户输入

> 线上炸了，支付回调接口全部 500，火烧眉毛赶紧修！

## AI 行为（Hotfix 模式）

跳过存档/同模式扫描/血统/Premortem/墓碑/疫苗/胶囊。**保留冲击波。**

**步骤 1：搜病历** — 命中："2026-07-10 · 支付签名校验失败"

**步骤 2：初审** — `payment/callback.py:89`，上游支付网关改了回调字段名 `trade_no` → `transaction_id`

**步骤 3.2：冲击波** — grep 全仓：
- `payment/callback.py` 直接消费(2 处)
- `order/confirm.py` 间接依赖(1 跳)
- 无共享状态影响

**步骤 3：TDD** — RED(测试重现 500) → GREEN(兼容新旧字段名) → 跳过 REFACTOR(线上修完再说)

## AI 输出

```python
# payment/callback.py:89 — Hotfix
trade_id = data.get("transaction_id") or data.get("trade_no")
```

```
[HOTFIX] 2026-07-12 · 支付回调字段名变更
- 根因：上游支付网关字段重命名，未同步通知
- 修复：兼容 transaction_id 和 trade_no 双字段
- 跳过的检查：存档(0.5)、同模式扫描(2)、血统(2)、Premortem(3.1)、墓碑(5)、疫苗+胶囊(7)
- ⚠️ 事后待补：疫苗(接入字段变更监控)、胶囊(记录此次弯路)
```
