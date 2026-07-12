---
name: coding-max
description: 根因修复引擎。触发:修bug/定位/报错/修复/验证/debug/线上/hotfix/排查/分析/崩溃/异常。Quick是默认。
---

# coding-max

根因修复，不自欺，不掩盖，不遗留。

## 铁律

违反→回诊断。同bug ≥3次失败→硬停，展示所有尝试，请用户介入。

1. **不自欺** — "应该就是X""先修后面补""再试一次"→停，重新分析
2. **RED先于GREEN** — 先写失败测试，确认它失败，再修
3. **禁裸吞异常** — `except:` / `catch{}` / `recover()` 带具体类型
4. **不确定=说不确定** — 没挖到根因就承认
5. **最小修复** — 只改冲击波范围。arch-根因止血不重构

## 模式路由

按触发信号选模式。信号不明确时参考影响面: 单机→Quick倾向 | 多用户/并发→Standard倾向。

| 触发信号 | 模式 | 走什么 |
|---------|------|--------|
| 拼写/注释/字符串/格式化/import排序 | **Trivial** | 直接改→三层自检→验证 |
| 常规bug，无arch-信号 **(默认)** | **Quick** | 搜病历→5Whys→TDD→三层自检→验证→病历 |
| arch-信号/并发/多模块/自检不通过 | **Standard** | 搜病历→并行5Whys→🔴CP1→Premortem→🔴CP2→TDD→三层自检→验证→疫苗+胶囊 |
| "看看/排查/分析" | **Explore** | 搜病历→5Whys→插桩，**不改代码**，输出诊断报告 |
| "线上/紧急/hotfix/火烧眉毛" | **Hotfix** | 搜病历→5Whys→冲击波→TDD(GREEN)→三层自检→验证。`[HOTFIX]`前缀，事后补 |

## 流程

### 诊断

**1. 搜病历** — 读 `.project-memory/BUG_PATTERNS.md`。精确→模糊→同义扩展(见 `references/bug-memory-format.md`)。命中且一致→跳TDD。arch-标签命中→升Standard。

**2. 5 Whys** (≥2层) — Standard从**3视角并行**扫:
- **数据流**: 输入→处理→输出，偏离发生在哪步？
- **调用链**: 谁破坏了契约？
- **时序**: 竞态窗口？状态机非法转换？

不确定→≤3假设(简单>匹配>可证伪排序)。全错→进插桩。第2轮→换视角。`git log -- <file> -20` + `git blame` 查回归。

**3. 插桩** (3假设全错/并发/时序时触发) — 关键状态变更点插入 `[BUG-TRACE]`(时间戳+线程ID+状态变量+预期vs实际)，复现→分析偏离→确认根因后**立即清理**。

### 🔴 检查点1 — 诊断确认 (Standard)

输出: 根因假设+置信度+证据(git血统/日志/代码)+备选假设。**等用户确认后进入修复。** 拒绝→换视角重诊。

### 修复

**4. Premortem** (Standard) — 写修复方案前: 会搞坏什么？能单commit revert？≥3个边界用例(含1个非happy-path)？

**5. 冲击波** — grep调用方。≤5文件全查。声明影响面。Quick≤3句。

**6. TDD: RED→GREEN→REFACTOR** — RED: 测试确认在未修复代码上失败。GREEN: 最小修改。REFACTOR(Quick/Standard): 消重复。Hotfix跳过。

### 🔴 检查点2 — 方案确认 (Standard)

展示diff+影响面+边界。**等用户确认后应用修复。**

### 验证

**7. 三层自检** — 代码层: 创可贴？(if-else壳/try-catch藏/改常量不解释/加默认参数不追踪→见 `references/patch-signals.md`) 思维层: 红旗念头？反事实: revert→bug重现？不通过→+1 strike→回诊断。

**8. 全量验证** —
- 有测试: 全跑+增量覆盖率≥基线。重构删死代码不阻塞。失败→+1 strike。
- 无测试: Quick/Trivial/Hotfix→手动清单(复现+≥3边界+回归点+回滚)。Standard→拦截→`PHASE.json(state:bootstrapping)`→coding-pipeline搭基建→回步骤8。

**9. 病历+疫苗+胶囊** —
- **病历**: `git diff --stat`+commit message自动提取摘要→人工确认→追加 `BUG_PATTERNS.md`
- **疫苗**: 根因→lint/CI规则(见 `references/bug-memory-format.md` 映射表)
- **胶囊**: 弯路/突破/误导/重来，≥1项
- **架构负债**: 同arch-标签≥3次→`⚠️架构负债警告`

**10. 墓碑** (Standard/Quick) — 清理 `[BUG-TRACE]`/临时test/调试日志。commit≤5文件。

## 迭代控制

- **3-Strike**: 1→换视角, 2→换视角+并行诊断, 3→硬停+写 `.resume.md`
- **断点**: 启动读 `.resume.md`→跳已完成步骤→继续→完成后删
- **PHASE.json**: `idle→bootstrapping→testing→done`，与coding-pipeline联动

## 项目记忆

`BUG_PATTERNS.md`(病历) | `PROJECT_PROFILE.md`(画像+基线) | `bugs/`(报告+胶囊) | `.resume.md`(断点) | `PHASE.json`(联动状态)

## 参考

- `references/patch-signals.md` — 补丁信号+认知红旗+架构异味+反事实+Premortem清单
- `references/bug-memory-format.md` — 病历/同义扩展/疫苗映射/最小止血范例
- `memory-template/` — 初始化模板
- `../coding-pipeline` — 配套: 搭测试基建
