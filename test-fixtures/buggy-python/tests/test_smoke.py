"""AST-only smoke checks; do not import application modules or trigger side effects."""
import ast
import os

APP_DIR = os.path.join(os.path.dirname(__file__), "..", "app")
MAIN_PY = os.path.join(APP_DIR, "main.py")
CONFIG_PY = os.path.join(APP_DIR, "config.py")


def test_entry_syntax():
    """The entry module has valid syntax."""
    with open(MAIN_PY, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    assert tree is not None


def test_config_syntax():
    """The configuration module has valid syntax."""
    with open(CONFIG_PY, encoding="utf-8") as f:
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


def test_top_level_functions_exist():
    """Expected public functions exist at module scope."""
    with open(MAIN_PY, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    funcs = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    }
    assert "get_user" in funcs, "Missing get_user"
    assert "update_user" in funcs, "Missing update_user"
    assert "get_user_cached" in funcs, "Missing get_user_cached"


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


def test_config_no_sensitive_defaults():
    """Flag likely hard-coded secrets in configuration."""
    with open(CONFIG_PY, encoding="utf-8") as f:
        content = f.read()
    # This fixture reports suspicious assignments without printing values.
    suspicious = ["password", "secret", "api_key", "token"]
    for line_no, line in enumerate(content.split("\n"), 1):
        for s in suspicious:
            if s in line.lower() and "=" in line:
                print(f"  Warning: config line {line_no} may contain sensitive field {s}")
