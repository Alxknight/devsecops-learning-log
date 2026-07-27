# S3 Security Auditor

> **Project status:** Complete for the defined educational scope  
> **Development status:** Preserved as a finished learning milestone; no active feature development planned

A Python CLI tool that audits **simulated AWS S3 bucket configurations**, detects common cloud-security misconfigurations, generates structured findings, supports JSON and CSV reporting, sends optional Discord alerts, and can behave as a basic CI/CD security gate.

> This project uses a local JSON inventory. It does not connect to a real AWS account.

---

## Project Purpose

The project demonstrates how a small security script can evolve into a tested and reusable automation tool.

It translates simplified S3 security requirements into executable checks and produces evidence that can be consumed by engineers, pipelines, or GRC stakeholders.

```text
Simulated S3 inventory
        ↓
Input validation
        ↓
Security-control evaluation
        ↓
Severity assignment
        ↓
Structured findings
        ↓
JSON / CSV report
        ↓
Optional Discord alert
        ↓
Optional CI failure threshold
```

The value of the project is not that it replaces an AWS security product. Its value is showing the connection between **security controls, Python logic, tests, evidence generation, notifications, and pipeline decisions**.

---

## Final Scope

The completed version includes:

- A command-line interface built with `argparse`
- Local JSON inventory loading and validation
- Four simulated S3 security controls
- Environment-aware severity logic
- Structured findings with recommendations
- Simplified security-framework mappings
- JSON and CSV output
- Professional logging
- Custom error handling
- Optional Discord webhook alerts
- Environment-variable secret handling
- Severity-based notification filtering
- CI-style failure behavior with `--fail-on-severity`
- Automated tests with `pytest`
- Mocked tests for the external webhook integration
- GitHub Actions CI for repeatable validation

---

## Security Controls

| Control ID | Requirement | Main risk |
|---|---|---|
| `S3_PUBLIC_ACCESS_DISABLED` | A bucket should not be publicly accessible | Unauthorized public exposure of data |
| `S3_ENCRYPTION_ENABLED` | Encryption at rest should be enabled | Stored data may lack expected protection |
| `S3_VERSIONING_ENABLED` | Versioning should be enabled | Recovery from deletion or overwrite becomes harder |
| `S3_ACCESS_LOGGING_ENABLED` | Access logging should be enabled | Reduced visibility for monitoring and investigations |

---

## Severity Model

Severity depends on the failed control and the declared environment.

| Condition | Severity |
|---|---|
| Public bucket in `production` | `critical` |
| Public bucket outside production | `high` |
| Missing encryption in `production` | `high` |
| Missing encryption outside production | `medium` |
| Missing versioning or logging in `production` | `medium` |
| Missing versioning or logging outside production | `low` |

This model is intentionally simplified. It demonstrates prioritization logic but is not a formal risk assessment methodology.

---

## Project Structure

```text
auto-audit-script/
├── audit.py
├── infrastructure.example.json
├── findings.example.json
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── tests/
│   └── test_audit.py
└── README.md
```

| File | Purpose |
|---|---|
| `audit.py` | CLI entry point, validation, audit logic, reporting, notification, and exit behavior |
| `infrastructure.example.json` | Example simulated S3 inventory |
| `findings.example.json` | Example machine-readable findings |
| `requirements.txt` | Runtime dependencies |
| `requirements-dev.txt` | Development and test dependencies |
| `pytest.ini` | Test discovery and import configuration |
| `tests/test_audit.py` | Unit, integration-style, output, notification, and CLI behavior tests |

---

## Requirements

Recommended version:

```text
Python 3.10+
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install runtime dependencies:

```bash
pip install -r requirements.txt
```

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

---

## Input Format

The input must be a JSON list of bucket objects.

```json
[
  {
    "bucket_name": "prod-customer-data",
    "environment": "production",
    "is_public": true,
    "encryption_enabled": false,
    "versioning_enabled": false,
    "logging_enabled": false
  },
  {
    "bucket_name": "prod-security-logs",
    "environment": "production",
    "is_public": false,
    "encryption_enabled": true,
    "versioning_enabled": true,
    "logging_enabled": true
  }
]
```

---

## Basic Usage

Run the audit and create a JSON report:

```bash
python audit.py \
  --input infrastructure.example.json \
  --output findings.example.json
```

Create a CSV report:

```bash
python audit.py \
  --input infrastructure.example.json \
  --output findings.csv \
  --output-format csv
```

---

## CLI Arguments

| Argument | Required | Description |
|---|---:|---|
| `--input` | Yes | Path to the simulated S3 inventory |
| `--output` | No | Destination for findings; defaults to `findings.json` |
| `--output-format` | No | `json` or `csv`; defaults to `json` |
| `--webhook-url` | No | Discord webhook URL; environment variable use is preferred |
| `--notify-severity` | No | Minimum severity that triggers a notification |
| `--fail-on-severity` | No | Minimum severity that causes a policy-failure exit code |

---

## Structured Findings

Example finding:

```json
{
  "resource_type": "aws_s3_bucket",
  "resource_name": "prod-customer-data",
  "environment": "production",
  "control_id": "S3_PUBLIC_ACCESS_DISABLED",
  "status": "failed",
  "severity": "critical",
  "message": "S3 bucket 'prod-customer-data' is publicly accessible.",
  "recommendation": "Disable public access and review the bucket policy.",
  "framework_mapping": {
    "nist_csf": "PR.DS - Data Security",
    "iso_27001": "A.8 - Technology Controls",
    "cis_aws": "S3 security best practices"
  }
}
```

JSON supports automation and machine processing. CSV supports spreadsheet review, evidence handling, and communication with non-engineering stakeholders.

---

## CI/CD Security Gate

The `--fail-on-severity` option separates an execution error from a policy failure.

```bash
python audit.py \
  --input infrastructure.example.json \
  --output findings.example.json \
  --fail-on-severity high
```

| Exit code | Meaning |
|---:|---|
| `0` | Audit succeeded and no finding met the configured failure threshold |
| `1` | Technical execution error, such as invalid input or an output failure |
| `2` | Audit completed, but findings met or exceeded the configured threshold |

This behavior allows a pipeline to distinguish between a broken tool and a valid audit that found unacceptable risk.

---

## Discord Notifications

A Discord webhook can receive a summary when findings meet the notification threshold.

Set the secret in the environment rather than committing it:

```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/example"
```

Run the audit:

```bash
python audit.py \
  --input infrastructure.example.json \
  --output findings.example.json \
  --notify-severity high
```

Notification thresholds:

| Value | Findings that can trigger an alert |
|---|---|
| `low` | Low, medium, high, and critical |
| `medium` | Medium, high, and critical |
| `high` | High and critical |
| `critical` | Critical only |

A webhook URL is a secret because anyone who possesses it may be able to send messages through the integration.

---

## Testing

Run the test suite:

```bash
pytest -v
```

The final suite contains more than 40 tests covering areas such as:

- Secure and insecure bucket scenarios
- Environment-aware severity assignment
- Invalid resource objects
- Missing or malformed input
- JSON and CSV output
- Notification thresholds
- Mocked Discord requests
- Webhook failures
- Failure-threshold behavior
- CLI exit codes

The project uses mocks for Discord so automated tests do not send real network notifications.

---

## Continuous Integration

GitHub Actions runs the automated test suite when relevant changes are pushed or proposed through a pull request.

```text
Push / Pull Request
        ↓
Install Python
        ↓
Install dependencies
        ↓
Run pytest
        ↓
Pass or fail the workflow
```

The CI workflow makes the validation repeatable and protects the repository from merging known test failures.

---

## Error Handling

| Scenario | Final behavior |
|---|---|
| Missing input file | Log and return a technical failure |
| Input path is not a file | Raise a controlled audit error |
| Invalid JSON | Log a validation error |
| Top-level JSON is not a list | Reject the inventory |
| Invalid bucket object | Warn, skip the item, and continue where possible |
| Invalid or missing bucket fields | Surface a warning without terminating the full audit |
| Output cannot be written | Return a controlled technical failure |
| Unsupported output format | Reject the requested format |
| Missing Discord webhook | Skip notification and continue |
| Discord request failure | Surface a controlled integration error |
| Finding reaches policy threshold | Complete the audit and return exit code `2` |

---

## Design Decisions

### Simulated Inventory

The local JSON inventory isolates the control logic from AWS credentials, API costs, account configuration, and network access. This made it possible to focus on Python design, testing, severity logic, reporting, and CI behavior.

### Structured Findings

Each finding carries consistent fields so the same result can support logging, JSON, CSV, notifications, and future integrations.

### Separate Notification and Failure Thresholds

A team may want to send alerts at one severity while blocking a pipeline at another. Keeping these decisions separate makes the CLI more flexible.

### Mocked External Integration

Discord behavior is tested without making real external requests. This improves reliability and prevents accidental messages during CI runs.

---

## Limitations and Out-of-Scope Items

This is an educational project, not a production AWS scanner.

The final scope does not include:

- Live AWS inventory through `boto3`
- IAM, bucket-policy, or ACL evaluation
- Cross-account discovery
- Additional AWS services
- Formal compliance certification
- A production notification platform
- SARIF publishing or packaging as an installable CLI

These are possible directions for a separate future project, not unfinished requirements of this one.

---

## Lessons Demonstrated

- Security requirements can be represented as explicit and testable logic.
- A finding should include context, severity, and a recommended action.
- Machine-readable and human-readable reports serve different audiences.
- A scanner's exit code can become a policy decision in CI/CD.
- External integrations should use environment-based secrets and mocked tests.
- Passing tests do not prove that the security model is complete; limitations must remain visible.

---

## Interview Summary

> I built a Python CLI that audits a simulated inventory of S3 buckets for public access, encryption, versioning, and logging. The tool generates structured JSON or CSV findings, assigns severity based on environment, sends optional Discord alerts, and can return a separate exit code when findings violate a configured threshold. I added more than 40 pytest tests, mocked the external webhook integration, and used GitHub Actions for repeatable validation. The project intentionally uses simulated data, so it demonstrates security-control automation and CI behavior without claiming to be a live AWS scanner.

---

## Final Project Statement

The S3 Security Auditor is complete for its defined learning scope. Its final version is preserved as evidence of Python security automation, control translation, testing, reporting, notification handling, and CI/CD gate design.

---

## Disclaimer

This project is for educational and portfolio purposes only. It is not a replacement for AWS-native security services, commercial cloud-security platforms, or a formal compliance assessment.
