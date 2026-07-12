"""冒烟测试 — 纯语法树检查，不实际 import FastAPI（避免启动服务器/连数据库/读配置导致 CI 崩溃）"""
import ast
import os

APP_DIR = os.path.join(os.path.dirname(__file__), "..", "app")
MAIN_PY = os.path.join(APP_DIR, "main.py")


def test_entry_syntax():
    """入口文件语法有效"""
    with open(MAIN_PY, encoding="utf-8") as f:
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


def test_routes_defined():
    """FastAPI 路由装饰器存在"""
    with open(MAIN_PY, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    routes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and hasattr(node.func, "attr"):
            if node.func.attr in ("get", "post", "put", "delete", "patch"):
                routes.append(node.func.attr.upper())
    assert len(routes) >= 1, "至少应定义 1 个路由"
    # 验证已知路由
    route_paths = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and hasattr(node.func, "attr"):
            if node.func.attr in ("get", "post", "put", "delete", "patch"):
                if node.args:
                    route_paths.add(node.args[0].value if isinstance(node.args[0], ast.Constant) else str(node.args[0]))
    assert "/health" in route_paths, "缺少 /health 健康检查路由"


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
