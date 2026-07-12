---
name: coding-max
description: 当修复bug、排查报错、定位根因、处理线上问题(hotfix)、验证修复或debug时使用。触发:修bug/定位/报错/修复/验证/debug/线上/hotfix/排查/分析/崩溃/异常。
---

# coding-max

根因修复,不自欺,不留墓碑。违反文字=违反精神,每个bug都觉得自己特殊。

## 模式

| 模式 | 触发 | 走哪些步骤 |
|------|------|-----------|
| **Explore** | "看看/排查/分析" | 1→2→2.5,输出诊断,不写代码 |
| **Quick** | "常规/fix/修一下"或Moderate | 1→2(初审)→3→4→6 跳过:插桩/Premortem/冲击波/墓碑/疫苗 |
| **Standard** | 默认 | 完整0→7 |
| **Hotfix** | "线上/紧急/hotfix/火烧眉毛" | 1→2(初审)→3.2→3→6→7 跳过:存档/同模式/血统/Premortem/墓碑/疫苗/胶囊 |

Hotfix:`[HOTFIX]`前缀+事后补跳过的检查。Quick:事后补病历+疫苗。Explore:不改文件。

## 流程

### 0. 分级
拼写/注释/字符串/格式化/import排序→Trivial→直跳步骤3。其他→初审(命名/嵌套≤3/函数≤50行/参数≤5/错误一致性/同类一致性/逻辑diff)→全干净=Quick,有信号=Standard,多模块/并发/架构=Complex(+3-Strike)。步骤4不通过→升Moderate。

### 0.0 环境探测(首次,缓存)
有测试→步骤6正常 | 无测试→步骤6降级(手动验证清单) | 无测试+高风险→先确认用户

### 0.5 存档
存`.project-memory/bugs/BUG-YYYY-MM-DD-<slug>.md`。Hotfix跳过。

### 1. 搜病历
读`BUG_PATTERNS.md`。精确→模糊→同义扩展(映射见references)。命中且一致→跳步骤3。arch-标签→升Moderate。

### 2. 挖根因
**5 Whys**≥2层。Why指架构→arch-。**同模式扫描**当前模块+同级目录,>50条截断。**血统**`git log --follow`30commit同作者。不确定→排序3假设(简单>匹配>可证伪)。全错→2.5。第2+次→换视角(数据流/调用链/配置/时序)。

### 2.5 插桩
Complex/并发/时序/状态机/3假设全错→`[BUG-TRACE]`2-4个→复现→分析→清理。

### 3. TDD
**3.0**复现失败→步骤1。**3.1**Premortem(破坏/回滚/边界/模式/依赖):Trivial跳,Hotfix跳。**3.2**冲击波:grep调用方≤3跳→声明范围,Quick跳,Hotfix保留。**3.3**RED(失败)→GREEN(最少)→REFACTOR(清理)。arch-最小修(范例见references)。

### 4. 自检
代码:if-else壳/try-catch藏/改常量不解释/默认参数/解释不了根因。思维:"快修"/"试试X"/"跳过测试"/"应该是X"/"不确定能行"/"再试一次"。文档:description泄流程?引用断裂?章节缺?语言混? 清单:测试跑?代码净?改动小?真好了? 反事实:revert→bug回? 不通过→+1→步骤2。

### 5. 墓碑
清源文件+/tests。必删:test_tmp/debug/quick,≤2函数assertTrue,BUG-TRACE-TMP。建议删:无注释skip,僵尸import。commit≤5。Hotfix跳。

### 6. 全量验证
有测试:`<测试命令>`通过+覆盖率不降→步骤7。失败→+1,≥3硬停。
无测试:输出清单(复现+边界≥3+回归点+回滚)→用户确认→步骤7。

### 7. 病历+疫苗+胶囊
病历→yes/merge/no(Hotfix:`[HOTFIX]`)。疫苗→lint/CI。胶囊→弯路/突破/误导/重来。arch-≥3→`⚠️架构负债`。

## 硬约束
1.RED先于GREEN 2.补丁+红旗→重做 3.禁裸吞异常(`except:`/`catch{}`/`recover()`) 4.临时物步骤5清 5.只改冲击波范围 6.arch-不重构 7.不确定=说不确定 8.写记忆需确认 9.不pip/push/rm 10.≥3失败硬停

## 自欺红旗(触发→回步骤2)
| 借口 | 现实 |
|------|------|
| "太简单跳过TDD" | 简单也出错,30秒写测试 |
| "先修后面补" | 后面不会来 |
| "手动验过了" | 不可重复,不可审计 |
| "应该就是X" | 先验证,再下手 |
| "不确定能行" | 没挖到根因,回步骤2 |
| "再试一次"(2+) | 碰运气,硬停 |
| "这次特殊" | 文字=精神,照做 |

## 迭代控制
3-Strike(1→2换视角→3硬停),会话级,新bug重置。断点`.resume.md`,恢复自动删。

## 项目记忆
`BUG_PATTERNS`(病历索引)/`PROJECT_PROFILE`(画像,10条刷新,>30天告警)/`bugs/`(报告+胶囊)/`.resume`(断点)。格式见`references/bug-memory-format.md`,模板见`memory-template/`。

## 参考
- `references/patch-signals.md` — 补丁信号+红旗+架构异味+反事实
- `references/bug-memory-format.md` — 病历/合并/同义映射/疫苗映射/报告/小修范例
- `memory-template/` — BUG_PATTERNS/PROFILE/RESUME模板
