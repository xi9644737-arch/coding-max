from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import validate


ROOT = Path(__file__).resolve().parent


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def expand(value: str, workspace: Path) -> str:
    return (
        value.replace("{python}", sys.executable)
        .replace("{workspace}", str(workspace))
        .replace("{benchmark_root}", str(ROOT))
    )


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(root)
        if "__pycache__" in relative.parts or relative.suffix in {".pyc", ".pyo"}:
            continue
        digest.update(relative.as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def git_commit(workspace: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(workspace), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def expectation_found(output: str, expected: dict) -> bool:
    for line in output.splitlines():
        if expected["contains"] in line and line.rstrip().endswith(
            f"... {expected['outcome']}"
        ):
            return True
    return False


def execute(command: dict, workspace: Path) -> dict:
    argv = [expand(item, workspace) for item in command["argv"]]
    cwd = (workspace / command["cwd"]).resolve()
    if not validate.contained(cwd, workspace) or not cwd.is_dir():
        raise SystemExit(f"evaluator cwd escapes workspace: {command['id']}")
    overrides = {key: expand(value, workspace) for key, value in command["env"].items()}
    environment = os.environ.copy()
    environment.update(overrides)
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    combined = result.stdout + "\n" + result.stderr
    tests_match = all(
        expectation_found(combined, expectation)
        for expectation in command["expected_tests"]
    )
    output_digest = hashlib.sha256(
        (result.stdout + "\0" + result.stderr).encode("utf-8")
    ).hexdigest()
    return {
        "artifact_id": f"command:{command['id']}",
        "argv": argv,
        "cwd": str(cwd),
        "env": overrides,
        "exit_code": result.returncode,
        "expected_exit": command["expected_exit"],
        "stdout": result.stdout,
        "stderr": result.stderr,
        "output_sha256": output_digest,
        "expected_tests": command["expected_tests"],
        "expectations_met": result.returncode == command["expected_exit"]
        and tests_match,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run trusted evaluator checks and capture immutable host evidence."
    )
    parser.add_argument("case_id", choices=sorted(validate.EXPECTED))
    parser.add_argument("workspace", type=Path)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    validate.main()
    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        raise SystemExit(f"workspace does not exist: {workspace}")
    validate.reject_symlinks(workspace)
    manifest_path = args.manifest.resolve()
    if validate.contained(manifest_path, workspace):
        raise SystemExit("manifest must remain outside the exposed workspace")
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    truth = validate.load(ROOT / "ground-truth" / f"{args.case_id}.json")
    started = utc_now()
    before = tree_digest(workspace)
    commands = [execute(command, workspace) for command in truth["evaluator_commands"]]
    after = tree_digest(workspace)
    manifest = {
        "schema_version": 1,
        "case_id": args.case_id,
        "provenance": {
            "captured_by": "evaluator",
            "capture_method": "subprocess",
            "started_at": started,
            "finished_at": utc_now(),
            "repository_commit": git_commit(workspace),
        },
        "workspace_snapshots": {
            "before_evaluation": before,
            "after_evaluation": after,
        },
        "commands": commands,
        "passed": all(command["expectations_met"] for command in commands),
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(manifest_path)
    raise SystemExit(0 if manifest["passed"] else 1)


if __name__ == "__main__":
    main()
