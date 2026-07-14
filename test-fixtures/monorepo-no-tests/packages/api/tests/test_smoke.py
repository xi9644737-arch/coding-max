"""AST-only smoke checks; do not import FastAPI or start application side effects."""
import ast
import os

APP_DIR = os.path.join(os.path.dirname(__file__), "..", "app")
MAIN_PY = os.path.join(APP_DIR, "main.py")


def test_entry_syntax():
    """The entry module has valid syntax."""
    with open(MAIN_PY, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    assert tree is not None


def test_no_bare_except():
    """Reject bare exception handlers."""
    with open(MAIN_PY, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            assert node.type is not None, (
                f"Bare except at line {node.lineno}; specify an exception type"
            )


def test_routes_defined():
    """At least one FastAPI route and the health endpoint exist."""
    with open(MAIN_PY, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    routes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and hasattr(node.func, "attr"):
            if node.func.attr in ("get", "post", "put", "delete", "patch"):
                routes.append(node.func.attr.upper())
    assert len(routes) >= 1, "Expected at least one route"
    # Verify the known health route.
    route_paths = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and hasattr(node.func, "attr"):
            if node.func.attr in ("get", "post", "put", "delete", "patch"):
                if node.args:
                    route_paths.add(node.args[0].value if isinstance(node.args[0], ast.Constant) else str(node.args[0]))
    assert "/health" in route_paths, "Missing /health route"


def test_no_mutable_default_args():
    """Reject mutable default arguments."""
    with open(MAIN_PY, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    raise AssertionError(
                        f"Function {node.name} has a mutable default at line {default.lineno}"
                    )
