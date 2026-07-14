# Security Audit Report

## Project

Webhook Validator DevSecOps Project

## Purpose

This document summarizes the security validation process for the Webhook Validator microservice.

The goal is to demonstrate a practical DevSecOps workflow where a simple Python API is tested, containerized, scanned, and documented using repeatable security practices.

---

## Security Model

The application receives webhook requests and validates their authenticity using HMAC SHA-256 signatures.

Basic flow:

```text
External sender
   ↓
Payload + X-Webhook-Signature
   ↓
FastAPI service
   ↓
HMAC SHA-256 verification
   ↓
Accept or reject request

---

## CVE Research Notes

### Context

During local container image scanning with Trivy, the Webhook Validator project reported two main groups of security findings:

1. Python dependency findings related to `starlette`.
2. Operating system package findings inherited from the container base image.

The purpose of this note is to document the triage process before testing an alternative base image such as `python:3.12-alpine`.

This project is intentionally simple at the application layer. The main DevSecOps value is demonstrating how security findings are identified, researched, classified, remediated when possible, and documented when no immediate fix exists.

---

## Finding Group 1: Starlette Vulnerabilities

### Summary

Trivy reported HIGH vulnerabilities in `starlette`, a Python dependency used by FastAPI.

Reported findings:

- CVE-2025-62727
- CVE-2026-48818
- CVE-2026-54283

These findings appeared in the Python package layer, not in the operating system layer.

---

### CVE-2025-62727 — Starlette DoS via Range Header Processing

This vulnerability is related to Starlette's file response handling. A crafted HTTP `Range` header can trigger inefficient processing when Starlette merges byte ranges, potentially causing CPU exhaustion.

#### Application Exposure

The current Webhook Validator service has limited direct exposure because:

- It does not serve files.
- It does not use `FileResponse`.
- It does not expose static file endpoints.
- The main webhook endpoint reads the raw request body.

#### Decision

Even though direct exposure is limited, a fixed version exists. Therefore, the correct DevSecOps decision is to remediate rather than accept the risk.

Status: Remediated through dependency update.

---

### CVE-2026-48818 — Starlette StaticFiles SSRF / NTLM Credential Exposure on Windows

This vulnerability is related to Starlette's `StaticFiles` behavior on Windows when resolving UNC paths. A crafted path could cause an outbound SMB connection and potentially expose NTLM credentials.

#### Application Exposure

The current service has limited direct exposure because:

- It runs inside a Linux-based Docker container.
- It does not use Windows as the runtime environment.
- It does not use `StaticFiles`.
- It does not serve user-controlled file paths.

#### Decision

Even though the vulnerability is unlikely to be exploitable in the current containerized Linux deployment, a fixed version exists. The dependency should still be remediated.

Status: Remediated through dependency update.

---

### CVE-2026-54283 — Starlette `request.form()` DoS

This vulnerability is related to how Starlette handled limits for `application/x-www-form-urlencoded` form parsing. If limits are ignored, an attacker could send a large number of fields or oversized fields and cause denial of service.

#### Application Exposure

The current service has limited direct exposure because:

- It does not call `request.form()`.
- It does not process form submissions.
- The webhook endpoint reads the raw request body using `request.body()`.

#### Decision

Even though the application does not currently use the vulnerable code path, a fixed version exists. The dependency should be remediated.

Status: Remediated through dependency update.

---

## Starlette Remediation Actions

The following remediation work was performed:

- FastAPI was updated.
- Starlette was pinned directly as a temporary security remediation.
- `pip check` was executed to validate dependency compatibility.
- Pytest was executed to validate application behavior.
- The Docker image was rebuilt without cache.
- Trivy was re-run against the rebuilt image.

### Validation

Validation commands used:

```bash
python -m pip check
python -m pytest -v
docker build --pull --no-cache -t webhook-validator:starlette-remediation .