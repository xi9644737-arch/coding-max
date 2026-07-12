# 🪦 coding-max

> 根因修复引擎。不自欺，不留墓碑。

<p align="center">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue">
  <img alt="Format" src="https://img.shields.io/badge/format-Markdown%20%2B%20YAML-lightgrey">
  <img alt="Lines" src="https://img.shields.io/badge/size-4.4KB-small">
</p>

---

AI 修 bug 最大的问题不是修不好，是**假装修好了**。加个 if-else 把异常吞掉、包层 try-catch 让报错消失、改个常量值碰运气——代码不炸了，根因还在。

`coding-max` 是一套让 AI **直面根因**的方法论。纯文本文件，不绑定任何平台。4 种模式、9 步流程、10 条硬约束、7 个自欺红旗。

---

## 四种模式，一个引擎

```
Explore          Quick           Standard         Hotfix
 "看看"          "修一下"          "有bug"         "线上炸了"
   │               │                │                │
   ├─ 只诊断       ├─ 精简流程       ├─ 完整9步       ├─ 紧急通道
   ├─ 不改代码     ├─ 跳过插桩       ├─ 5 Whys挖根    ├─ 保留冲击波
   ├─ 不写文件     ├─ 跳过Premortem  ├─ TDD红绿重构   ├─ 跳过文档归档
   └─ 输出报告     └─ 事后补病历     └─ 疫苗+胶囊     └─ 事后补全检查
```

---

## 怎么装

这是一个 **纯文本方法论文件**（Markdown + YAML），不是 npm 包、不是 VS Code 插件、不需要编译。**无论你的 AI 编程助手是什么，只要能加载 markdown 指令，就能用。**

```bash
# 通用方式（任何支持指令文件的 AI 工具）
git clone https://github.com/xi9644737-arch/coding-max.git
# 然后把 SKILL.md 放到你 AI 工具读取规则/指令的目录

# Claude Code 用户
git clone https://github.com/xi9644737-arch/coding-max.git ~/.claude/skills/coding-max

# Cursor / Windsurf 用户
git clone https://github.com/xi9644737-arch/coding-max.git .cursor/rules/coding-max

# 其他 AI Agent（Copilot / Codex / Aider 等）
# 将 SKILL.md 内容复制到你的项目级或用户级 agent 指令文件中
```

---

## 做了什么

| 步骤 | 干了什么 | 跳过条件 |
|------|---------|---------|
| 0. 分级 | Trivial/Moderate/Complex 自动判定，拼写错误直通修复 | — |
| 0.0 环境探测 | 检测项目有无测试体系，没有就降级为手动验证 | 缓存会话 |
| 0.5 存档 | 建 Bug 报告 | Hotfix 跳过 |
| 1. 搜病历 | 查历史 Bug 模式，命中直接复用 | 首次使用 |
| 2. 挖根因 | 5 Whys ≥2层 + 同模式扫描 + git 血统追溯 | — |
| 2.5 插桩 | `[BUG-TRACE]` 埋点复现，分析偏离点 | Trivial/Moderate 跳过 |
| 3. TDD | RED(先写失败测试) → GREEN(最少修复) → REFACTOR(清理) | — |
| 4. 自检 | 代码层/思维层/文档层三层审查 + 反事实测试 | — |
| 5. 墓碑 | 清理临时调试代码 | Hotfix 跳过 |
| 6. 全量验证 | 跑全量测试 + 覆盖率比对（无测试项目降级为手动清单） | — |
| 7. 病历+疫苗+胶囊 | 写病历 / 生成 lint 规则 / 记录弯路和突破 | — |

## 硬约束

```
1. RED 先于 GREEN          6. arch-根因不重构
2. 补丁+红旗→重做          7. 不确定=说不确定
3. 禁裸吞异常               8. 写记忆需确认
4. 临时物步骤5清            9. 不 pip / push / rm
5. 只改冲击波范围           10. ≥3 失败硬停
```

## 自欺红旗

AI 冒出以下念头 → 立刻停止，回到步骤 2 换视角：

| 借口 | 现实 |
|------|------|
| "太简单跳过 TDD" | 简单也出错 |
| "先修后面补" | 后面不会来 |
| "手动验过了" | 不可审计 |
| "应该就是 X" | 先验证 |
| "不确定能行" | 没挖到根因 |
| "再试一次" | 碰运气 |
| "这次特殊" | 每个 bug 都觉得自己特殊 |

## 文件结构

```
├── SKILL.md                    # 主引擎（4.4KB）
├── references/
│   ├── patch-signals.md        # 5个补丁信号 + 6个认知红旗 + 架构异味
│   └── bug-memory-format.md    # 病历格式 + 同义映射 + 疫苗映射 + 修复范例
└── memory-template/
    ├── BUG_PATTERNS.md         # 病历索引模板
    ├── PROJECT_PROFILE.md      # 项目画像模板
    └── RESUME.md               # 断点恢复模板
```

## 许可证

MIT © 2026
