# 历史病例检索协议

仅当任务根存在 `.project-memory/BUG_PATTERNS.md` 且当前故障已记录症状时加载。历史病例用于提出待证伪假设，不是当前事件的证据。

## 检索

1. 从当前病历读取 `signature`；未知值保持 `null`，不得用历史值补齐。
2. 先只读 `BUG_PATTERNS.md` 的索引和模式块，不遍历加载全部病历。
3. 忽略含 `null` 的比较，按以下首个命中层选择候选：
   - A：`origin_contract` 与 `failure_mode` 均精确匹配；
   - B：`component` 与 `failure_mode` 均精确匹配；
   - C：`symptom_fingerprint` 与 `environment` 均精确匹配。
4. 同层候选依次按五个 signature 字段的精确匹配覆盖度、最近一次病例日期、pattern ID 排序。只完整加载前 1–3 个不同病例；其他候选只保留索引摘要。
5. 零命中即继续当前事件的独立调查，不扩大加载范围。记录“无历史匹配”而非创建推测关系。

历史材料只能新增可证伪假设和建议检查项，不能单独推进 `localized`、`cause-confirmed`、Actionability Gate 或关闭状态。每个被采用的历史假设都必须由当前代码、当前 RED 或当前因果实验验证；冲突时以当前证据为准。

## 合并与反馈

当前病例达到 `cause-confirmed` 后才评估模式合并。只有当前证据确认相同 `origin_contract` 与 `failure_mode`，且其余 signature 不矛盾时，才向既有 pattern 追加病例与差异；否则新建 stable ID，不因症状相似强行合并。

同根因第二次，或 security/data/public_contract 硬风险病例一次，标记 `prevention_status: candidate`；第三次复发视为 Prevention 失效，改为 `failed` 并提出 invariant test、CI gate 或架构治理。Detection 与 Prevention 必须链接当前证据，不能由频次自动证明有效。
