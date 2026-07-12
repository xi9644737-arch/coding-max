# 🪦 coding-max + coding-pipeline

> 根因修复引擎 + 测试基建引擎。不自欺，不掩盖，不遗留。

<p align="center">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue">
  <img alt="Format" src="https://img.shields.io/badge/format-Markdown%20%2B%20YAML-lightgrey">
  <img alt="Skills" src="https://img.shields.io/badge/skills-2-orange">
  <img alt="Languages" src="https://img.shields.io/badge/langs-Python%20%7C%20Node%20%7C%20Go%20%7C%20Rust%20%7C%20Java-brightgreen">
</p>

---

AI 修 bug 最大问题是**假装修好了**——包层 try-catch 让报错消失、改个常量碰运气、加个 if-else 把异常吞掉。另一个问题是**没测试还硬修**——没有安全网，越修越慌。

| Skill | 干什么 | 设计哲学 |
|-------|--------|---------|
| `coding-max` | 根因修复引擎 | 5模式 × 3阶段(诊断→修复→验证) × 5铁律 × 2人机检查点 |
| `coding-pipeline` | 测试基建引擎 | 审计→装框→冒烟(两段)→CI(生产级)→增量基线，5语言一等支持 |

双 skill 通过 `PHASE.json` 状态机联动：无测试→拦截→搭基建→回正常流。

---

## 快速预览

**"用户列表接口偶尔 500，`KeyError: 'display_name'`"** → coding-max (Quick):

```
搜病历→5 Whys(3视角)→TDD:RED→GREEN→REFACTOR→三层自检(代码/思维/反事实)→验证通过→病历归档
```

**"项目全无测试，帮我搭基建"** → coding-pipeline:

```
审计→Monorepo(web+api)→装pytest+vitest→Phase1语法树冒烟(秒级)→GitHub Actions(矩阵+缓存+Codecov)→增量基线84%
```

更多 → [`examples/`](examples/)

---

## 安装

```bash
git clone https://github.com/xi9644737-arch/coding-max.git

# Claude Code — 复制到 skills 目录
cp -r coding-max/coding-max ~/.claude/skills/coding-max
cp -r coding-max/coding-pipeline ~/.claude/skills/coding-pipeline

# 一行安装
# Windows:  irm https://raw.githubusercontent.com/xi9644737-arch/coding-max/master/install.ps1 | iex
# macOS/Linux: curl -fsSL https://raw.githubusercontent.com/xi9644737-arch/coding-max/master/install.sh | bash
```

其他 AI Agent: 将 `SKILL.md` 放到工具的规则/指令目录。

---

## coding-max 结构

```
5 铁律 (Always-On)
    ↓
模式路由 (5模式: Trivial/Quick/Standard/Explore/Hotfix)
    ↓
┌─ 诊断 ─────────────────────────────────────┐
│ 搜病历 → 5 Whys(3视角并行) → 插桩(条件触发)  │
│              🔴 CP1: 诊断确认               │
├─ 修复 ─────────────────────────────────────┤
│ Premortem → 冲击波 → TDD(RED→GREEN→REFACTOR)│
│              🔴 CP2: 方案确认               │
├─ 验证 ─────────────────────────────────────┤
│ 三层自检 → 全量验证 → 病历+疫苗+胶囊 → 墓碑   │
└────────────────────────────────────────────┘
```

| 铁律 | 说明 |
|------|------|
| 不自欺 | "应该就是X"/"先修后面补"/"再试一次"→停，重分析 |
| RED先于GREEN | 先写失败测试，确认失败，再修 |
| 禁裸吞异常 | `except:`/`catch{}`/`recover()` 永远带类型 |
| 不确定=说不确定 | 没挖到根因就承认 |
| 最小修复 | 只改冲击波范围，arch-止血不重构 |

---

## coding-pipeline 结构

```
审计(Glob/Grep, 5语言一等支持) → 装框架 → 两段冒烟(Phase1秒级) → CI(缓存+Codecov+Slack) → 增量基线
```

**语言支持:** Python(pytest) · Node(vitest/jest) · Go(testing+testify) · Rust(cargo test) · Java(JUnit5+JaCoCo) + 通用模板

---

## 文件结构

```
├── coding-max/                     # 根因修复引擎
│   ├── SKILL.md                    # 5铁律 + 5模式 + 3阶段 + 2检查点
│   ├── references/
│   │   ├── patch-signals.md        # 5补丁信号 + 6认知红旗 + 架构异味 + Premortem清单
│   │   └── bug-memory-format.md    # 病历/胶囊/同义扩展/疫苗映射(7语言)/最小止血范例
│   └── memory-template/            # BUG_PATTERNS / PROFILE / RESUME 初始化模板
├── coding-pipeline/                # 测试基建引擎
│   ├── SKILL.md                    # 审计→框架→冒烟→CI→基线
│   └── references/
│       ├── smoke-templates.md      # Phase1冒烟模板(5语言)
│       ├── github-actions-ci-template.yml  # GHA模板(5语言+缓存+Codecov+Slack)
│       ├── gitlab-ci-template.yml  # GitLab CI两阶段
│       └── universal-ci-template.yml # 通用Docker+Bash(含Rust/Java完整示例)
├── examples/                       # 4场景示例
└── test-fixtures/                  # Buggy项目(练习用)
```

## 许可证

MIT © 2026
