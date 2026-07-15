from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import validate


ROOT = Path(__file__).resolve().parent


def copy_bundle(case_id: str, destination: Path) -> None:
    validate.main()
    case_path = ROOT / "cases" / f"{case_id}.json"
    if not case_path.is_file():
        raise SystemExit(f"unknown case id: {case_id}")
    if destination.exists():
        raise SystemExit(f"destination already exists: {destination}")
    if validate.contained(destination, ROOT.resolve()):
        raise SystemExit("destination must remain outside the benchmark source tree")

    public_case = json.loads(case_path.read_text(encoding="utf-8"))
    workspace = ROOT / public_case["workspace"]
    destination.mkdir(parents=True)
    public_case["workspace"] = "workspace"
    (destination / "case.json").write_text(
        json.dumps(public_case, indent=2) + "\n", encoding="utf-8"
    )
    shutil.copytree(
        workspace,
        destination / "workspace",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a public benchmark bundle without evaluator-only files."
    )
    parser.add_argument("case_id", choices=sorted(validate.EXPECTED))
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    copy_bundle(args.case_id, args.destination.resolve())
    print(args.destination.resolve())


if __name__ == "__main__":
    main()
