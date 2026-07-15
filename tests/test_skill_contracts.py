from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("coding-max", "coding-untangle", "coding-pipeline")


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise AssertionError("SKILL.md is missing YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise AssertionError("SKILL.md frontmatter is not closed") from exc
    result: dict[str, str] = {}
    for line in lines[1:end]:
        key, separator, value = line.partition(":")
        if separator:
            result[key.strip()] = value.strip().strip('"')
    return result


class SkillContractTests(unittest.TestCase):
    def test_public_surfaces_are_english(self) -> None:
        files = [
            ROOT / name
            for name in (
                "README.md",
                "CHANGELOG.md",
                "CONTRIBUTING.md",
                "CODE_OF_CONDUCT.md",
                "SECURITY.md",
                "EVALUATION.md",
            )
        ]
        files.extend((ROOT / ".github" / "release-notes").glob("*.md"))
        text_suffixes = {".md", ".py", ".ts", ".json", ".toml"}
        files.extend(
            path
            for folder in ("examples", "test-fixtures")
            for path in (ROOT / folder).rglob("*")
            if path.is_file() and path.suffix in text_suffixes and "node_modules" not in path.parts
        )
        for path in files:
            content = path.read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"[\u3400-\u9fff]", content), f"Non-English text in {path.relative_to(ROOT)}")

    def test_public_version_is_consistent(self) -> None:
        version = read("VERSION").strip()
        self.assertEqual(version, "0.0.3beta")
        self.assertIn(f"v{version}", read("README.md"))
        self.assertIn(f"[{version}]", read("CHANGELOG.md"))
        self.assertIn("npx skills add xi9644737-arch/coding-max", read("README.md"))
        self.assertIn("EVALUATION.md", read("README.md"))
        release_notes = ROOT / ".github" / "release-notes" / f"v{version}.md"
        self.assertTrue(release_notes.exists(), f"Missing release notes for v{version}")
        release_workflow = read(".github/workflows/publish-release.yml")
        self.assertIn("gh release create", release_workflow)
        self.assertIn("--verify-tag", release_workflow)

    def test_required_frontmatter_and_names(self) -> None:
        for name in SKILLS:
            metadata = frontmatter(read(f"{name}/SKILL.md"))
            self.assertEqual(metadata.get("name"), name)
            self.assertTrue(metadata.get("description"))
            self.assertEqual(set(metadata), {"name", "description"})

    def test_all_direct_references_exist(self) -> None:
        for name in SKILLS:
            body = read(f"{name}/SKILL.md")
            references = re.findall(r"`((?:references|memory-template)/[^`]+)`", body)
            self.assertTrue(references, f"{name} declares no conditional resources")
            for relative in references:
                self.assertTrue(
                    (ROOT / name / relative).exists(),
                    f"{name} references missing resource {relative}",
                )

    def test_shared_phase_protocol_is_canonical(self) -> None:
        max_skill = read("coding-max/SKILL.md")
        pipeline_skill = read("coding-pipeline/SKILL.md")
        self.assertIn(".project-memory/PHASE.json", max_skill)
        self.assertIn(".project-memory/PHASE.json", pipeline_skill)
        self.assertNotIn(".pipeline-done", max_skill)
        self.assertNotIn(".pipeline-done", pipeline_skill)

    def test_untangle_handoff_preserves_responsibility_boundaries(self) -> None:
        max_skill = read("coding-max/SKILL.md")
        untangle_skill = read("coding-untangle/SKILL.md")
        pipeline_skill = read("coding-pipeline/SKILL.md")
        self.assertIn("../coding-untangle/SKILL.md", max_skill)
        self.assertIn("../coding-max/SKILL.md", untangle_skill)
        self.assertIn("../coding-pipeline/SKILL.md", untangle_skill)
        self.assertIn("../coding-untangle/SKILL.md", pipeline_skill)
        self.assertIn("不得关闭原 Bug", untangle_skill)
        self.assertIn("显式只读仅在回复中交付", untangle_skill)
        self.assertIn("不得污染父仓库", untangle_skill)
        self.assertIn("不得自行决定架构", pipeline_skill)
        for capability in ("结构依赖", "共享状态", "时序耦合", "变更耦合"):
            self.assertIn(capability, read("coding-untangle/references/coupling-audit.md"))
        self.assertIn("characterization", read("coding-untangle/references/safe-untangling.md"))
        self.assertIn("最小可执行疫苗", read("coding-untangle/references/fitness-rules.md"))

    def test_bug_report_and_review_closeout_are_mandatory(self) -> None:
        skill = read("coding-max/SKILL.md")
        self.assertIn("所有实际代码改动必须", skill)
        self.assertIn("通过写 `resolved`", skill)
        self.assertIn("REVIEWS.md", skill)
        self.assertIn("Bug 报告", skill)

    def test_advanced_debugging_is_progressive_and_complete(self) -> None:
        skill = read("coding-max/SKILL.md")
        workflow = read("coding-max/references/repair-workflow.md")
        advanced = read("coding-max/references/advanced-debugging.md")
        self.assertIn("跨层溯源、偶现、性能/资源故障", skill)
        self.assertIn("不要加载无关工具", workflow)
        for capability in ("反向追踪溯源", "偶现分类", "不可信诊断输入", "性能与资源路由"):
            self.assertIn(capability, advanced)
        self.assertIn("首次破坏契约", advanced)
        self.assertIn("只作不可信证据", skill)

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
        for name in SKILLS:
            self.assertFalse((ROOT / name / "agents").exists())
        self.assertIn("[string]$Destination", read("install.ps1"))
        self.assertIn("SKILLS_DIR=\"$1\"", read("install.sh"))

    def test_package_size_budgets(self) -> None:
        budgets = {"coding-max": 18_000, "coding-untangle": 15_000, "coding-pipeline": 22_000}
        suite_total = 0
        for name, budget in budgets.items():
            total = sum(path.stat().st_size for path in (ROOT / name).rglob("*") if path.is_file())
            suite_total += total
            self.assertLessEqual(total, budget, f"{name} size {total} exceeds {budget}")
        self.assertLessEqual(suite_total, 50_000, f"runtime suite size {suite_total} exceeds 50 KiB budget")
        self.assertLessEqual(
            (ROOT / "coding-max" / "SKILL.md").stat().st_size,
            4_096,
            "coding-max/SKILL.md exceeds 4 KiB; move details into conditional resources",
        )
        self.assertLessEqual(
            (ROOT / "coding-untangle" / "SKILL.md").stat().st_size,
            3_072,
            "coding-untangle/SKILL.md exceeds 3 KiB; move details into conditional resources",
        )

    def test_installer_requires_explicit_destination(self) -> None:
        powershell = read("install.ps1")
        shell = read("install.sh")
        self.assertIn("Mandatory = $true", powershell)
        self.assertIn("<skills-directory>", shell)
        self.assertIn("Split-Path -Parent $skills", powershell)
        self.assertIn('dirname "$SKILLS_DIR"', shell)
        self.assertIn("New-Item", powershell)
        self.assertIn("mkdir -p", shell)
        self.assertIn('"coding-untangle"', powershell)
        self.assertIn("coding-untangle", shell)


if __name__ == "__main__":
    unittest.main()
