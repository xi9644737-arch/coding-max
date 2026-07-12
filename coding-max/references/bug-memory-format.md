# 病历记录格式规范

## 记录格式

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

- **yes**: 追加到文件末尾，保持与上一条记录间有一个空行
- **merge**: 找到症状关键词匹配 ≥2 的已有记录，插入"补充"子节
- **no**: 不写入

## 合并格式

```markdown
### 2026-07-10 · bare except 吞异常
- 症状: ...
- 根因: ...
- 根因类型: 代码层面
- 修复: ...
- 标签: bare-except, 异常处理

### 补充 (2026-07-12)
- 发现位置: 手星.py:56
- 修复: 同上方案
```

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

| 中文 | 英文/缩写 | | 中文 | 英文/缩写 |
|------|----------|-|------|----------|
| 超时 | timeout | | 竞态 | race-condition |
| 空指针/空值 | None / null / nil / undefined | | 溢出 | overflow / stack-overflow |
| 连接 | connection | | 注入 | injection / SQLi / XSS |
| 死锁 | deadlock | | 泄漏 | leak |
| 内存/OOM | memory / OutOfMemory | | 死循环 | infinite-loop / endless-loop |
| 递归 | recursion | | 循环依赖 | circular-import / circular-dependency |

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

| 异味 | 最小修复（不改架构） |
|------|---------------------|
| 循环依赖 | 延迟导入 / import移入函数内 |
| 层级混乱 | 加参数校验+明确错误信息，不搬业务逻辑 |
| 上帝模块 | 加类型校验和边界检查，不拆分 |
| 缺少抽象 | 只修触发点，不改其他N-1处重复 |
| 紧耦合 | 薄适配函数(1-3行)，不解耦 |
| 改动扩散 | 修触发模块，其余加防御性校验(不改逻辑) |
| 接口泄漏 | 调用处加字段筛选/过滤，不重新设计接口 |
