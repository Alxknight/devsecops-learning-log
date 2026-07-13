import json
from pathlib import Path

import pytest

from audit import (
    AuditError,
    audit_s3_security_controls,
    determine_severity,
    load_infrastructure,
    send_discord_alert,
    severity_meets_threshold,
)


def test_public_production_bucket_generates_critical_finding():
    buckets = [
        {
            "bucket_name": "prod-customer-data",
            "environment": "production",
            "is_public": True,
            "encryption_enabled": True,
            "versioning_enabled": True,
            "logging_enabled": True,
        }
    ]

    findings = audit_s3_security_controls(buckets)

    assert len(findings) == 1
    assert findings[0]["resource_name"] == "prod-customer-data"
    assert findings[0]["control_id"] == "S3_PUBLIC_ACCESS_DISABLED"
    assert findings[0]["severity"] == "critical"
    assert findings[0]["status"] == "failed"


def test_public_staging_bucket_generates_high_finding():
    buckets = [
        {
            "bucket_name": "staging-marketing-assets",
            "environment": "staging",
            "is_public": True,
            "encryption_enabled": True,
            "versioning_enabled": True,
            "logging_enabled": True,
        }
    ]

    findings = audit_s3_security_controls(buckets)

    assert len(findings) == 1
    assert findings[0]["resource_name"] == "staging-marketing-assets"
    assert findings[0]["control_id"] == "S3_PUBLIC_ACCESS_DISABLED"
    assert findings[0]["severity"] == "high"


def test_secure_bucket_generates_no_findings():
    buckets = [
        {
            "bucket_name": "prod-security-logs",
            "environment": "production",
            "is_public": False,
            "encryption_enabled": True,
            "versioning_enabled": True,
            "logging_enabled": True,
        }
    ]

    findings = audit_s3_security_controls(buckets)

    assert findings == []


def test_bucket_missing_encryption_generates_encryption_finding():
    buckets = [
        {
            "bucket_name": "prod-customer-data",
            "environment": "production",
            "is_public": False,
            "encryption_enabled": False,
            "versioning_enabled": True,
            "logging_enabled": True,
        }
    ]

    findings = audit_s3_security_controls(buckets)

    assert len(findings) == 1
    assert findings[0]["control_id"] == "S3_ENCRYPTION_ENABLED"
    assert findings[0]["severity"] == "high"
    assert "encryption" in findings[0]["message"].lower()


def test_bucket_missing_versioning_generates_versioning_finding():
    buckets = [
        {
            "bucket_name": "prod-customer-data",
            "environment": "production",
            "is_public": False,
            "encryption_enabled": True,
            "versioning_enabled": False,
            "logging_enabled": True,
        }
    ]

    findings = audit_s3_security_controls(buckets)

    assert len(findings) == 1
    assert findings[0]["control_id"] == "S3_VERSIONING_ENABLED"
    assert findings[0]["severity"] == "medium"


def test_bucket_missing_logging_generates_logging_finding():
    buckets = [
        {
            "bucket_name": "dev-temp-files",
            "environment": "development",
            "is_public": False,
            "encryption_enabled": True,
            "versioning_enabled": True,
            "logging_enabled": False,
        }
    ]

    findings = audit_s3_security_controls(buckets)

    assert len(findings) == 1
    assert findings[0]["control_id"] == "S3_ACCESS_LOGGING_ENABLED"
    assert findings[0]["severity"] == "low"


def test_invalid_bucket_object_is_skipped():
    buckets = [
        "not-a-valid-bucket",
        {
            "bucket_name": "valid-bucket",
            "environment": "production",
            "is_public": False,
            "encryption_enabled": True,
            "versioning_enabled": True,
            "logging_enabled": True,
        },
    ]

    findings = audit_s3_security_controls(buckets)

    assert findings == []


def test_bucket_without_valid_name_is_skipped():
    buckets = [
        {
            "bucket_name": "",
            "environment": "production",
            "is_public": True,
            "encryption_enabled": False,
            "versioning_enabled": False,
            "logging_enabled": False,
        }
    ]

    findings = audit_s3_security_controls(buckets)

    assert findings == []


@pytest.mark.parametrize(
    "environment, control_id, expected_severity",
    [
        ("production", "S3_PUBLIC_ACCESS_DISABLED", "critical"),
        ("staging", "S3_PUBLIC_ACCESS_DISABLED", "high"),
        ("production", "S3_ENCRYPTION_ENABLED", "high"),
        ("development", "S3_ENCRYPTION_ENABLED", "medium"),
        ("production", "S3_VERSIONING_ENABLED", "medium"),
        ("development", "S3_VERSIONING_ENABLED", "low"),
        ("production", "S3_ACCESS_LOGGING_ENABLED", "medium"),
        ("development", "S3_ACCESS_LOGGING_ENABLED", "low"),
    ],
)
def test_determine_severity(environment, control_id, expected_severity):
    severity = determine_severity(environment, control_id)

    assert severity == expected_severity


@pytest.mark.parametrize(
    "severity, threshold, expected_result",
    [
        ("critical", "critical", True),
        ("critical", "high", True),
        ("high", "critical", False),
        ("high", "high", True),
        ("medium", "high", False),
        ("medium", "medium", True),
        ("low", "medium", False),
        ("low", "low", True),
    ],
)
def test_severity_meets_threshold(severity, threshold, expected_result):
    result = severity_meets_threshold(severity, threshold)

    assert result is expected_result


def test_load_infrastructure_loads_valid_json_file(tmp_path):
    input_file = tmp_path / "infrastructure.json"

    data = [
        {
            "bucket_name": "test-bucket",
            "environment": "test",
            "is_public": False,
            "encryption_enabled": True,
            "versioning_enabled": True,
            "logging_enabled": True,
        }
    ]

    input_file.write_text(json.dumps(data), encoding="utf-8")

    loaded_data = load_infrastructure(str(input_file))

    assert loaded_data == data


def test_load_infrastructure_raises_error_when_file_does_not_exist():
    with pytest.raises(FileNotFoundError):
        load_infrastructure("missing-file.json")


def test_load_infrastructure_raises_error_for_invalid_json(tmp_path):
    input_file = tmp_path / "invalid.json"
    input_file.write_text("{invalid-json", encoding="utf-8")

    with pytest.raises(ValueError):
        load_infrastructure(str(input_file))


def test_load_infrastructure_raises_error_when_json_is_not_list(tmp_path):
    input_file = tmp_path / "invalid-structure.json"
    input_file.write_text(json.dumps({"bucket_name": "not-a-list"}), encoding="utf-8")

    with pytest.raises(TypeError):
        load_infrastructure(str(input_file))

def test_send_discord_alert_sends_request_for_matching_severity(monkeypatch):
    posted_payloads = []

    class FakeResponse:
        def raise_for_status(self):
            return None

    def fake_post(url, json, timeout):
        posted_payloads.append(
            {
                "url": url,
                "json": json,
                "timeout": timeout,
            }
        )
        return FakeResponse()

    monkeypatch.setattr("audit.requests.post", fake_post)

    findings = [
        {
            "resource_name": "prod-customer-data",
            "control_id": "S3_PUBLIC_ACCESS_DISABLED",
            "severity": "critical",
        }
    ]

    send_discord_alert(
        webhook_url="https://discord.com/api/webhooks/test",
        findings=findings,
        notify_severity="high",
    )

    assert len(posted_payloads) == 1
    assert posted_payloads[0]["url"] == "https://discord.com/api/webhooks/test"
    assert posted_payloads[0]["timeout"] == 10

    payload = posted_payloads[0]["json"]

    assert payload["username"] == "S3 Security Auditor"
    assert payload["embeds"][0]["title"] == "S3 Security Audit Alert"


def test_send_discord_alert_does_not_send_when_no_findings_match_threshold(monkeypatch):
    post_was_called = False

    def fake_post(url, json, timeout):
        nonlocal post_was_called
        post_was_called = True

    monkeypatch.setattr("audit.requests.post", fake_post)

    findings = [
        {
            "resource_name": "dev-temp-files",
            "control_id": "S3_ACCESS_LOGGING_ENABLED",
            "severity": "low",
        }
    ]

    send_discord_alert(
        webhook_url="https://discord.com/api/webhooks/test",
        findings=findings,
        notify_severity="critical",
    )

    assert post_was_called is False


def test_send_discord_alert_raises_audit_error_when_request_fails(monkeypatch):
    import requests

    def fake_post(url, json, timeout):
        raise requests.RequestException("network error")

    monkeypatch.setattr("audit.requests.post", fake_post)

    findings = [
        {
            "resource_name": "prod-customer-data",
            "control_id": "S3_PUBLIC_ACCESS_DISABLED",
            "severity": "critical",
        }
    ]

    with pytest.raises(AuditError):
        send_discord_alert(
            webhook_url="https://discord.com/api/webhooks/test",
            findings=findings,
            notify_severity="high",
        )


def test_send_discord_alert_skips_empty_webhook_url(monkeypatch):
    post_was_called = False

    def fake_post(url, json, timeout):
        nonlocal post_was_called
        post_was_called = True

    monkeypatch.setattr("audit.requests.post", fake_post)

    findings = [
        {
            "resource_name": "prod-customer-data",
            "control_id": "S3_PUBLIC_ACCESS_DISABLED",
            "severity": "critical",
        }
    ]

    send_discord_alert(
        webhook_url="   ",
        findings=findings,
        notify_severity="high",
    )

    assert post_was_called is False