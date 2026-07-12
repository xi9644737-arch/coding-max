# 病历记录格式规范

## 记录格式

### 自动提取（步骤7默认）
从 `git diff --stat` + commit message 自动生成，人工确认：
```bash
git diff --stat HEAD~1 | tail -1  # → "3 files changed, 12 insertions(+), 5 deletions(-)"
git log -1 --format="%s"          # → "fix: KeyError when user missing email field"
```
生成摘要: `2026-07-12 · main.py:19 KeyError — 用户缺少email字段时get_user崩溃`

### 手动格式（自动提取失败时）

```markdown
### YYYY-MM-DD · <简短标题>
- 症状: <用户原始描述或报错信息摘要>
- 根因: <5 Whys 得出的根本原因>
- 根因类型: 代码层面 / 架构层面
- 修复: <具体改动，可引用 commit hash>
- 文件: <修改的文件列表 + 行号>
- 环境: Python版本, OS, 关键依赖版本
- 标签: <逗号分隔的关键词>
- 迭代次数: <本次修复尝试次数（1~3）>
```

## 标签词汇表

### 代码层面
```
异常类:     bare-except, swallowed-exception, type-error, key-error
并发类:     race-condition, deadlock, thread-safety
资源类:     memory-leak, connection-leak, file-not-closed
输入类:     sql-injection, xss, path-traversal, no-validation
逻辑类:     off-by-one, null-check, boundary, infinite-loop
```

### 架构层面（arch- 前缀）
```
耦合类:     arch-coupling, tight-coupling, circular-import
结构类:     wrong-layer, god-module, missing-abstraction
边界类:     leaky-interface, cross-module-side-effect
```

## 架构病历积累规则

同一 `arch-` 标签在病历中出现 ≥3 次 → 输出架构负债警告：

```
⚠️ 架构负债警告
标签 "{circular-import}" 已出现 3 次:
  - 2026-07-01: 回路.py
  - 2026-07-08: 引擎.py
  - 2026-07-12: 连接器.py

建议: 安排独立的架构重构迭代，而非继续逐条修复。
```

## 写入规则

- **yes**: 追加到末尾，留一空行
- **merge**: 关键词匹配已有记录（≥2）→ 追加 `### 补充 (日期) ...`
- **no**: 不写入

---

## 胶囊格式（步骤7，每次修复末尾）

不新建文件，追加在 BUG 报告末尾的 `## 胶囊` 节：

```markdown
## 胶囊
- 弯路: 一开始以为是 X 问题，花了 2 次尝试才发现不是
- 突破: 读了 Y 模块的调用方才意识到真正原因
- 误导: Z 日志信息指向了错误方向
- 重来: 如果再修一次，会先 grep 调用方再下手
```

至少填 1 项。全是"无" = 没认真反思。

---

## .resume 断点格式（迭代控制用）

3-Strike 触发硬停时写入 `.project-memory/.resume.md`：

```yaml
---
bug_id: BUG-2026-07-12-buggy-python
strikes: 2
last_step: 2
last_perspective: 数据流
blocked_at: 2026-07-12T14:00:00+08:00
pending_hypotheses:
  - 缓存失效导致脏读
  - 配置热更新未同步
---
```

恢复时读取 → 跳过已完成步骤 → 从 `last_step` 继续。bug 解决后自动删。格式: YAML frontmatter + 必要上下文（不再放 Markdown 正文，避免幻觉）。

---

## PHASE.json 状态机（步骤0.0用，多skill通信）

```json
{"state":"idle|bootstrapping|testing|done","target":"<标识>","skill":"coding-max|coding-pipeline","started_at":"<ISO>","updated_at":"<ISO>","retry":0}
```
流转: `idle`→(搭基建)→`bootstrapping`→(管道通)→`testing`→(验证)→`done`。`skill`字段区分调用方。`retry`≥3→`done`(失败)。

## 索引

文件开头维护一个索引：

```markdown
## 索引
| 日期 | 类型 | 标签 | 症状摘要 |
|------|------|------|---------|
| 2026-07-12 | 代码 | bare-except | 回路.py 静默失败 |
| 2026-07-10 | 架构 | circular-import | 引擎.py 和回路.py 互相导入 |
```

---

## 同义扩展映射表（步骤1检索用）

**用法**: 用户说"炸了"→查表→搜 `crash` / `panic` / `exception` / `exit-code`

| 症状聚类 | 口语说法 | 搜索关键词 |
|----------|---------|-----------|
| 崩溃/退出 | 炸了/挂了/崩了/闪退/core dump/进程没了 | crash, panic, segfault, exit, signal, core dump |
| 卡住/无响应 | 卡死/不动了/转圈/冻住 | hang, freeze, deadlock, timeout, block |
| 慢 | 龟速/吃不消/跑不动 | slow, timeout, O(n²), latency, bottleneck |
| 内存爆了 | OOM/吃内存/内存泄漏/越跑越大 | memory leak, OOM, heap, RSS, GC thrash |
| 数据错了 | 不对/丢了/脏数据/凭空出现 | wrong result, data loss, corruption, stale |
| 不生效 | 没用/没反应/跟没改一样 | no-op, config not loaded, cache not invalidated |
| 偶发/重现不了 | 时好时坏/有时候/我这儿好的 | intermittent, flaky, race condition, heisenbug |
| 以前好的现在坏了 | 老版本没事/升级后/回退了 | regression, bisect, git bisect, good→bad |
| 循环依赖 | 互相import/蛋鸡问题/套娃 | circular import, cycle, dependency loop |
| 配置文件不生效 | 改了没用/环境不对/路径不对 | config, env, path, precedence, override |

---

## Bug报告模板（步骤0.5用）

```yaml
---
id: BUG-YYYY-MM-DD-<slug>
severity: <Trivial|Moderate|Complex>
reported: YYYY-MM-DD
status: investigating
---
## 症状
<原始描述>

## 复现步骤
<提取，不完整标注"待补充">

## 环境
<语言版本 / OS / 关键依赖>
```

---

## 疫苗映射表（步骤7用，按根因→lint规则/CI脚本）

| 根因类型 | Python | TypeScript | Go | 通用 |
|---------|--------|-----------|-----|------|
| null-check遗漏 | mypy strict | strictNullChecks | nilaway | 关键入口加断言 |
| bare-except | ruff BLE001 | no-unsafe-catch | errcheck | grep禁止`except:`(不含except () |
| 竞态条件 | — | — | -race flag | CI重复压测脚本 |
| SQL注入 | bandit B608 | no-sql-injection | sqlcheck | 参数化查询 |
| 循环导入 | `python -c 'import <m>'` | madge --circular | go mod graph | CI导入检查 |
| 资源泄漏 | ruff PL | no-unsafe-finally | defer检查 | with/try-with-resources |
| 边界遗漏 | hypothesis | fast-check | fuzzing | property-based test |

---

## 架构最小修复范例（步骤3.3用）

⚠️ 这些是**止血**，不是修复。每条都应打 `arch-` 标签，积累≥3 触发架构负债警告。

| 异味 | 最小止血 | 真正的重构（独立任务） |
|------|---------|---------------------|
| 循环依赖 | 延迟导入(⚠️临时:把import-time炸推迟到runtime) | 抽取共同接口/依赖倒置 |
| 层级混乱 | 加参数校验+明确错误信息，不搬业务逻辑 | 分层重组 |
| 上帝模块 | 加类型校验和边界检查，不拆分 | 按职责拆模块 |
| 缺少抽象 | 只修触发点，不改其他N-1处重复 | 抽取公共函数/基类 |
| 紧耦合 | 薄适配函数(1-3行) | 引入接口/DI |
| 改动扩散 | 修触发模块，其余加防御性校验(不改逻辑) | 消除隐式依赖 |
| 接口泄漏 | 调用处加字段筛选/过滤 | 重新设计接口契约 |
