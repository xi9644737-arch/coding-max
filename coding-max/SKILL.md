---
name: coding-max
description: 根因修复引擎。触发:修bug/定位/报错/修复/验证/debug/线上/hotfix/排查/分析/崩溃/异常。Quick是默认。
---

# coding-max

根因修复，不自欺，不掩盖，不遗留。

## 铁律

1. **不自欺** — "应该就是X""先修后面补""再试一次"→停
2. **RED先于GREEN** — 先写失败测试，再修
3. **禁裸吞异常** — `except:` / `catch{}` / `recover()` 带类型
4. **不确定=说不确定** — 没挖到根因就承认
5. **最小修复** — 只改冲击波。arch-止血不重构

≥3次失败→硬停，展示所有尝试，请用户介入。

## 模式路由

| 触发 | 模式 | 步骤 |
|------|------|------|
| 拼写/注释/字符串/格式化/import排序 | **Trivial** | 直接改→自检→验证 |
| 常规bug **(默认)** | **Quick** | 搜病历→5Whys→假设表→TDD→自检→验证→病历 |
| arch-/并发/多模块/自检不通过 | **Standard** | 搜病历→4域并行→假设表→CP1→插桩→Premortem→CP2→TDD→自检→验证→疫苗+胶囊 |
| "看看/排查/分析" | **Explore** | 搜病历→5Whys→假设表→插桩，**不改代码**，输出诊断 |
| "线上/紧急/hotfix" | **Hotfix** | 搜病历→5Whys→冲击波→TDD(GREEN)→自检→验证，`[HOTFIX]`前缀 |

信号不明时: 单机→Quick | 多用户→Standard | 分布式→Standard

## 流程

**1. 搜病历** (全部) — 读 `BUG_PATTERNS.md`。精确→模糊→同义扩展(见references)。命中且一致→跳TDD。arch-命中→升Standard。

**2. 5 Whys** (全部，≥2层) — Standard从**4域并行**: ①日志/报错 ②git血统(`git log -20`+`git blame`) ③配置/环境 ④近期变更(`git diff HEAD~5`)。

→ 输出**假设表**:

| # | 假设 | 置信度 | 验证方法 | 结果 |
|---|------|--------|---------|------|

按置信度排。逐一验证→填结果。确认的即根因。全排除→进插桩。第2轮→换领域。

**3. 插桩** (假设表全排除/并发/时序) — ①标记状态变更点(赋值/函数口/锁) ②插入 `[BUG-TRACE]`(时间戳+线程+变量+预期vs实际) ③复现→对比预期状态转换→找偏离→**清理**。

### 🔴 CP1 — 诊断确认 (Standard)

展示假设表(已填结果)+根因+证据。**等用户确认。** 拒绝→换领域。

**4. Premortem** (Standard) — 会搞坏什么？能单commit revert？≥3边界(含1非happy-path)。

**5. 冲击波** (Quick/Standard/Hotfix) — grep调用方。≤5全查。声明影响面。

**6. TDD** (全部) — RED(失败测试)→GREEN(最小改)→REFACTOR(消重复，Hotfix跳)。

### 🔴 CP2 — 方案确认 (Standard)

展示diff+影响面+边界。**等用户确认。**

**7. 三层自检** (全部) — 代码:创可贴？(if-else壳/try-catch藏/改常量/加默认参数→见references) 思维:红旗？反事实:revert→bug回？不通过→+1 strike→回5Whys。

**8. 全量验证** (全部) — 有测试:全跑+增量覆盖率≥基线。无测试:Quick/Trivial/Hotfix→手动清单；Standard→拦截→`PHASE.json`→coding-pipeline→回步骤8。

**9. 病历+疫苗+胶囊** (Quick/Standard) — 病历:`git diff --stat`+commit自动提取→确认→追加 `BUG_PATTERNS.md`。疫苗:根因→lint/CI(见映射表)。胶囊:弯路/突破/误导/重来≥1项。arch-≥3→`⚠️架构负债`。

**10. 墓碑** — 清理 `[BUG-TRACE]`/临时test/调试日志。

## 记忆文件

`BUG_PATTERNS.md` | `PROJECT_PROFILE.md` | `bugs/` | `.resume.md` | `PHASE.json`(`idle→bootstrapping→testing→done`)

## 参考

`references/patch-signals.md`(补丁+红旗+异味+反事实+Premortem) | `references/bug-memory-format.md`(病历/同义/疫苗/止血) | `../coding-pipeline`(搭基建)
