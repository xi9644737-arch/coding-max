from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise AssertionError("SKILL.md 缺少 YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise AssertionError("SKILL.md frontmatter 未闭合") from exc
    result: dict[str, str] = {}
    for line in lines[1:end]:
        key, separator, value = line.partition(":")
        if separator:
            result[key.strip()] = value.strip().strip('"')
    return result


class SkillContractTests(unittest.TestCase):
    def test_required_frontmatter_and_names(self) -> None:
        for name in ("coding-max", "coding-pipeline"):
            metadata = frontmatter(read(f"{name}/SKILL.md"))
            self.assertEqual(metadata.get("name"), name)
            self.assertTrue(metadata.get("description"))
            self.assertEqual(set(metadata), {"name", "description"})

    def test_all_direct_references_exist(self) -> None:
        for name in ("coding-max", "coding-pipeline"):
            body = read(f"{name}/SKILL.md")
            references = re.findall(r"`((?:references|memory-template)/[^`]+)`", body)
            self.assertTrue(references, f"{name} 没有声明按需资源")
            for relative in references:
                self.assertTrue(
                    (ROOT / name / relative).exists(),
                    f"{name} 引用了不存在的 {relative}",
                )

    def test_shared_phase_protocol_is_canonical(self) -> None:
        max_skill = read("coding-max/SKILL.md")
        pipeline_skill = read("coding-pipeline/SKILL.md")
        self.assertIn(".project-memory/PHASE.json", max_skill)
        self.assertIn(".project-memory/PHASE.json", pipeline_skill)
        self.assertNotIn(".pipeline-done", max_skill)
        self.assertNotIn(".pipeline-done", pipeline_skill)

    def test_bug_report_and_review_closeout_are_mandatory(self) -> None:
        skill = read("coding-max/SKILL.md")
        self.assertIn("所有实际代码改动必须", skill)
        self.assertIn("通过写 `resolved`", skill)
        self.assertIn("REVIEWS.md", skill)
        self.assertIn("Bug 报告", skill)

    def test_javascript_smoke_does_not_reject_normal_catch_binding(self) -> None:
        sources = "\n".join(
            [
                read("coding-pipeline/references/smoke-templates.md"),
                read("coding-pipeline/references/github-actions-ci-template.yml"),
                read("coding-pipeline/references/gitlab-ci-template.yml"),
            ]
        )
        bad_pattern = r"catch\\s\*\\\(\\s\*\\w\*\\s\*\\\)\\s\*\\\{"
        self.assertNotIn(bad_pattern, sources)
        self.assertIn("--check", sources)

    def test_gitlab_template_requires_bound_image_and_matrix(self) -> None:
        template = read("coding-pipeline/references/gitlab-ci-template.yml")
        self.assertIn("image: __TOOLCHAIN_IMAGE__", template)
        self.assertIn("parallel:", template)
        self.assertNotIn("image: python:3.12", template)

    def test_skills_are_vendor_neutral(self) -> None:
        for name in ("coding-max", "coding-pipeline"):
            self.assertFalse((ROOT / name / "agents").exists())
        self.assertIn("[string]$Destination", read("install.ps1"))
        self.assertIn("SKILLS_DIR=\"$1\"", read("install.sh"))

    def test_package_size_budgets(self) -> None:
        budgets = {"coding-max": 18_000, "coding-pipeline": 22_000}
        for name, budget in budgets.items():
            total = sum(path.stat().st_size for path in (ROOT / name).rglob("*") if path.is_file())
            self.assertLessEqual(total, budget, f"{name} 体积 {total} 超过 {budget}")

    def test_installer_requires_explicit_destination(self) -> None:
        powershell = read("install.ps1")
        shell = read("install.sh")
        self.assertIn("Mandatory = $true", powershell)
        self.assertIn("<skills-directory>", shell)
        self.assertIn("Split-Path -Parent $skills", powershell)
        self.assertIn('dirname "$SKILLS_DIR"', shell)
        self.assertIn("New-Item", powershell)
        self.assertIn("mkdir -p", shell)


if __name__ == "__main__":
    unittest.main()
