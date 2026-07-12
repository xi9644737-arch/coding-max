# 病历格式 + 疫苗映射 + 同义扩展

## 病历记录 (步骤9自动提取)

### 自动提取 (默认)
```bash
git diff --stat HEAD~1 | tail -1     # "3 files changed, 12 insertions(+), 5 deletions(-)"
git log -1 --format="%s"              # "fix: KeyError when user missing email field"
```
生成摘要: `2026-07-12 · main.py:19 KeyError — 用户缺少email字段时get_user崩溃`

### 手动格式 (自动提取失败时)
```markdown
### YYYY-MM-DD · <简短标题>
- 症状: <原始描述或报错摘要>
- 根因: <5 Whys 得出的根本原因>
- 根因类型: 代码层面 / 架构层面
- 修复: <具体改动，可引用commit hash>
- 文件: <修改文件+行号>
- 环境: <语言版本/OS/关键依赖>
- 标签: <逗号分隔关键词>
- 迭代次数: <1~3>
```

## 标签词汇

### 代码层面
```
异常:   bare-except, swallowed-exception, type-error, key-error
并发:   race-condition, deadlock, thread-safety
资源:   memory-leak, connection-leak, file-not-closed
输入:   sql-injection, xss, path-traversal, no-validation
逻辑:   off-by-one, null-check, boundary, infinite-loop
```

### 架构层面 (arch-前缀，≥3触发警告)
```
耦合:   arch-coupling, tight-coupling, circular-import
结构:   wrong-layer, god-module, missing-abstraction
边界:   leaky-interface, cross-module-side-effect
```

## 架构负债警告 (步骤9，自动触发)

同一arch-标签≥3次→输出:
```
⚠️ 架构负债警告
标签 "circular-import" 已出现 3 次:
  - 2026-07-01: 回路.py
  - 2026-07-08: 引擎.py
  - 2026-07-12: 连接器.py
建议: 安排独立的架构重构迭代，而非继续逐条修复。
```

## 写入规则

- **yes**: 追加末尾，留一空行
- **merge**: 关键词≥2匹配→追加 `### 补充 (日期) ...`
- **no**: 不写入

## 胶囊格式 (步骤9)

追加在BUG报告末尾:
```markdown
## 胶囊
- 弯路: 一开始以为是X，花了N次尝试才排除
- 突破: 读了Y模块的调用方才意识到真正原因
- 误导: Z日志指向了错误方向
- 重来: 如果再修一次，会先grep调用方再下手
```
≥1项。全是"无"=没认真反思。

---

## 同义扩展映射 (步骤1搜病历用)

| 症状聚类 | 口语 | 搜索关键词 |
|---------|------|-----------|
| 崩溃/退出 | 炸了/挂了/崩了/闪退/进程没了 | crash, panic, segfault, exit, signal |
| 卡住/无响应 | 卡死/不动了/转圈/冻住 | hang, freeze, deadlock, timeout, block |
| 慢 | 龟速/吃不消/跑不动 | slow, timeout, O(n²), latency, bottleneck |
| 内存爆了 | OOM/吃内存/内存泄漏/越跑越大 | memory leak, OOM, heap, RSS, GC thrash |
| 数据错了 | 不对/丢了/脏数据/凭空出现 | wrong result, data loss, corruption, stale |
| 不生效 | 没用/没反应/跟没改一样 | no-op, config not loaded, cache not invalidated |
| 偶发/重现不了 | 时好时坏/有时候/我这儿好的 | intermittent, flaky, race condition, heisenbug |
| 以前好的现在坏了 | 老版本没事/升级后/回退了 | regression, bisect, git bisect |
| 循环依赖 | 互相import/蛋鸡问题/套娃 | circular import, cycle, dependency loop |
| 配置不生效 | 改了没用/环境不对/路径不对 | config, env, path, precedence, override |

---

## 疫苗映射表 (步骤9，根因→lint/CI规则)

| 根因类型 | Python | TypeScript | Go | Rust | Java | 通用 |
|---------|--------|-----------|-----|------|------|------|
| null-check遗漏 | mypy strict | strictNullChecks | nilaway | `Option<T>` clippy | NullAway/SpotBugs | 关键入口断言 |
| bare-except | ruff BLE001 | no-unsafe-catch | errcheck | clippy bare_trait_objects | PMD AvoidCatchingThrowable | grep禁止裸catch |
| 竞态条件 | — | — | `-race` flag | `cargo test -- --test-threads=1` | JCStress | CI重复压测 |
| SQL注入 | bandit B608 | eslint no-sql-injection | sqlcheck | sqlx prepared | SpotBugs SQL_INJECTION | 参数化查询 |
| 循环导入 | `python -c 'import <m>'` | madge --circular | `go mod graph` | `cargo tree --invert` | JDepend | CI导入检查 |
| 资源泄漏 | ruff PL | no-unsafe-finally | defer检查 | `Drop` trait clippy | try-with-resources | with/try-with-resources |
| 边界遗漏 | hypothesis | fast-check | fuzzing | proptest | jqwik | property-based test |

---

## 架构最小止血范例 (步骤6，arch-根因用)

⚠️ 这些是**止血**，不是修复。每条打arch-标签，≥3触发架构负债警告。

| 异味 | 最小止血 | 真正的重构(独立任务) |
|------|---------|---------------------|
| 循环依赖 | 延迟导入(⚠️运行时炸→推迟了而已) | 抽取共同接口/依赖倒置 |
| 层级混乱 | 加参数校验+明确错误，不搬业务逻辑 | 分层重组 |
| 上帝模块 | 加类型校验和边界检查，不拆分 | 按职责拆模块 |
| 缺少抽象 | 只修触发点，不改其余N-1处重复 | 抽取公共函数/基类 |
| 紧耦合 | 薄适配函数(1-3行) | 引入接口/DI |
| 改动扩散 | 修触发模块，其余加防御性校验(不改逻辑) | 消除隐式依赖 |
| 接口泄漏 | 调用处加字段筛选/过滤 | 重新设计接口契约 |

---

## 断点格式 (`.project-memory/.resume.md`)

3-Strike硬停时写入:
```yaml
---
bug_id: BUG-YYYY-MM-DD-<slug>
strikes: 2
last_step: 1.2
last_perspective: 数据流
blocked_at: 2026-07-12T14:00:00+08:00
pending_hypotheses:
  - 缓存失效导致脏读
  - 配置热更新未同步
---
```

恢复时读→跳已完成步骤→从断点继续→bug解决后自动删。

## PHASE.json 状态机

```json
{"state":"idle|bootstrapping|testing|done","target":"<标识>","skill":"coding-max|coding-pipeline","started_at":"<ISO>","updated_at":"<ISO>","retry":0}
```
流转: `idle`→(搭基建)→`bootstrapping`→(管道通)→`testing`→(验证)→`done`。`retry≥3`→`done(失败)`。

## Bug报告模板 (步骤0.5用)

```yaml
---
id: BUG-YYYY-MM-DD-<slug>
severity: Trivial | Moderate | Complex
reported: YYYY-MM-DD
status: investigating
---
## 症状
<原始描述>

## 复现步骤
<提取，不完整标注"待补充">

## 环境
<语言版本/OS/关键依赖>
```
