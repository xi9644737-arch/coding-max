# buggy-python

测试 `coding-max` 用的 Python 项目，包含 3 个已知 bug，**无测试**。

## 种植的 Bug

| # | 文件:行 | 类型 | 触发方式 |
|---|---------|------|---------|
| 1 | `app/main.py:17` | KeyError | 调用 `get_user(2)` — 用户缺 `email` 字段 |
| 2 | `app/main.py:30` | 裸 except | 调用 `update_user(1, {"bad_field": ...})` — 异常被吞 |
| 3 | `app/main.py:41` | 竞态条件 | `_cache` 全局变量无锁保护 |

## 测试方式

复制到你的项目目录，对 AI 说：

> "这个项目有个用户管理模块，帮我看看有没有 bug"

观察 coding-max 是否能：
1. 自动探测到 3 个 bug
2. 走 Quick/Standard 流程
3. 不自欺（比如只修 KeyError 不加 .get()，而是追踪同类模式）
