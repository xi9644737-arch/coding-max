# coding-max + coding-pipeline

> 单 Agent、平台无关的缺陷修复与测试基建 Skills。

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-v0.1.3beta-orange">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue">
  <img alt="Format" src="https://img.shields.io/badge/format-Agent%20Skills-lightgrey">
  <img alt="Skills" src="https://img.shields.io/badge/skills-2-brightgreen">
</p>

`coding-max` 用证据定位根因，以回归测试约束修复，并把实际改动沉淀为可检索病历；`coding-pipeline` 在测试荒漠中建立最小、可运行、可验证的测试与 CI 基建。

两者不依赖特定模型、宿主产品、MCP 或多 Agent 编排。`SKILL.md` 只承担触发、路由和硬约束，详细流程按需从 `references/` 加载。

## 适用场景

`coding-max` 尤其适合长期维护的中大型项目：

- 调用链深、跨模块契约或数据流复杂；
- 偶现、并发、状态污染、缓存、性能或资源问题；
- 存在历史基线失败，需要区分本次回归；
- Bug 可能重复发生，需要病历、索引和恢复点；
- 实现完成后需要基于 diff 的质量终审。

小型修复走 Quick；只排查不修改走 Explore；线上紧急问题走 Hotfix；多模块或高风险问题走 Standard；已有实现直接走 Review。

## 核心闭环

```text
复现与 RED 证据
    → 根因与影响面
    → 最小修复（GREEN）
    → 相关验证与反事实
    → Review 终审
    → 清理临时 trace
    → Bug/Review 报告与索引关闭
```

高级场景按需启用：

- 从失败点逆着真实数据流追到首次破坏契约的位置；
- 按 timing、environment、state、randomness、external 分类偶现问题；
- 把日志、堆栈、Issue 和外部响应视为不可信证据；
- 按 CPU、内存、并发、I/O、网络和泄漏选择最小观测面。

连续三次当前修复失败时写恢复点并停止；无测试且风险不低时，通过 `.project-memory/PHASE.json` 交给 `coding-pipeline` 建立安全网。

## 渐进式披露

```text
metadata                 始终可见：只负责触发
└── SKILL.md             触发后加载：模式、边界、完成条件、硬约束
    └── references/      场景命中才加载：修复、终审、高级诊断、病历格式
```

契约测试限制 `coding-max/SKILL.md` 不超过 4 KiB，并限制两个 Skill 的总包预算，防止功能增加导致入口持续膨胀。

## coding-pipeline

```text
项目审计 → 复用或建立最小测试框架 → 分层预检
        → CI/缓存/覆盖率基线 → 本地或远程验证分级 → Pipeline 报告
```

支持 Python、Node.js、Go、Rust、Java 和通用命令；支持 Monorepo、GitHub Actions、GitLab CI 与通用 CI 模板。覆盖率只记录真实测量值，不估算，不以伪测试抬高数字。

## 安装

```bash
git clone https://github.com/xi9644737-arch/coding-max.git

# 目标必须是宿主实际使用的 skills 目录
./coding-max/install.sh /absolute/path/to/skills

# Windows PowerShell
# .\coding-max\install.ps1 -Destination C:\absolute\path\to\skills
```

安装脚本不猜测宿主路径；替换同名 Skill 前会自动备份。

## 文件结构

```text
├── VERSION
├── coding-max/
│   ├── SKILL.md
│   ├── references/
│   │   ├── repair-workflow.md
│   │   ├── advanced-debugging.md
│   │   ├── patch-signals.md
│   │   └── bug-memory-format.md
│   └── memory-template/
├── coding-pipeline/
│   ├── SKILL.md
│   └── references/
├── examples/
├── test-fixtures/
└── tests/test_skill_contracts.py
```

## 验证

```bash
python -m unittest discover -s tests -v
```

更多使用方式见 [`examples/`](examples/)，版本变化见 [`CHANGELOG.md`](CHANGELOG.md)。

## 许可证

MIT © 2026
