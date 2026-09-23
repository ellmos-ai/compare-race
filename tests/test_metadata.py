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
        "*conflicted copy*",
        "*(kopie)*",
        "*-WORKSTATION-*",
        "*-ASUS-*",
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
    assert project.get("license-files") == ["LICENSE", "NOTICE", "THIRD_PARTY_LICENSES.md"]

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
    assert "Programming Language :: Python :: 3.13" in classifiers

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
    assert urls.get("LLM Context") == "https://github.com/ellmos-ai/compare-race/blob/master/llms.txt"

    # Optional test dependencies
    opt_deps = project.get("optional-dependencies", {})
    assert "test" in opt_deps
    assert any("pytest" in d for d in opt_deps["test"])
    assert any("ruff" in d for d in opt_deps["test"])


def test_ci_matrix_workflow_definition():
    """Verify GitHub Actions CI matrix tests Python 3.10, 3.11, 3.12, 3.13 and has timeout."""
    content = _read_text(".github/workflows/ci.yml")
    assert "name: CI" in content
    assert "timeout-minutes: 15" in content
    assert 'matrix:' in content
    assert '"3.10"' in content
    assert '"3.11"' in content
    assert '"3.12"' in content
    assert '"3.13"' in content
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
    """Verify 18-point quick navigation, dual HTML anchors, and clean Mermaid syntax."""
    import re
    en_content = _read_text("README.md")
    de_content = _read_text("README_de.md")

    en_links = re.findall(r"^\d+\.\s+\[.+?\]\((#.+?)\)", en_content, re.MULTILINE)
    de_links = re.findall(r"^\d+\.\s+\[.+?\]\((#.+?)\)", de_content, re.MULTILINE)

    assert len(en_links) == 18, f"Expected 18 navigation links in README.md, got {len(en_links)}"
    assert len(de_links) == 18, f"Expected 18 navigation links in README_de.md, got {len(de_links)}"

    # Check Mermaid diagrams present in both and semicolon-free
    for content, lang in [(en_content, "EN"), (de_content, "DE")]:
        assert "```mermaid\nflowchart TD" in content, f"Missing flowchart TD in {lang}"
        assert "```mermaid\nsequenceDiagram" in content, f"Missing sequenceDiagram in {lang}"
        mermaid_blocks = re.findall(r"```mermaid\n(.*?)```", content, re.DOTALL)
        for block in mermaid_blocks:
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            for line in lines:
                assert not line.endswith(";"), f"Mermaid line ends with semicolon in {lang}: {line}"

    # Check dual HTML anchors presence across both documents
    anchor_en_1 = (
        '<a id="core-concept--identity"></a><a id="executive-summary--core-identity"></a>'
    )
    anchor_de_1 = (
        '<a id="kernkonzept--identität"></a><a id="executive-summary--core-identity"></a>'
    )
    assert anchor_en_1 in en_content
    assert anchor_de_1 in de_content
    assert '<a id="system-architecture"></a><a id="visual-architecture-topology"></a>' in en_content
    assert '<a id="systemarchitektur"></a><a id="visual-architecture-topology"></a>' in de_content
    assert '<a id="end-to-end-race-lifecycle"></a><a id="sequence-flow"></a>' in en_content
    assert '<a id="end-to-end-renn-lebenszyklus"></a><a id="sequence-flow"></a>' in de_content
    assert '<a id="license"></a><a id="statutory-notice--liability-limitation"></a>' in en_content
    assert '<a id="lizenz"></a><a id="statutory-notice--liability-limitation"></a>' in de_content


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
    for inv_key in invariants:
        assert inv_key in en_content, f"Missing {inv_key} in README.md"
        assert inv_key in de_content, f"Missing {inv_key} in README_de.md"
        assert inv_key in llms_content, f"Missing {inv_key} in llms.txt"
        assert inv_key in marketing_content, f"Missing {inv_key} in MARKETING-LOG.txt"
        assert inv_key in licenses_content, f"Missing {inv_key} in THIRD_PARTY_LICENSES.md"


def test_third_party_licenses_audit():
    """Verify THIRD_PARTY_LICENSES.md audits dependencies and guarantees permissive licensing."""
    content = _read_text("THIRD_PARTY_LICENSES.md")
    assert "Level 1 SBOM" in content
    assert "Zero-Egress" in content
    assert "RunAsInvoker" in content
    assert "system-auditor" in content
    assert "coma" in content
    assert "pytest" in content
    assert "ruff" in content
    assert "PSFL-2.0" in content
    assert "MIT License" in content
    assert "Zero-Copyleft Guarantee" in content
    assert "NOTICE" in content


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
    assert "9. MARKETING & DISCOVERABILITY PARITY UPGRADE (PFAD B)" in content


def test_target_personas_sections():
    """Verify target personas [PERSONA-01] to [PERSONA-04] in both READMEs."""
    en_content = _read_text("README.md")
    de_content = _read_text("README_de.md")
    personas = ["[PERSONA-01]", "[PERSONA-02]", "[PERSONA-03]", "[PERSONA-04]"]
    for p in personas:
        assert p in en_content, f"Missing {p} in README.md"
        assert p in de_content, f"Missing {p} in README_de.md"


def test_comparative_matrix_sections():
    """Verify 10-dimension comparative matrix vs. alternatives in both READMEs."""
    en_content = _read_text("README.md")
    de_content = _read_text("README_de.md")
    for content, lang in [(en_content, "EN"), (de_content, "DE")]:
        assert "LMSYS Chatbot Arena" in content, f"Missing LMSYS Chatbot Arena in {lang}"
        assert "lm-evaluation-harness" in content, f"Missing lm-evaluation-harness in {lang}"
        assert "INV-LOCAL-01" in content, f"Missing INV-LOCAL-01 in {lang}"
        assert "INV-SLA-10" in content, f"Missing INV-SLA-10 in {lang}"


def test_statutory_disclaimer_521_bgb():
    """Verify Section 18 statutory notice and liability limitation (§ 521 BGB)."""
    en_content = _read_text("README.md")
    de_content = _read_text("README_de.md")
    for content, lang in [(en_content, "EN"), (de_content, "DE")]:
        assert "§ 521 BGB" in content, f"Missing § 521 BGB in {lang}"
        assert "Gefälligkeitsrecht" in content, f"Missing Gefälligkeitsrecht in {lang}"
        assert "intentional misconduct" in content, f"Missing intentional misconduct in {lang}"


def test_notice_file_exists():
    """Verify NOTICE file exists and contains correct entity attributions."""
    content = _read_text("NOTICE")
    assert "compare-race" in content
    assert "Lukas Geiger" in content
    assert "ellmos-ai" in content
    assert "open-bricks" in content


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


def test_changelog_recent_pfad_a_071_entry():
    """Contract test: Ensure CHANGELOG.md documents [0.7.1] with Pfad A hygiene items."""
    content = _read_text("CHANGELOG.md")
    assert "## [0.7.1] - 2026-09-13" in content
    assert "CI-Timeout-Guardrail" in content
    assert "Multi-Host-Sync-Härtung" in content
    assert "PEP 621" in content


def test_changelog_recent_pfad_b_072_entry():
    """Contract test: Ensure CHANGELOG.md documents [0.7.2] Pfad B release notes."""
    content = _read_text("CHANGELOG.md")
    assert "## [0.7.2] - 2026-09-20" in content
    assert "18-Punkte-Bilinguale Schnellnavigation" in content
    assert "Level 1 SBOM" in content
    assert "§ 521 BGB" in content


def test_llms_txt_version_and_recency():
    """Contract test: Ensure llms.txt reflects v0.7.2, 2026-09-23 audit stamp and green tests."""
    content = _read_text("llms.txt")
    assert "Version: 0.7.2" in content
    assert "Last-checked: 2026-09-23" in content
    assert "Tests: 58 passed (100% green)" in content


def test_level1_sbom_invariant_cross_reference_matrix_completeness():
    """Contract test: Ensure Level 1 SBOM has complete invariant cross-reference table."""
    content = _read_text("THIRD_PARTY_LICENSES.md")
    assert "Level 1 SBOM" in content
    assert "Invariant Cross-Reference Matrix" in content
    assert "Zero-Copyleft Isolation Guarantee & RunAsInvoker Certification" in content
    assert "100% Offline / Zero-Egress" in content
    assert "Non-Elevation (`RunAsInvoker`)" in content
    assert "Six-Axis Attribution Discipline" in content
    assert "Evidence-Aware Fail-Closed Judge" in content


def test_dual_mermaid_diagram_syntax_integrity():
    """Contract test: Ensure dual mermaid diagrams define required subgraphs and actors."""
    en_content = _read_text("README.md")
    de_content = _read_text("README_de.md")
    for content, lang in [(en_content, "EN"), (de_content, "DE")]:
        assert "subgraph CLI" in content, f"Missing subgraph CLI in {lang}"
        assert "subgraph Core" in content, f"Missing subgraph Core in {lang}"
        assert "subgraph Exec" in content, f"Missing subgraph Exec in {lang}"
        assert "subgraph Storage" in content, f"Missing subgraph Storage in {lang}"
        assert "subgraph JudgeLayer" in content, f"Missing subgraph JudgeLayer in {lang}"
        assert "autonumber" in content, f"Missing autonumber in {lang}"
        assert "StarterJudge" in content, f"Missing StarterJudge in {lang}"


def test_lifecycle_workflows_present_and_hardened():
    """Contract test: Ensure CI lifecycle workflows (stale, welcome) are hardened."""
    stale_content = _read_text(".github/workflows/stale.yml")
    assert "timeout-minutes: 10" in stale_content
    assert "cancel-in-progress: true" in stale_content
    assert "issues: write" in stale_content
    assert "pull-requests: write" in stale_content

    welcome_content = _read_text(".github/workflows/welcome.yml")
    assert "timeout-minutes: 5" in welcome_content
    assert "cancel-in-progress: true" in welcome_content
    assert "actions/first-interaction@v3" in welcome_content
    assert "issues: write" in welcome_content
    assert "pull-requests: write" in welcome_content


def test_gitignore_multihost_and_lock_guards():
    """Contract test: Ensure .gitignore guards multi-host conflict files and lock leaks."""
    content = _read_text(".gitignore")
    lines = {
        line.strip()
        for line in content.splitlines()
        if line.strip() and not line.startswith("#")
    }
    required = [
        "*-WORKSTATION-LG*",
        "*-ASUS-GEI*",
        "*-LAPTOP*",
        "*-Mac Studio*",
        "LOCK.user.*",
        "LOCK.until.*",
        "LOCK.condition.*",
        "LOCK.permissions.json",
        "uv.lock",
        "!package-lock.json",
        ".pytest_temp/",
        ".hypothesis/",
        ".turbo/",
    ]
    for pattern in required:
        assert pattern in lines, f"Missing required .gitignore pattern: {pattern}"


def test_pyproject_pep621_hardening_urls_and_pytest():
    """Contract test: Ensure pyproject.toml includes Notice URL and pytest hardening."""
    content = _read_text("pyproject.toml")
    assert 'Notice = "https://github.com/ellmos-ai/compare-race/blob/master/NOTICE"' in content
    assert 'minversion = "7.0"' in content
    assert "norecursedirs" in content


def test_changelog_unreleased_pfad_a_entry():
    """Contract test: Ensure CHANGELOG.md contains ## [Unreleased] with Pfad A hygiene items."""
    content = _read_text("CHANGELOG.md")
    assert "## [Unreleased]" in content
    assert "CI-Lifecycle-Workflows" in content
    assert "Multi-Host-, Cache- & Lock-Schutz" in content
    assert "PEP 621" in content


def test_marketing_log_section_10():
    """Contract test: Ensure MARKETING-LOG.txt documents section 10 Pfad A audit."""
    content = _read_text("MARKETING-LOG.txt")
    assert "10. MAINTENANCE AUDIT & HYGIENE VERIFICATION (PFAD A)" in content
    assert "Date: 2026-09-23" in content
    assert "Frozen per T-20260920-167562623" in content


def test_third_party_licenses_audit_recency():
    """Contract test: Ensure THIRD_PARTY_LICENSES.md reflects 2026-09-23 audit."""
    content = _read_text("THIRD_PARTY_LICENSES.md")
    assert "Audited:** 2026-09-23" in content
