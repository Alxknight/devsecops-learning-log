import argparse
import json
import logging
import os
from pathlib import Path
from typing import Any

import requests


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


class AuditError(Exception):
    """Base exception for audit-related errors."""


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Audit simulated AWS S3 bucket configurations for security risks."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the JSON file containing the simulated S3 bucket inventory.",
    )

    parser.add_argument(
        "--output",
        required=False,
        default="findings.json",
        help="Path where audit findings will be saved. Default: findings.json",
    )

    parser.add_argument(
        "--webhook-url",
        required=False,
        default=os.getenv("DISCORD_WEBHOOK_URL"),
        help="Discord webhook URL. Can also be set using DISCORD_WEBHOOK_URL.",
    )

    parser.add_argument(
        "--notify-severity",
        required=False,
        default="high",
        choices=["low", "medium", "high", "critical"],
        help="Minimum severity required to send a Discord alert. Default: high.",
    )

    parser.add_argument(
        "--fail-on-severity",
        required=False,
        choices=["low", "medium", "high", "critical"],
        help="Exit with code 2 if findings meet or exceed this severity.",
    )

    return parser.parse_args()


def load_infrastructure(file_path: str) -> list[dict[str, Any]]:
    """
    Load and validate the infrastructure inventory from a JSON file.

    Args:
        file_path: Path to the JSON inventory file.

    Returns:
        A list of S3 bucket dictionaries.

    Raises:
        FileNotFoundError: If the input file does not exist.
        AuditError: If the file cannot be read.
        ValueError: If the file is not valid JSON.
        TypeError: If the JSON structure is not a list.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    if not path.is_file():
        raise AuditError(f"Input path is not a file: {file_path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(f"Input file is not valid JSON: {file_path}") from error

    except OSError as error:
        raise AuditError(f"Could not read input file: {file_path}") from error

    if not isinstance(data, list):
        raise TypeError("Input JSON must contain a list of S3 buckets.")

    return data


def determine_severity(environment: str, control_id: str) -> str:
    """
    Determine finding severity based on environment and failed control.

    Args:
        environment: Environment where the bucket exists.
        control_id: Identifier of the failed control.

    Returns:
        Severity as a string.
    """
    environment = environment.lower()

    if control_id == "S3_PUBLIC_ACCESS_DISABLED":
        if environment == "production":
            return "critical"
        return "high"

    if control_id == "S3_ENCRYPTION_ENABLED":
        if environment == "production":
            return "high"
        return "medium"

    if control_id in {"S3_VERSIONING_ENABLED", "S3_ACCESS_LOGGING_ENABLED"}:
        if environment == "production":
            return "medium"
        return "low"

    return "medium"


def create_finding(
    bucket_name: str,
    environment: str,
    control_id: str,
    severity: str,
    message: str,
    recommendation: str,
) -> dict[str, Any]:
    """
    Create a structured audit finding.

    Args:
        bucket_name: Name of the affected S3 bucket.
        environment: Environment where the bucket exists.
        control_id: Security control that failed.
        severity: Finding severity.
        message: Human-readable description of the issue.
        recommendation: Suggested remediation.

    Returns:
        A structured finding dictionary.
    """
    return {
        "resource_type": "aws_s3_bucket",
        "resource_name": bucket_name,
        "environment": environment,
        "control_id": control_id,
        "status": "failed",
        "severity": severity,
        "message": message,
        "recommendation": recommendation,
        "framework_mapping": {
            "nist_csf": "PR.DS - Data Security",
            "iso_27001": "A.8 - Technology Controls",
            "cis_aws": "S3 security best practices",
        },
    }


def severity_meets_threshold(severity: str, threshold: str) -> bool:
    """
    Check whether a severity level meets or exceeds the notification threshold.

    Args:
        severity: Finding severity.
        threshold: Minimum severity required for notification.

    Returns:
        True if severity meets or exceeds the threshold.
    """
    severity_order = {
        "low": 1,
        "medium": 2,
        "high": 3,
        "critical": 4,
    }

    return severity_order.get(severity, 0) >= severity_order.get(threshold, 3)

def has_findings_at_or_above_threshold(
    findings: list[dict[str, Any]],
    threshold: str,
) -> bool:
    """
    Check whether any finding meets or exceeds the configured threshold.

    Args:
        findings: List of structured audit findings.
        threshold: Minimum severity that should trigger a failure.

    Returns:
        True if at least one finding meets or exceeds the threshold.
    """
    return any(
        severity_meets_threshold(
            severity=str(finding.get("severity", "")),
            threshold=threshold,
        )
        for finding in findings
    )

def audit_s3_security_controls(buckets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Audit simulated AWS S3 bucket security controls.

    Current controls:
    - S3 buckets should not be public.
    - S3 buckets should have encryption enabled.
    - S3 buckets should have versioning enabled.
    - S3 buckets should have access logging enabled.

    Args:
        buckets: List of simulated S3 bucket configurations.

    Returns:
        List of structured audit findings.
    """
    findings: list[dict[str, Any]] = []

    logger.info("Starting S3 security audit")

    for index, bucket in enumerate(buckets, start=1):
        if not isinstance(bucket, dict):
            logger.warning(
                "Skipping item %s because it is not a valid bucket object.",
                index,
            )
            continue

        bucket_name = bucket.get("bucket_name")
        environment = bucket.get("environment", "unknown")

        if not isinstance(bucket_name, str) or not bucket_name.strip():
            logger.warning(
                "Skipping bucket at position %s because it has an invalid or missing bucket_name.",
                index,
            )
            continue

        if not isinstance(environment, str) or not environment.strip():
            environment = "unknown"

        is_public = bucket.get("is_public")
        encryption_enabled = bucket.get("encryption_enabled")
        versioning_enabled = bucket.get("versioning_enabled")
        logging_enabled = bucket.get("logging_enabled")

        if is_public is True:
            control_id = "S3_PUBLIC_ACCESS_DISABLED"
            severity = determine_severity(environment, control_id)

            findings.append(
                create_finding(
                    bucket_name=bucket_name,
                    environment=environment,
                    control_id=control_id,
                    severity=severity,
                    message=f"S3 bucket '{bucket_name}' is publicly accessible.",
                    recommendation="Disable public access and review the bucket policy.",
                )
            )

            logger.critical(
                "Finding created: bucket '%s' is public in '%s'.",
                bucket_name,
                environment,
            )

        elif is_public is False:
            logger.info(
                "Passed: bucket '%s' is not public.",
                bucket_name,
            )

        else:
            logger.warning(
                "Bucket '%s' has an invalid or missing value for 'is_public'.",
                bucket_name,
            )

        if encryption_enabled is False:
            control_id = "S3_ENCRYPTION_ENABLED"
            severity = determine_severity(environment, control_id)

            findings.append(
                create_finding(
                    bucket_name=bucket_name,
                    environment=environment,
                    control_id=control_id,
                    severity=severity,
                    message=f"S3 bucket '{bucket_name}' does not have encryption enabled.",
                    recommendation="Enable default server-side encryption for the bucket.",
                )
            )

            logger.warning(
                "Finding created: bucket '%s' does not have encryption enabled.",
                bucket_name,
            )

        elif encryption_enabled is True:
            logger.info(
                "Passed: bucket '%s' has encryption enabled.",
                bucket_name,
            )

        else:
            logger.warning(
                "Bucket '%s' has an invalid or missing value for 'encryption_enabled'.",
                bucket_name,
            )

        if versioning_enabled is False:
            control_id = "S3_VERSIONING_ENABLED"
            severity = determine_severity(environment, control_id)

            findings.append(
                create_finding(
                    bucket_name=bucket_name,
                    environment=environment,
                    control_id=control_id,
                    severity=severity,
                    message=f"S3 bucket '{bucket_name}' does not have versioning enabled.",
                    recommendation="Enable versioning to protect against accidental deletion or overwrite.",
                )
            )

            logger.warning(
                "Finding created: bucket '%s' does not have versioning enabled.",
                bucket_name,
            )

        elif versioning_enabled is True:
            logger.info(
                "Passed: bucket '%s' has versioning enabled.",
                bucket_name,
            )

        else:
            logger.warning(
                "Bucket '%s' has an invalid or missing value for 'versioning_enabled'.",
                bucket_name,
            )

        if logging_enabled is False:
            control_id = "S3_ACCESS_LOGGING_ENABLED"
            severity = determine_severity(environment, control_id)

            findings.append(
                create_finding(
                    bucket_name=bucket_name,
                    environment=environment,
                    control_id=control_id,
                    severity=severity,
                    message=f"S3 bucket '{bucket_name}' does not have access logging enabled.",
                    recommendation="Enable S3 server access logging or centralized CloudTrail monitoring.",
                )
            )

            logger.warning(
                "Finding created: bucket '%s' does not have access logging enabled.",
                bucket_name,
            )

        elif logging_enabled is True:
            logger.info(
                "Passed: bucket '%s' has access logging enabled.",
                bucket_name,
            )

        else:
            logger.warning(
                "Bucket '%s' has an invalid or missing value for 'logging_enabled'.",
                bucket_name,
            )

    return findings


def save_findings(findings: list[dict[str, Any]], output_path: str) -> None:
    """
    Save audit findings to a JSON file.

    Args:
        findings: List of structured audit findings.
        output_path: Path where the findings file will be written.

    Raises:
        AuditError: If the findings file cannot be written.
    """
    path = Path(output_path)

    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(findings, file, indent=2, ensure_ascii=False)

    except OSError as error:
        raise AuditError(f"Could not write findings file: {output_path}") from error


def print_summary(
    total_buckets: int,
    findings: list[dict[str, Any]],
    output_path: str,
) -> None:
    """
    Print a summary of the audit results.

    Args:
        total_buckets: Total number of buckets scanned.
        findings: List of structured audit findings.
        output_path: Path where findings were saved.
    """
    severity_count = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for finding in findings:
        severity = finding.get("severity")

        if severity in severity_count:
            severity_count[severity] += 1

    logger.info("========== AUDIT SUMMARY ==========")
    logger.info("Total buckets scanned: %s", total_buckets)
    logger.info("Total findings: %s", len(findings))
    logger.info("Critical findings: %s", severity_count["critical"])
    logger.info("High findings: %s", severity_count["high"])
    logger.info("Medium findings: %s", severity_count["medium"])
    logger.info("Low findings: %s", severity_count["low"])
    logger.info("Findings written to: %s", output_path)


def send_discord_alert(
    webhook_url: str,
    findings: list[dict[str, Any]],
    notify_severity: str,
) -> None:
    """
    Send a Discord webhook alert for audit findings that meet the severity threshold.

    Args:
        webhook_url: Discord webhook URL.
        findings: List of structured audit findings.
        notify_severity: Minimum severity required to trigger an alert.

    Raises:
        AuditError: If the Discord webhook request fails.
    """
    if not webhook_url.strip():
        logger.info("Discord webhook URL is empty. Skipping alert notification.")
        return

    alert_findings = [
        finding
        for finding in findings
        if severity_meets_threshold(
            severity=str(finding.get("severity", "")),
            threshold=notify_severity,
        )
    ]

    if not alert_findings:
        logger.info(
            "No findings met the notification threshold: %s",
            notify_severity,
        )
        return

    severity_count = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for finding in alert_findings:
        severity = finding.get("severity")

        if severity in severity_count:
            severity_count[severity] += 1

    top_findings = alert_findings[:5]

    finding_lines = []

    for finding in top_findings:
        finding_lines.append(
            f"- [{str(finding.get('severity', 'unknown')).upper()}] "
            f"{finding.get('resource_name', 'unknown-resource')} | "
            f"{finding.get('control_id', 'unknown-control')}"
        )

    if len(alert_findings) > 5:
        finding_lines.append(
            f"- ...and {len(alert_findings) - 5} more finding(s)."
        )

    message = {
        "username": "S3 Security Auditor",
        "embeds": [
            {
                "title": "S3 Security Audit Alert",
                "description": "Security findings were detected during the S3 audit.",
                "color": 15158332,
                "fields": [
                    {
                        "name": "Notification Threshold",
                        "value": notify_severity.upper(),
                        "inline": True,
                    },
                    {
                        "name": "Findings Triggering Alert",
                        "value": str(len(alert_findings)),
                        "inline": True,
                    },
                    {
                        "name": "Severity Summary",
                        "value": (
                            f"Critical: {severity_count['critical']}\n"
                            f"High: {severity_count['high']}\n"
                            f"Medium: {severity_count['medium']}\n"
                            f"Low: {severity_count['low']}"
                        ),
                        "inline": False,
                    },
                    {
                        "name": "Top Findings",
                        "value": "\n".join(finding_lines)[:1000],
                        "inline": False,
                    },
                ],
            }
        ],
    }

    try:
        response = requests.post(
            webhook_url,
            json=message,
            timeout=10,
        )
        response.raise_for_status()

    except requests.RequestException as error:
        raise AuditError("Failed to send Discord webhook alert.") from error

    logger.info(
        "Discord alert sent successfully. Findings sent: %s",
        len(alert_findings),
    )


def main() -> int:
    """
    Main entry point for the S3 security audit CLI.

    Returns:
        Exit code:
        0 means successful execution.
        1 means execution failed.
    """
    args = parse_args()

    try:
        inventory = load_infrastructure(args.input)
        findings = audit_s3_security_controls(inventory)
        save_findings(findings, args.output)

        print_summary(
            total_buckets=len(inventory),
            findings=findings,
            output_path=args.output,
        )

        if args.webhook_url:
            send_discord_alert(
                webhook_url=args.webhook_url,
                findings=findings,
                notify_severity=args.notify_severity,
            )
        else:
            logger.info("Discord webhook not configured. Skipping alert notification.")

        if args.fail_on_severity and has_findings_at_or_above_threshold(
            findings=findings,
            threshold=args.fail_on_severity,
        ):
            logger.error(
                "Audit failed because findings met or exceeded severity threshold: %s",
                args.fail_on_severity,
            )
            return 2

        return 0

    except FileNotFoundError as error:
        logger.error("File error: %s", error)

    except ValueError as error:
        logger.error("JSON validation error: %s", error)

    except TypeError as error:
        logger.error("Data structure error: %s", error)

    except AuditError as error:
        logger.error("Audit error: %s", error)

    except Exception as error:
        logger.exception("Unexpected error during audit: %s", error)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())