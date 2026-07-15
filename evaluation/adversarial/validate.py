from __future__ import annotations

import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED = {"misleading-timeout", "dirty-baseline", "green-but-slow"}
PUBLIC_KEYS = {"id", "workspace", "prompt", "observable", "required_artifacts"}
COMMAND_KEYS = {
    "id",
    "argv",
    "cwd",
    "env",
    "expected_exit",
    "expected_tests",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def contained(path: Path, parent: Path) -> bool:
    try:
        return os.path.commonpath([path, parent]) == str(parent)
    except ValueError:
        return False


def reject_symlinks(path: Path) -> None:
    for candidate in [path, *path.rglob("*")]:
        if candidate.is_symlink():
            raise SystemExit(f"symlink is not allowed in public workspace: {candidate}")


def validate_command(case_id: str, command: dict) -> None:
    if set(command) != COMMAND_KEYS:
        raise SystemExit(f"invalid evaluator command keys for {case_id}")
    if not command["id"] or not command["argv"]:
        raise SystemExit(f"empty evaluator command for {case_id}")
    if not all(isinstance(item, str) and item for item in command["argv"]):
        raise SystemExit(f"evaluator argv must be non-empty strings for {case_id}")
    if not isinstance(command["expected_exit"], int):
        raise SystemExit(f"expected_exit must be an integer for {case_id}")
    if not isinstance(command["env"], dict) or not isinstance(
        command["expected_tests"], list
    ):
        raise SystemExit(f"invalid evaluator expectations for {case_id}")
    for expectation in command["expected_tests"]:
        if set(expectation) != {"contains", "outcome"}:
            raise SystemExit(f"invalid test expectation for {case_id}")


def main() -> None:
    rubric = load(ROOT / "rubric.json")
    if sum(metric["weight"] for metric in rubric["metrics"]) != 100:
        raise SystemExit("rubric weights must total 100")
    if not rubric["fatal_failures"]:
        raise SystemExit("rubric requires fatal failures")
    if any(len(metric.get("anchors", [])) < 3 for metric in rubric["metrics"]):
        raise SystemExit("every rubric metric requires scoring anchors")
    schema = load(ROOT / rubric["artifact_contract"]["schema"])
    if schema.get("title") != "Adversarial evaluation host-captured run manifest":
        raise SystemExit("run manifest schema is missing or invalid")

    cases = {path.stem: load(path) for path in (ROOT / "cases").glob("*.json")}
    truths = {
        path.stem: load(path) for path in (ROOT / "ground-truth").glob("*.json")
    }
    if set(cases) != EXPECTED or set(truths) != EXPECTED:
        raise SystemExit("case and ground-truth ids must match the benchmark contract")

    public_root = (ROOT / "workspaces").resolve()
    for case_id in EXPECTED:
        public_case = cases[case_id]
        truth = truths[case_id]
        if set(public_case) != PUBLIC_KEYS:
            raise SystemExit(f"public case schema violation for {case_id}")
        if public_case["id"] != case_id or truth.get("id") != case_id:
            raise SystemExit(f"id mismatch for {case_id}")
        if not truth.get("evaluator_only"):
            raise SystemExit(f"ground truth marker missing for {case_id}")
        expected_relative = f"workspaces/{case_id}"
        if Path(public_case["workspace"]).as_posix() != expected_relative:
            raise SystemExit(f"workspace must be {expected_relative}")
        workspace = (ROOT / public_case["workspace"]).resolve()
        if not workspace.is_dir() or not contained(workspace, public_root):
            raise SystemExit(f"workspace escapes public root for {case_id}")
        reject_symlinks(ROOT / public_case["workspace"])
        command_ids: set[str] = set()
        for command in truth.get("evaluator_commands", []):
            validate_command(case_id, command)
            if command["id"] in command_ids:
                raise SystemExit(f"duplicate evaluator command id for {case_id}")
            command_ids.add(command["id"])

    print(
        f"{len(EXPECTED)} adversarial source packages valid; "
        "build_bundle.py is required for runtime isolation"
    )


if __name__ == "__main__":
    main()
