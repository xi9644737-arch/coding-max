# 诊断与修复流程

Explore 只调查并输出；修复执行全部步骤。状态、风险和交权由 `incident-protocol.md` 定义。

## 1. 观察与定位

记录任务根、dirty baseline、既有失败和最小复现；修改前建 `investigating` 病历（Hotfix 可后补）。读入口、调用链、配置和测试；按症状/组件/根因标签检索 `BUG_PATTERNS.md`，历史只能生成假设。

列最多三个可证伪假设，从失败点追到首次破坏契约处并扫描相邻模式。跨层污染、偶现或性能/资源故障读 `advanced-debugging.md` 的匹配分支，不要加载无关工具。必要时加 2–4 个 `[BUG-TRACE]`，复现后删除。

核对调用方、数据/错误格式、配置和外部接口，检查三个边界（含非 happy path）。Standard 永久修改前读 `patch-signals.md` 做 Premortem。Actionability 通过且无待决 Human Gate 才能永久修改。

## 2. RED / GREEN

证据分级：**产品 RED** 失败在目标产品断言；**合同构建门**（import/collection/compile/schema）只证明能力表面缺失；**harness failure**（barrier、timeout、fixture、清理、钩子）先修测试设施。只把改变方向的被拒证据写入胶囊。

并发、时序、偶发或资源边界须连续三次同型产品断言失败；普通确定性缺陷不机械三跑，复跑一次即可。无法稳定复现则用协议认可的采样/不变量证据，永久修复前仍须取得失败的回归疫苗。然后最小 GREEN；不能自动化则记录命令、输入、预期和实际。Hotfix 可先做预授权可逆 mitigation，但病历保持活动；架构根因只止血并标 `arch-*`，除非获准重构。

## 3. 验证与关闭

按真实契约检查异常、默认值、资源、并发、调用方和无关改动；运行复现、相关测试及允许的全量检查，条件/边界 Bug 做定向变异或反事实。

仅满足 incident protocol 的 `regression-proven` 可判 resolved；无关基线失败只列出。仅新失败或同一未解假设计 strike，三次写恢复点并停止。无测试且风险不低时调用 `coding-pipeline`。

按病历格式补全根因、修复、验证、回滚、回归疫苗和胶囊；关闭状态，更新/合并 `BUG_PATTERNS.md`，删除诊断残留。
