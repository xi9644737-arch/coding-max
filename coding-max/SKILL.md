---
name: coding-max
description: 当修复bug、排查报错、定位根因、处理线上问题(hotfix)、验证修复或debug时使用。触发:修bug/定位/报错/修复/验证/debug/线上/hotfix/排查/分析/崩溃/异常。
---

# coding-max

根因修复,不自欺,不留墓碑。违反文字=违反精神,每个bug都觉得自己特殊。

## 模式

**Quick 是默认。** 只有触发 arch- 信号、自检不通过、或多模块/并发/架构问题才升 Standard。

| 模式 | 触发 | 走哪些步骤 |
|------|------|-----------|
| **Trivial** | 拼写/注释/字符串/格式化/import排序 | 直接改→4(自检)→6(验) 跳过:0.5/1/2/2.5/3/5/7。无测试不拦截。 |
| **Quick** | **默认**。常规fix、无arch-信号 | 0→0.0→1→2(初审)→3→4→6→7(仅病历)。跳过:0.5/插桩/Premortem/冲击波/墓碑/疫苗/胶囊。无测试→警告不阻断。 |
| **Standard** | arch-信号/自检不通过/多模块/并发/架构 | 完整0→7 |
| **Explore** | "看看/排查/分析" | 1→2→2.5,输出诊断,不写代码 |
| **Hotfix** | "线上/紧急/hotfix/火烧眉毛" | 1→2(初审)→3.2→3→6→7 跳过:存档/同模式/血统/Premortem/墓碑/疫苗/胶囊 |

Hotfix:`[HOTFIX]`前缀+事后补跳过的检查。Quick:事后补病历+疫苗。Explore:不改文件。Trivial:事后补病历。

## 流程

### 0. 分级

先判上下文：**影响面**（单机/单用户/多用户/分布式）+ **信号**（拼写/注释/字符串/格式化/import排序→Trivial）。然后初审（命名/嵌套≤3/函数≤50行/参数≤5/错误一致性/同类一致性/逻辑diff）→全干净=Quick,有arch-信号(并发/数据一致性/资源泄漏/循环依赖/层级混乱)=Standard,多模块/分布式/架构=Complex(+3-Strike)。步骤4不通过→升Standard。

| 影响面 | 含义 | 倾向 |
|--------|------|------|
| 单机 | CLI/脚本 | Quick |
| 单用户 | API单次调用 | Quick/Standard |
| 多用户 | 并发共享状态 | Standard |
| 分布式 | 多服务/消息队列/DB | Standard/Complex |

### 0.0 环境探测(首次,缓存)
有测试→步骤6。无测试→Trivial跳过 / Quick警告不阻断 / Standard拦截(PHASE.json→coding-pipeline) / Hotfix跳过。高风险(多用户/分布式)→先确认。

### 0.5 存档
输出摘要→等确认→存`.project-memory/bugs/BUG-YYYY-MM-DD-<slug>.md`。Hotfix跳过。

### 1. 搜病历
读`BUG_PATTERNS.md`。精确→模糊→同义扩展(映射见references)。命中且一致→跳步骤3。arch-标签→升Moderate。

### 2. 挖根因
**5 Whys**≥2层。Why指架构→arch-。**同模式扫描**当前模块+同级目录，输出超过终端可读范围时截断(约80行)，标注截断处。**追溯**`git log -- <file>` 20条定位改动历史 + `git blame` 找最近修改行。不确定→排序3假设(简单>匹配>可证伪)。全错→2.5。第2+次→换视角(数据流/调用链/配置/时序)。

### 2.5 插桩
Complex/并发/时序/状态机/3假设全错→`[BUG-TRACE]`2-4个→复现→分析→清理。

### 3. TDD
**3.0** 复现失败→回步骤1。**3.1** Premortem(检查清单见`references/patch-signals.md`):Trivial/Hotfix跳。**3.2** 冲击波:grep调用方,≤5文件全查,声明影响范围。Quick跳,Hotfix保留。**3.3** RED→GREEN→REFACTOR。arch-用最小止血(范例见references)。

### 4. 自检
**代码**: if-else壳/try-catch藏/改常量不解释? **思维**: 快修/试试X/跳过测试/应该是X/不确定/再试(2+)? **文档**: 引用断裂?章节缺? **反事实**: revert→bug回? 不通过→+1→步骤2。

### 5. 墓碑
删除为修复临时创建的文件和标记(BUG-TRACE/临时test/调试代码)。commit≤5。Hotfix跳。

### 6. 全量验证
有测试:`<测试命令>`通过+增量覆盖率≥基线(PROJECT_PROFILE)→步骤7。比增量不卡全局,重构删死代码不阻塞。失败→+1,≥3硬停。
无测试:输出清单(复现+边界≥3+回归点+回滚)→用户确认→步骤7。

### 7. 病历+疫苗+胶囊
**病历**(自动提取→人工确认):从`git diff --stat`+commit message自动生成摘要。格式:`<日期> · <文件>:<行> <类型> — <根因一句话>`。人工只确认/修改,不手写。
**疫苗**→lint/CI规则映射(见疫苗映射表)。
**胶囊**→弯路/突破/误导/重来。Quick/Trivial事后补。arch-≥3→`⚠️架构负债`。
Hotfix:`[HOTFIX]`前缀+事后补。

## 硬约束
1.RED先于GREEN 2.补丁+红旗→重做 3.禁裸吞异常(`except:`/`catch{}`/`recover()`) 4.临时物步骤5清 5.只改冲击波范围 6.arch-不重构(最小安全修复) 7.不确定=说不确定 8.写记忆前输出摘要→等确认 9.不全局安装CLI/不push --force/不rm -rf(测试框架pip install例外) 10.≥3失败硬停 11.**Quick是默认**,不因无测试而阻塞Trivial/Quick 12.影响面驱动分级,不看代码行数

## 自欺红旗(触发→回步骤2)
| 借口 | 现实 |
|------|------|
| "太简单跳过TDD" | 简单也出错 |
| "先修后面补" | 后面不会来 |
| "应该就是X" | 先验证再下手 |
| "不确定能行" | 没挖到根因 |
| "再试一次"(2+) | 碰运气,硬停 |

## 迭代控制
3-Strike(1→2换视角→3硬停),会话级,新bug重置。断点`.resume.md`,恢复自动删。

## 项目记忆
`BUG_PATTERNS`(病历)/`PROJECT_PROFILE`(画像+基线)/`bugs/`(报告+胶囊)/`.resume`(断点)/`PHASE.json`(状态机:idle→bootstrapping→testing→done,格式见`references/bug-memory-format.md`)。模板见`memory-template/`。

## 参考+联动
- `references/patch-signals.md` — 补丁信号+红旗+架构异味+反事实
- `references/bug-memory-format.md` — 病历/合并/同义映射/疫苗映射/报告/小修范例
- `memory-template/` — BUG_PATTERNS/PROFILE/RESUME模板
- `coding-pipeline` — 配套skill:搭测试基建→打通步骤6
