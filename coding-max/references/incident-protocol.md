# Incident runtime protocol

定义状态、动作边界和证据门。生命周期 `investigating -> fixing -> verifying -> resolved|blocked` 与认知状态正交。

## Diagnosis state

`diagnosis_stage` 由病历可复核证据推进；证据失效退回。假设是证据集合，不是状态。

| stage | 进入证据 | 允许动作 |
|---|---|---|
| `unknown` | 只有报告 | 定范围、只读收集 |
| `observed` | 症状/环境已记录 | 建基线；执行复现、采样或受控观测 |
| `failure-confirmed` | 产品 RED 或偶发故障的不变量/采样 | 验证可证伪假设 |
| `localized` | 首次破坏契约处已定位 | 查影响、回滚、替代解释 |
| `cause-confirmed` | 因果证据支持主因，改方案的替代解释已受控 | 过门后永久修改 |
| `regression-proven` | 原复现和相关验证通过；适用时反事实重现故障 | 关闭沉淀 |

条件/边界、微妙因果或非低风险须做反事实/定向变异。`patched` 属于生命周期，`memorized` 属于关闭动作。无法复现不得伪造 `failure-confirmed`；只记录频率/不变量、增强观测或授权止血。

永久 `fixing` 须 `cause-confirmed`、Actionability 通过且无待决 Human Gate；有补丁/止血证据才进 `verifying`；仅 `regression-proven` 且 Gate 清除可 `resolved`。证据写病历复现/根因/验证段，不得只改状态。

## Triage

记录 `blast_radius`、`uncertainty`、`irreversibility`: `low|medium|high`，以及 `migration/security/data/public_contract`: `none|present`；不算总分。三项均 low 且硬风险均 none 为 Quick，否则 Standard。Hotfix 只表示生产伤害正在发生。

## Actionability Gate

永久修改前证明：故障成立；契约 origin 已定位；主因有因果证据；改方案的替代解释已受控；影响、回滚、验证明确；无待决 Human Gate。不得用置信百分比。未通过则调查或按未解停止；只有下列边界触发 Human Gate。

## Human Gate

任一项交权：等价原因导向不同修复；扩大授权；数据迁移；公开契约/兼容策略变化；安全策略、权限、凭据或风险接受；不可恢复/回滚未证明；业务取舍。

```yaml
human_gate:
  required: true
  reason: <trigger>
  decision_needed: <choice>
  safe_state: evidence-preserved
  options: []
  rollback: <proved|unavailable>
  timeout_behavior: stop
```

等待只允许保存证据、只读调查、备选项和预授权可逆止血；禁止扩大范围、迁移、不可逆操作或代选策略。Gate 可从任一活动状态触发；交权或超时写 `blocked`，保持 diagnosis_stage 和决策点。获决定后记录授权、清除 Gate、重查 Actionability。
