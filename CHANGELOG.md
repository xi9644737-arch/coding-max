# Changelog

## [1.0.2] - 2026-07-12

### coding-max — 精炼

- **三层结构**: 铁律(Always-On) → 模式路由(5模式) → 3阶段流程(诊断→修复→验证)
- **5条铁律**置于文件最前
- **2个人机检查点**: CP1诊断确认 + CP2方案确认 (Standard模式)
- **并行诊断**: Standard从3视角(数据流/调用链/时序)并行扫描
- **插桩策略具体化**: `[BUG-TRACE]` 格式(时间戳+线程ID+状态变量+预期vs实际)
- 流程精简: 从11步合并为10步，消除碎片编号，步骤名语义化
- 自欺红旗与铁律1联动
- 修复悬空引用(Complex)、统一术语、精简冗余

### coding-pipeline — 精炼

- **5语言一等支持**: Python/Node/Go/Rust/Java，各含Phase1+CI模板
- **冒烟加深**: Phase1加裸catch检查+导入可解析性+`__init__.py`检查
- **CI模板生产级**: `actions/cache@v4`+`codecov/codecov-action@v4`+Slack通知模板
- Pre-commit主动探测`.pre-commit-config.yaml`+追加变更模块测试
- 新增 `github-actions-ci-template.yml`(5语言完整示例+缓存+Codecov+Slack)
- 疫苗映射表扩展至7语言
- 必含要素和硬约束改为清晰列表

### 修复

- SDO 反模式: description 从工作流摘要改为纯触发条件
- Hotfix 保留冲击波分析
- Trivial 快速通道: 拼写/注释/格式化变更不再误升 Moderate
- 硬约束去语言专属化

---

## [1.0.0] - 2026-07-12

### 新增
- 4种模式: Explore/Quick/Standard/Hotfix
- 9步根因修复流程 + 10条硬约束 + 7个自欺红旗
- 项目记忆体系: 病历索引、项目画像、断点恢复
- patch-signals + bug-memory-format 参考文件
- 无测试项目的环境探测与手动验证降级路径
