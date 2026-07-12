# coding-max

根因修复引擎 — 不自欺，不留墓碑。架构腐烂和代码 bug 一视同仁。

## 安装

### Claude Code（推荐）

```bash
# 用户级安装（所有项目可用）
git clone https://github.com/<your-username>/coding-max.git ~/.claude/skills/coding-max

# 项目级安装（仅当前项目）
git clone https://github.com/<your-username>/coding-max.git .claude/skills/coding-max
```

### 手动

将 `coding-max/` 目录复制到 Claude Code 的 skills 目录即可，符合 [agentskills.io](https://agentskills.io) 规范。

## 使用

对话中遇到 bug 时自动触发，或直接说：

| 说法 | 模式 |
|------|------|
| "帮我看看这个报错" | Explore — 仅诊断，不改代码 |
| "修一下这个 bug" | Quick — 常规修复，精简流程 |
| "这里有个 bug" | Standard — 完整根因修复 |
| "线上炸了赶紧修" | Hotfix — 紧急修复，保留冲击波分析 |

## 文件结构

```
coding-max/
├── SKILL.md                          # 主文件
├── references/
│   ├── patch-signals.md              # 补丁信号 + 认知红旗
│   └── bug-memory-format.md          # 病历格式 + 疫苗映射
└── memory-template/
    ├── BUG_PATTERNS.md               # 病历索引模板
    ├── PROJECT_PROFILE.md            # 项目画像模板
    └── RESUME.md                     # 断点恢复模板
```

## 许可证

MIT
