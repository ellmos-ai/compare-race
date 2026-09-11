"""Contract and hygiene tests for compare-race repository metadata.

Verifies PEP 621 compliance, .gitignore hygiene, CI matrix configuration,
bilingual documentation parity, security policy, and front-matter parsing contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read_text(relative_path: str) -> str:
    path = REPO_ROOT / relative_path
    assert path.exists(), f"Expected file {relative_path} does not exist"
    return path.read_text(encoding="utf-8")


def test_gitignore_hygiene():
    """Verify .gitignore contains essential security, lock, cache, and sync patterns."""
    content = _read_text(".gitignore")
    lines = {
        line.strip()
        for line in content.splitlines()
        if line.strip() and not line.startswith("#")
    }

    required_patterns = [
        "__pycache__/",
        "*.pyc",
        ".pytest_cache/",
        ".ruff_cache/",
        ".coverage",
        ".env",
        "*.db",
        "*-conflict-*",
        "*.sync-conflict-*",
        "*.sync-temp-*",
        "LOCK",
        "LOCK.*",
        "LOCK*.txt",
        "*.lock",
        "data/",
        "races/",
        "compare-race.config.json",
    ]
    for pattern in required_patterns:
        assert pattern in lines, f"Missing required .gitignore pattern: {pattern}"


def test_pyproject_pep621_metadata():
    """Verify pyproject.toml adheres to PEP 621 standard metadata fields."""
    if sys.version_info >= (3, 11):
        import tomllib
        with open(REPO_ROOT / "pyproject.toml", "rb") as f:
            data = tomllib.load(f)
    else:
        import tomli as tomllib
        with open(REPO_ROOT / "pyproject.toml", "rb") as f:
            data = tomllib.load(f)

    project = data.get("project", {})
    assert project.get("name") == "compare-race"
    import compare_race
    assert project.get("version") == compare_race.__version__
    assert "description" in project
    assert project.get("requires-python") == ">=3.10"
    assert project.get("license") == {"text": "MIT"}

    # Authors
    authors = project.get("authors", [])
    assert any(a.get("name") == "Lukas Geiger" for a in authors)

    # Keywords & Classifiers
    keywords = project.get("keywords", [])
    assert "benchmark" in keywords
    assert "evaluation" in keywords

    classifiers = project.get("classifiers", [])
    assert "Programming Language :: Python :: 3.10" in classifiers
    assert "Programming Language :: Python :: 3.11" in classifiers
    assert "Programming Language :: Python :: 3.12" in classifiers

    # URLs
    urls = project.get("urls", {})
    assert urls.get("Homepage") == "https://github.com/ellmos-ai/compare-race"
    assert urls.get("Repository") == "https://github.com/ellmos-ai/compare-race"
    assert urls.get("Issues") == "https://github.com/ellmos-ai/compare-race/issues"
    assert urls.get("Changelog") == "https://github.com/ellmos-ai/compare-race/blob/master/CHANGELOG.md"
    assert urls.get("Documentation") == "https://github.com/ellmos-ai/compare-race#readme"
    assert urls.get("Security") == "https://github.com/ellmos-ai/compare-race/blob/master/SECURITY.md"
    assert urls.get("Third-Party Licenses") == "https://github.com/ellmos-ai/compare-race/blob/master/THIRD_PARTY_LICENSES.md"
    assert urls.get("Marketing Log") == "https://github.com/ellmos-ai/compare-race/blob/master/MARKETING-LOG.txt"
    assert urls.get("Parent Organization") == "https://github.com/ellmos-ai"
    assert urls.get("Umbrella Ecosystem") == "https://github.com/open-bricks"

    # Optional test dependencies
    opt_deps = project.get("optional-dependencies", {})
    assert "test" in opt_deps
    assert any("pytest" in d for d in opt_deps["test"])
    assert any("ruff" in d for d in opt_deps["test"])


def test_ci_matrix_workflow_definition():
    """Verify GitHub Actions CI matrix tests Python 3.10, 3.11, and 3.12."""
    content = _read_text(".github/workflows/ci.yml")
    assert "name: CI" in content
    assert 'matrix:' in content
    assert '"3.10"' in content
    assert '"3.11"' in content
    assert '"3.12"' in content
    assert "compileall" in content
    assert "ruff check ." in content
    assert "pytest" in content


def test_security_policy_present_and_sla():
    """Verify SECURITY.md is present with 48h SLA response and contacts."""
    content = _read_text("SECURITY.md")
    assert "48 hours" in content or "48 Stunden" in content
    assert "5 business days" in content or "5 Werktagen" in content
    assert "security@open-bricks.org" in content
    assert "security@ellmos.ai" in content


def test_readme_bilingual_parity():
    """Verify presence and cross-links between English and German READMEs."""
    en_content = _read_text("README.md")
    de_content = _read_text("README_de.md")

    assert "Deutsche Fassung" in en_content or "README_de.md" in en_content
    assert "English version" in de_content or "README.md" in de_content

    # Both must display the header banner
    assert "assets/banner.png" in en_content
    assert "assets/banner.png" in de_content


def test_readme_navigation_anchor_parity():
    """Verify 15-point quick navigation and identical anchor links in both READMEs."""
    import re
    en_content = _read_text("README.md")
    de_content = _read_text("README_de.md")

    en_links = re.findall(r"^\d+\.\s+\[.+?\]\((#.+?)\)", en_content, re.MULTILINE)
    de_links = re.findall(r"^\d+\.\s+\[.+?\]\((#.+?)\)", de_content, re.MULTILINE)

    assert len(en_links) == 15, f"Expected 15 navigation links in README.md, got {len(en_links)}"
    assert len(de_links) == 15, f"Expected 15 navigation links in README_de.md, got {len(de_links)}"

    # Check Mermaid diagrams present in both
    for content, lang in [(en_content, "EN"), (de_content, "DE")]:
        assert "```mermaid\nflowchart TD" in content, f"Missing flowchart TD in {lang}"
        assert "```mermaid\nsequenceDiagram" in content, f"Missing sequenceDiagram in {lang}"


def test_governance_invariants_table():
    """Verify all 10 canonical runtime invariants (INV-LOCAL-01 to INV-SLA-10) are documented."""
    en_content = _read_text("README.md")
    de_content = _read_text("README_de.md")
    llms_content = _read_text("llms.txt")
    licenses_content = _read_text("THIRD_PARTY_LICENSES.md")
    marketing_content = _read_text("MARKETING-LOG.txt")

    invariants = [
        "INV-LOCAL-01", "INV-SEC-02", "INV-AXIS-03", "INV-JUDGE-04",
        "INV-ISOL-05", "INV-FAIL-06", "INV-BUNDLE-07", "INV-INTEROP-08",
        "INV-LIC-09", "INV-SLA-10",
    ]
    licenses_invariants = {
        "INV-LOCAL-01", "INV-SEC-02", "INV-AXIS-03", "INV-JUDGE-04",
        "INV-ISOL-05", "INV-FAIL-06", "INV-BUNDLE-07",
    }
    for inv_key in invariants:
        assert inv_key in en_content, f"Missing {inv_key} in README.md"
        assert inv_key in de_content, f"Missing {inv_key} in README_de.md"
        assert inv_key in llms_content, f"Missing {inv_key} in llms.txt"
        assert inv_key in marketing_content, f"Missing {inv_key} in MARKETING-LOG.txt"
        if inv_key in licenses_invariants:
            assert inv_key in licenses_content, f"Missing {inv_key} in THIRD_PARTY_LICENSES.md"


def test_third_party_licenses_audit():
    """Verify THIRD_PARTY_LICENSES.md audits dependencies and guarantees permissive licensing."""
    content = _read_text("THIRD_PARTY_LICENSES.md")
    assert "Zero-Egress" in content
    assert "RunAsInvoker" in content
    assert "system-auditor" in content
    assert "coma" in content
    assert "pytest" in content
    assert "ruff" in content
    assert "PSFL-2.0" in content
    assert "MIT License" in content


def test_marketing_log_contract():
    """Verify MARKETING-LOG.txt exists with personas, keywords, and competitive matrix."""
    content = _read_text("MARKETING-LOG.txt")
    assert "1. REPOSITORY AUDIT & DISCOVERABILITY BASELINE" in content
    assert "2. TARGET PERSONAS & USER JOURNEYS" in content
    assert "3. HIGH-INTENT SEARCH QUERIES" in content
    assert "4. COMPETITIVE DIFFERENTIATION MATRIX" in content
    assert "5. GOVERNANCE & RUNTIME INVARIANTS" in content
    assert "Benchmarking Engineers" in content
    assert "Enterprise Tooling" in content


def test_front_matter_contract_roundtrip_all_fields():
    """Contract test: Ensure all run_front_matter fields roundtrip through system-auditor parser."""
    from system_auditor.report import parse_front_matter

    from compare_race.race import RunResult, run_front_matter
    from compare_race.tokens import plan_race

    plan = plan_race("Solve 2+2", models=["lane-alpha"], system="TEST-HOST", variants=["prompt-v2"])
    result = RunResult(
        identity=plan.runs[0],
        backend="fake",
        ok=True,
        output="4",
        latency_s=0.85,
        started_utc="2026-09-10T00:00:00Z",
        finished_utc="2026-09-10T00:00:01Z",
        cost_gear="claude-3-5-sonnet",
        est_cost_usd=0.0012,
        checks_passed=["format-ok", "result-correct"],
        checks_failed=[],
    )

    rendered = run_front_matter(result, plan)
    parsed = parse_front_matter(rendered)

    assert parsed["race_id"] == plan.race_id
    assert parsed["model"] == "lane-alpha"
    assert parsed["system"] == "TEST-HOST"
    assert parsed["variant"] == "prompt-v2"
    assert parsed["backend"] == "fake"
    assert parsed["mode"] == "sequential"
    assert float(parsed["latency_s"]) == 0.85
    assert parsed["ok"] is True
    assert parsed["cost_gear"] == "claude-3-5-sonnet"
    assert float(parsed["est_cost_usd"]) == 0.0012
    assert "format-ok" in str(parsed["checks_passed"])
    assert "result-correct" in str(parsed["checks_passed"])
