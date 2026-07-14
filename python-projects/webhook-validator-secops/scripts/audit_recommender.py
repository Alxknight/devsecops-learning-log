#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
from typing import Any


SEVERITY_ORDER = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
    "INFO": 0,
    "UNKNOWN": 0,
}


def load_json(path: Path) -> Any:
    if not path.exists():
        return None

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return None


def normalize_severity(value: str | None) -> str:
    if not value:
        return "UNKNOWN"
    return value.upper()


def parse_bandit(report: Any) -> list[dict[str, str]]:
    findings = []

    if not isinstance(report, dict):
        return findings

    for item in report.get("results", []):
        severity = normalize_severity(item.get("issue_severity"))
        confidence = normalize_severity(item.get("issue_confidence"))

        findings.append(
            {
                "tool": "Bandit",
                "severity": severity,
                "confidence": confidence,
                "id": item.get("test_id", "N/A"),
                "title": item.get("issue_text", "N/A"),
                "file": item.get("filename", "N/A"),
                "line": str(item.get("line_number", "N/A")),
                "recommendation": (
                    "Review the flagged Python code. Avoid unsafe patterns, "
                    "hardcoded secrets, insecure subprocess usage, weak crypto, "
                    "or unsafe input handling."
                ),
            }
        )

    return findings


def parse_pip_audit(report: Any) -> list[dict[str, str]]:
    findings = []

    if not isinstance(report, dict):
        return findings

    # Common pip-audit JSON structure:
    # {"dependencies": [{"name": "...", "version": "...", "vulns": [...]}]}
    dependencies = report.get("dependencies", [])

    for dep in dependencies:
        package_name = dep.get("name", "N/A")
        installed_version = dep.get("version", "N/A")

        for vuln in dep.get("vulns", []):
            fix_versions = vuln.get("fix_versions", [])
            fix_text = ", ".join(fix_versions) if fix_versions else "No fixed version listed"

            if fix_versions:
                recommendation = (
                    f"Update {package_name} from {installed_version} "
                    f"to one of the fixed versions: {fix_text}."
                )
            else:
                recommendation = (
                    f"Review {package_name}. No fixed version was listed. "
                    "Check whether the package can be upgraded, replaced, or documented as accepted risk."
                )

            findings.append(
                {
                    "tool": "pip-audit",
                    "severity": normalize_severity(vuln.get("severity", "UNKNOWN")),
                    "id": vuln.get("id", "N/A"),
                    "title": vuln.get("description", "Python dependency vulnerability"),
                    "package": package_name,
                    "installed_version": installed_version,
                    "fixed_version": fix_text,
                    "recommendation": recommendation,
                }
            )

    return findings


def parse_trivy(report: Any) -> list[dict[str, str]]:
    findings = []

    if not isinstance(report, dict):
        return findings

    for result in report.get("Results", []):
        target = result.get("Target", "N/A")
        result_type = result.get("Type", "N/A")

        for vuln in result.get("Vulnerabilities", []) or []:
            severity = normalize_severity(vuln.get("Severity"))
            package_name = vuln.get("PkgName", "N/A")
            installed_version = vuln.get("InstalledVersion", "N/A")
            fixed_version = vuln.get("FixedVersion", "")

            if fixed_version:
                recommendation = (
                    f"Update {package_name} from {installed_version} "
                    f"to fixed version {fixed_version}. Then rebuild the Docker image."
                )
            elif result_type in {"debian", "ubuntu", "alpine"}:
                recommendation = (
                    f"No fixed version listed for {package_name}. "
                    "Try rebuilding with a newer base image and re-run Trivy."
                )
            else:
                recommendation = (
                    f"Review {package_name}. If no fixed version exists, document the risk "
                    "or evaluate replacing/upgrading the dependency."
                )

            findings.append(
                {
                    "tool": "Trivy",
                    "severity": severity,
                    "id": vuln.get("VulnerabilityID", "N/A"),
                    "title": vuln.get("Title", "Container or dependency vulnerability"),
                    "target": target,
                    "type": result_type,
                    "package": package_name,
                    "installed_version": installed_version,
                    "fixed_version": fixed_version or "No fixed version listed",
                    "recommendation": recommendation,
                }
            )

    return findings


def severity_score(finding: dict[str, str]) -> int:
    return SEVERITY_ORDER.get(finding.get("severity", "UNKNOWN"), 0)


def group_by_severity(findings: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped = {severity: [] for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", "UNKNOWN"]}

    for finding in findings:
        severity = finding.get("severity", "UNKNOWN")
        grouped.setdefault(severity, []).append(finding)

    return grouped


def write_markdown_summary(findings: list[dict[str, str]], output_path: Path) -> None:
    grouped = group_by_severity(findings)
    total = len(findings)

    lines = [
        "# Security Audit Summary",
        "",
        "Generated from local security audit reports.",
        "",
        "## Executive Summary",
        "",
        f"- Total findings: **{total}**",
        f"- Critical: **{len(grouped.get('CRITICAL', []))}**",
        f"- High: **{len(grouped.get('HIGH', []))}**",
        f"- Medium: **{len(grouped.get('MEDIUM', []))}**",
        f"- Low: **{len(grouped.get('LOW', []))}**",
        "",
    ]

    if total == 0:
        lines.extend(
            [
                "## Result",
                "",
                "No findings were parsed from the available reports.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "## Priority Recommendations",
                "",
            ]
        )

        critical_and_high = [
            finding
            for finding in findings
            if finding.get("severity") in {"CRITICAL", "HIGH"}
        ]

        if critical_and_high:
            for finding in sorted(critical_and_high, key=severity_score, reverse=True):
                lines.extend(
                    [
                        f"### {finding.get('severity')} - {finding.get('tool')} - {finding.get('id')}",
                        "",
                        f"**Title:** {finding.get('title', 'N/A')}",
                        "",
                        f"**Package/File:** {finding.get('package', finding.get('file', 'N/A'))}",
                        "",
                        f"**Installed version:** {finding.get('installed_version', 'N/A')}",
                        "",
                        f"**Fixed version:** {finding.get('fixed_version', 'N/A')}",
                        "",
                        f"**Recommendation:** {finding.get('recommendation', 'Review manually.')}",
                        "",
                    ]
                )
        else:
            lines.extend(
                [
                    "No CRITICAL or HIGH findings were detected in the parsed reports.",
                    "",
                ]
            )

        lines.extend(
            [
                "## All Findings",
                "",
                "| Severity | Tool | ID | Package/File | Recommendation |",
                "|---|---|---|---|---|",
            ]
        )

        for finding in sorted(findings, key=severity_score, reverse=True):
            package_or_file = finding.get("package") or finding.get("file") or finding.get("target") or "N/A"
            recommendation = finding.get("recommendation", "Review manually.").replace("|", "\\|")

            lines.append(
                f"| {finding.get('severity', 'UNKNOWN')} "
                f"| {finding.get('tool', 'N/A')} "
                f"| {finding.get('id', 'N/A')} "
                f"| {package_or_file} "
                f"| {recommendation} |"
            )

        lines.append("")

    lines.extend(
        [
            "## Notes",
            "",
            "- This summary is generated automatically and should be reviewed manually.",
            "- Do not commit raw `audit-reports/` output unless intentionally publishing evidence.",
            "- For container findings, rebuild the image after updating the base image or dependencies.",
            "- For Python dependency findings, update `requirements.txt`, reinstall, rerun tests, and rerun the audit.",
            "",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate security recommendations from audit reports.")
    parser.add_argument(
        "--report-dir",
        default="audit-reports",
        help="Directory containing Bandit, pip-audit, and Trivy JSON reports.",
    )
    parser.add_argument(
        "--output",
        default="audit-reports/security-summary.md",
        help="Markdown summary output path.",
    )
    parser.add_argument(
        "--fail-on-critical",
        action="store_true",
        help="Exit with code 1 if critical findings are detected.",
    )

    args = parser.parse_args()

    report_dir = Path(args.report_dir)
    output_path = Path(args.output)

    bandit_report = load_json(report_dir / "bandit.json")
    pip_audit_report = load_json(report_dir / "pip-audit.json")
    trivy_report = load_json(report_dir / "trivy-image.json")

    findings = []
    findings.extend(parse_bandit(bandit_report))
    findings.extend(parse_pip_audit(pip_audit_report))
    findings.extend(parse_trivy(trivy_report))

    findings = sorted(findings, key=severity_score, reverse=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_markdown_summary(findings, output_path)

    critical_count = sum(1 for finding in findings if finding.get("severity") == "CRITICAL")

    print(f"Security summary written to: {output_path}")
    print(f"Total findings: {len(findings)}")
    print(f"Critical findings: {critical_count}")

    if args.fail_on_critical and critical_count > 0:
        print("Critical findings detected. Failing as requested.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
