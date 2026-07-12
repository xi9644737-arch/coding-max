# 🪦 coding-max + coding-pipeline

> 根因修复 + 测试基建。两把刀，不绑定任何平台。

<p align="center">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue">
  <img alt="Format" src="https://img.shields.io/badge/format-Markdown%20%2B%20YAML-lightgrey">
  <img alt="Skills" src="https://img.shields.io/badge/skills-2-orange">
</p>

---

AI 修 bug 最大的问题不是修不好，是**假装修好了**。加个 if-else 把异常吞掉、包层 try-catch 让报错消失、改个常量值碰运气——代码不炸了，根因还在。另一个问题是**没测试还硬修**——改了代码没有安全网，越修越慌。

| Skill | 干什么 | 一句话 |
|-------|--------|--------|
| `coding-max` | 根因修复引擎 | 4 模式、9 步骤、10 硬约束、7 自欺红旗 |
| `coding-pipeline` | 测试基建 | 审计→搭框架→冒烟测试→CI→增量覆盖率基线 |

两个 skill 通过 PHASE 锁联动：coding-max 探测到无测试→拦截→coding-pipeline 搭管道→回 coding-max 正常修。

---

## coding-max：四种模式，一个引擎

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

## 快速预览

**你说：** "用户列表接口偶尔 500，日志里是 `KeyError: 'display_name'`"

**coding-max（Quick 模式）：**

```
初审→user_service.py:142→5 Whys→根因:老用户缺字段+逻辑分散
RED→GREEN(.get兜底)→REFACTOR(提取公共函数)→自检→14/14通过
```

**coding-pipeline（搭基建）：**

```
审计→Monorepo(web+api)→装pytest+vitest→语法树冒烟→GitHub Actions→增量基线84%
```

更多 → [`examples/`](examples/)

---

## 怎么装

```bash
# 克隆整个仓库（含两个 skill）
git clone https://github.com/xi9644737-arch/coding-max.git

# Claude Code — 复制或链接到 skills 目录
cp -r coding-max/coding-max ~/.claude/skills/coding-max
cp -r coding-max/coding-pipeline ~/.claude/skills/coding-pipeline

# 一行安装（Windows）
irm https://raw.githubusercontent.com/xi9644737-arch/coding-max/master/install.ps1 | iex

# 一行安装（macOS/Linux）
curl -fsSL https://raw.githubusercontent.com/xi9644737-arch/coding-max/master/install.sh | bash
```

其他 AI Agent：将 `coding-max/SKILL.md` 和 `coding-pipeline/SKILL.md` 放到你工具的规则/指令目录。
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

## coding-pipeline：渐进式补全

审计→缺什么补什么。**只通管道不写业务测试。**

| 步骤 | 干了什么 |
|------|---------|
| 0. 审计 | Glob/Grep 探测语言/框架/CI/覆盖率, Monorepo 递归子包 |
| 1. 装框架 | Python(pytest)/Node(vitest/jest)/Go(testing), 其他给通用模板 |
| 2. 脚手架 | 纯语法树冒烟测试(`ast.parse`/`acorn`), 不实际 import |
| 3. 生成 CI | GitHub Actions: push+PR, 矩阵, checkout→装依赖→跑测试→上传覆盖率 |
| 4. 增量基线 | git diff 追踪增量行覆盖率, 不卡全局%, 写入 PROJECT_PROFILE |

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
├── coding-max/                 # 根因修复引擎
│   ├── SKILL.md                # 主引擎
│   ├── references/
│   │   ├── patch-signals.md    # 补丁信号 + 认知红旗 + 架构异味
│   │   └── bug-memory-format.md # 病历格式 + 疫苗映射 + 修复范例
│   └── memory-template/        # 病历/画像/断点模板
├── coding-pipeline/            # 测试基建引擎
│   └── SKILL.md                # 审计→框架→CI→基线
└── examples/                   # 4个场景示例
```

## 许可证

MIT © 2026
