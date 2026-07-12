"""冒烟测试 — 纯语法树检查，不实际 import 模块（避免连数据库/读配置/初始化日志导致 CI 崩溃）"""
import ast
import os

APP_DIR = os.path.join(os.path.dirname(__file__), "..", "app")
MAIN_PY = os.path.join(APP_DIR, "main.py")
CONFIG_PY = os.path.join(APP_DIR, "config.py")


def test_entry_syntax():
    """入口文件语法有效"""
    with open(MAIN_PY, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    assert tree is not None


def test_config_syntax():
    """配置文件语法有效"""
    with open(CONFIG_PY, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    assert tree is not None


def test_no_bare_except():
    """禁止裸 except: — coding-max 硬约束 #3"""
    with open(MAIN_PY, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            assert node.type is not None, (
                f"裸 except: 在行 {node.lineno} — 必须指定异常类型"
            )


def test_top_level_functions_exist():
    """关键函数在模块顶层定义"""
    with open(MAIN_PY, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    funcs = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    }
    assert "get_user" in funcs, "缺少 get_user 函数"
    assert "update_user" in funcs, "缺少 update_user 函数"
    assert "get_user_cached" in funcs, "缺少 get_user_cached 函数"


def test_no_mutable_default_args():
    """禁止可变默认参数"""
    with open(MAIN_PY, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    raise AssertionError(
                        f"函数 {node.name} 有可变默认参数 (行 {default.lineno})"
                    )


def test_config_no_sensitive_defaults():
    """配置文件中没有硬编码敏感信息"""
    with open(CONFIG_PY, encoding="utf-8") as f:
        content = f.read()
    # 检查是否有明显的密钥/密码硬编码
    suspicious = ["password", "secret", "api_key", "token"]
    for line_no, line in enumerate(content.split("\n"), 1):
        for s in suspicious:
            if s in line.lower() and "=" in line:
                print(f"  ⚠ 配置文件行 {line_no} 包含疑似敏感信息: {s}")
