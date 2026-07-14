# DevSecOps Learning Journey

> **12-Month Transformation:** Security Compliance Analyst → DevSecOps Engineer  
> **Timeline:** July 2026 - July 2027  
> **Target Role:** Junior DevOps Engineer / Cloud Security Analyst / Junior DevSecOps Engineer

## About This Repository

This repository documents my transition from **Security Compliance / GRC** into hands-on **DevSecOps, Cloud Security, and SRE-style engineering**.

The repository is being organized around **portfolio-ready projects**, structured CTF notes, and reproducible learning artifacts instead of loose practice files.

> **Repository cleanup note:** The old `week-01/` practice folder was removed to keep the repository cleaner and focused on stronger project work.

---

## Current Status

### Week 2 In Progress 🔄  
**Dates:** July 9-15, 2026

Week 2 is focused on improving the quality and professionalism of the first portfolio projects while completing foundational Linux/security practice through Bandit CTF.

### Week 2 Progress So Far

- ✅ Removed obsolete `week-01/` practice files
- ✅ Improved **S3 Security Auditor** with automated `pytest` coverage
- ✅ Added `pytest.ini` for local test discovery and imports
- ✅ Added GitHub Actions CI for the S3 Security Auditor
- ✅ Added mocked tests for Discord webhook alerting
- ✅ Added `--fail-on-severity` so the auditor can act as a CI/CD security gate
- ✅ Added JSON/CSV findings export with `--output-format`
- ✅ Improved **Webhook Validator SecOps** with Docker build and smoke test in GitHub Actions
- ✅ Updated GitHub Actions versions to avoid Node.js 20 deprecation warnings
- ✅ Added Trivy vulnerability scanning to the Webhook Validator workflow
- ✅ Added stronger secret handling for production-like environments
- ✅ Added `/ready` readiness endpoint in addition to `/health`
- ✅ Added request ID propagation with `X-Request-ID`
- ✅ Added Docker `HEALTHCHECK`
- ✅ Added `SECURITY_AUDIT.md` with OWASP-oriented security notes
- ✅ Performed Trivy-based CVE triage for Python dependencies and OS packages
- ✅ Updated FastAPI / Starlette dependency handling after vulnerability analysis
- ✅ Switched Webhook Validator base image from `python:3.12-slim` to `python:3.12-alpine`
- ✅ Verified Alpine-based image reduced Trivy HIGH/CRITICAL findings to zero in the tested scan
- ✅ Continued branch-based development for cleaner implementation history
- ✅ Completed available **OverTheWire Bandit CTF** levels through `bandit33`
- ✅ Documented advanced Bandit concepts for README and study database updates
- ✅ Continued KodeKloud Linux, Git, AWS, Azure, and MLOps/Jupyter labs

> **Bandit completion note:** Bandit level 34 does not currently exist, so `bandit33` represents the current end of the available Bandit wargame path.

---

## Current Repository Structure

```text
devsecops-learning-log/
├── .github/
│   └── workflows/
│       ├── s3-auditor-ci.yml
│       └── webhook-validator-ci.yml
├── ctf/
│   └── bandit/
│       └── bandit-final-notes.md
├── python-projects/
│   ├── auto-audit-script/
│   │   ├── audit.py
│   │   ├── infrastructure.example.json
│   │   ├── findings.example.json
│   │   ├── requirements.txt
│   │   ├── requirements-dev.txt
│   │   ├── pytest.ini
│   │   ├── README.md
│   │   └── tests/
│   │       └── test_audit.py
│   └── webhook-validator-secops/
│       ├── app/
│       │   ├── __init__.py
│       │   └── main.py
│       ├── tests/
│       │   └── test_main.py
│       ├── scripts/
│       │   ├── local-security-audit.sh
│       │   └── audit_recommender.py
│       ├── .dockerignore
│       ├── .env.example
│       ├── .gitignore
│       ├── Dockerfile
│       ├── pyproject.toml
│       ├── requirements.txt
│       ├── SECURITY_AUDIT.md
│       └── README.md
└── README.md
```

---

# Portfolio Projects

## 1. S3 Security Auditor

**Status:** ✅ Functional MVP + Discord Alerts + Pytest + CI + Security Gate + CSV Export  
**Folder:** `python-projects/auto-audit-script/`  
**Language:** Python 3  
**Focus:** Cloud Security / GRC Automation / DevSecOps

### What It Does

The S3 Security Auditor is a Python CLI tool that audits simulated AWS S3 bucket configurations from a local JSON file.

It checks for common S3 security misconfigurations:

- Public bucket access
- Missing encryption
- Missing versioning
- Missing access logging

The tool generates structured findings with:

- Resource name
- Failed security control
- Severity
- Recommendation
- Basic framework mapping
- JSON or CSV output report

### Main Features

- CLI interface with `argparse`
- JSON input validation
- Professional logging
- Custom exception handling
- Structured security findings
- Severity-based prioritization
- Optional Discord webhook alerting
- Environment variable-based secret handling
- Automated testing with `pytest`
- Mocked tests for Discord webhook behavior
- GitHub Actions CI for automated tests
- `--fail-on-severity` security gate behavior
- JSON and CSV output with `--output-format`

### Example Usage

```bash
cd python-projects/auto-audit-script

pip install -r requirements.txt
python audit.py --input infrastructure.example.json --output findings.example.json
```

Run with CSV output:

```bash
python audit.py \
  --input infrastructure.example.json \
  --output findings.csv \
  --output-format csv
```

Run as a security gate:

```bash
python audit.py \
  --input infrastructure.example.json \
  --output findings.example.json \
  --fail-on-severity high
```

Run with Discord alerts:

```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/your-webhook"
python audit.py \
  --input infrastructure.example.json \
  --output findings.example.json \
  --notify-severity high
```

### Testing

```bash
pip install -r requirements-dev.txt
pytest -v
```

Latest expected local result:

```text
40+ passing tests
```

### What This Project Demonstrates

- Python automation for security use cases
- Translating GRC controls into executable logic
- Cloud security fundamentals
- Risk prioritization
- Secure handling of secrets
- Webhook-based alerting
- Mocking external integrations
- Automated unit testing
- CI/CD security gate behavior
- JSON and CSV reporting
- Branch-based implementation workflow

### Completed Improvements

- ✅ Production-ready audit CLI
- ✅ Discord webhook alerting
- ✅ Pytest coverage
- ✅ GitHub Actions CI
- ✅ Mocked webhook tests
- ✅ `--fail-on-severity` security gate
- ✅ CSV findings export

### Next Improvements

- Real AWS inventory using `boto3`
- More S3 controls
- SARIF output
- Slack webhook support
- Package as installable CLI

---

## 2. Webhook Validator SecOps

**Status:** ✅ API + Tests + Docker + CI + Trivy + Security Audit + Alpine Base Image  
**Folder:** `python-projects/webhook-validator-secops/`  
**Language:** Python 3  
**Focus:** DevSecOps / SRE / Secure API Delivery

### What It Does

Webhook Validator SecOps is a FastAPI microservice that validates incoming webhooks using **HMAC SHA-256** signatures.

The application receives a payload and a signature, recalculates the expected HMAC signature using a shared secret, and safely compares both signatures before accepting or rejecting the webhook.

```text
External client sends payload + signature
   ↓
API receives the webhook
   ↓
API recalculates expected HMAC signature
   ↓
API compares signatures securely
   ↓
Webhook is accepted or rejected
```

### Current Implementation

Completed so far:

- ✅ FastAPI application
- ✅ `/health` liveness endpoint
- ✅ `/ready` readiness endpoint
- ✅ `/webhook` endpoint
- ✅ HMAC SHA-256 signature validation
- ✅ Secure comparison with `hmac.compare_digest()`
- ✅ Production-like environments require explicit `WEBHOOK_SECRET`
- ✅ Request tracing with `X-Request-ID`
- ✅ Safe logging for accepted/rejected webhook events without exposing secrets, signatures, or payloads
- ✅ Pytest test suite with 9 tests
- ✅ Dockerfile using `python:3.12-alpine`
- ✅ Non-root container user
- ✅ Docker `HEALTHCHECK`
- ✅ `.dockerignore`
- ✅ GitHub Actions CI for Python tests
- ✅ GitHub Actions Docker build
- ✅ Automated container smoke test against `/health`
- ✅ Trivy vulnerability scanning in the container security workflow
- ✅ `SECURITY_AUDIT.md` with OWASP/CVE triage notes
- ✅ CVE triage for Starlette findings and OS-level base image findings
- ✅ Alpine base image experiment reduced Trivy HIGH/CRITICAL findings to zero in the tested image
- ✅ Updated GitHub Actions versions:
  - `actions/checkout@v5`
  - `actions/setup-python@v6`

### Local Usage

```bash
cd python-projects/webhook-validator-secops

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

pytest
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://localhost:8000/health
```

Readiness check:

```bash
curl http://localhost:8000/ready
```

### Docker Usage

Build image:

```bash
docker build -t webhook-validator:local .
```

Run container:

```bash
docker run --rm \
  -p 8000:8000 \
  -e WEBHOOK_SECRET=dev-secret \
  webhook-validator:local
```

Smoke test:

```bash
curl --fail http://localhost:8000/health
curl --fail http://localhost:8000/ready
```

### Security Audit Usage

Run the local audit workflow from the project folder:

```bash
./scripts/local-security-audit.sh
```

Generated reports are stored locally in:

```text
audit-reports/
```

The reports are intentionally ignored by Git. The project keeps the repeatable audit workflow and the human-readable `SECURITY_AUDIT.md`, not noisy machine-generated output.

### CI/CD Pipeline

The workflow lives at:

```text
.github/workflows/webhook-validator-ci.yml
```

Current pipeline:

```text
Push / Pull Request
   ↓
Run Python tests
   ↓
Build Docker image
   ↓
Run Trivy scan
   ↓
Run container
   ↓
Smoke test /health endpoint
   ↓
Clean up container
```

### Security Practices Applied

- HMAC SHA-256 validation
- Secure signature comparison with `hmac.compare_digest()`
- Secret loaded from environment variable
- Production-like environments require explicit secret configuration
- `/ready` validates whether the service is configured to receive traffic
- `X-Request-ID` supports request tracing
- Safe logging avoids exposing secrets, signatures, and payloads
- Non-root container user
- Alpine-based runtime image to reduce OS package footprint
- Docker `HEALTHCHECK`
- Automated tests in CI
- Docker smoke test in CI
- Trivy-based vulnerability scanning
- CVE triage documented in `SECURITY_AUDIT.md`
- Workflow permissions limited with `contents: read`
- AWS Budget configured before cloud infrastructure work

### Next Improvements

The next sprint starts with cloud/Kubernetes preparation.

Planned work:

1. Prepare low-cost AWS EC2 environment
2. Install K3s or Minikube on EC2
3. Create Kubernetes manifests
4. Add Kubernetes `Secret` for `WEBHOOK_SECRET`
5. Add readiness/liveness probes using `/ready` and `/health`
6. Deploy the API to Kubernetes
7. Document architecture and evidence for portfolio use

---

## 3. CTF Practice — OverTheWire Bandit

**Status:** ✅ Completed available levels through `bandit33`  
**Folder:** `ctf/bandit/`  
**Focus:** Linux Security / DevSecOps Foundations / Git Security / Shell Escapes

### What It Is

OverTheWire Bandit is a Linux security wargame focused on practical command-line problem solving. It builds foundational skills for security engineering, DevSecOps, system administration, and troubleshooting.

I completed the available Bandit path through `bandit33`. Level 34 does not currently exist, so `bandit33` represents the current end of the wargame.

### DevSecOps Lessons

Bandit reinforced several real-world DevSecOps lessons:

- Secrets should never be committed to Git, even temporarily.
- Git history, branches, tags, and metadata must be included in repository audits.
- Cron jobs and automation scripts can accidentally expose sensitive data.
- `setuid` binaries are powerful and dangerous when misconfigured.
- Services need rate limiting and brute force protections.
- Restricted shells must be configured carefully because interactive programs may allow escapes.
- Reading scripts written by others is a critical security and operations skill.

---

## Learning Platforms

| Platform | Status | Focus Area | Progress |
|---|---|---|---|
| Bandit CTF | ✅ Completed available path | Linux security, Git security, shell escapes | Completed through `bandit33` |
| KodeKloud | ✅ Active | Linux, cloud, DevOps labs | 13+ labs |
| KillerCoda | ✅ Active | Interactive scenarios | 2 lessons |
| LabEx | ✅ Active | Hands-on Linux labs | 4 labs |
| Exercism | ✅ Active | Bash scripting | 1 exercise |
| AWS Free Tier | 🔄 Starting | Cloud hands-on | Budget configured |

---

## Roadmap

### Phase 1: Foundations  
**Months 1-3**  
**Status:** 🔄 In Progress — Week 2 of 12

- [x] Linux fundamentals
- [x] Bandit CTF levels 0-33
- [x] First Python security automation project
- [x] Discord webhook alerting
- [x] Pytest coverage for S3 Security Auditor
- [x] GitHub Actions CI for S3 Security Auditor
- [x] Fail-on-severity security gate
- [x] CSV export for audit findings
- [x] Webhook Validator API with FastAPI
- [x] Dockerized Webhook Validator
- [x] GitHub Actions CI for tests
- [x] Docker build and smoke test in CI
- [x] Trivy image scanning and CVE triage
- [x] Alpine base image hardening experiment
- [ ] Continue AWS CLI and IAM practice
- [ ] Start Kubernetes fundamentals with K3s or Minikube

> Bandit level 34 is not currently available, so the Bandit CTF milestone is complete for the available path.

### Phase 2: Automation & Infrastructure  
**Months 4-6**

- [ ] Terraform basics
- [ ] Infrastructure as Code
- [ ] GitHub Actions security gates
- [ ] Python automation with real AWS APIs
- [ ] Docker and Kubernetes deployment workflows

### Phase 3: Security Integration  
**Months 7-9**

- [ ] AWS security services
- [ ] Container security
- [ ] Secret management
- [ ] Vulnerability scanning in pipelines
- [ ] Policy-as-code fundamentals

### Phase 4: Advanced Portfolio  
**Months 10-12**

- [ ] Kubernetes hardening basics
- [ ] Monitoring and logging
- [ ] 3-5 portfolio projects
- [ ] Resume, LinkedIn, and interview preparation

---

## Week 2 Goals

**Dates:** July 9-15, 2026  
**Status:** 🔄 In Progress

- [x] Complete Bandit CTF available levels through `bandit33`
- [x] Add pytest tests to S3 Security Auditor
- [x] Add mocked tests for Discord webhook alerts
- [x] Add GitHub Actions CI for S3 Security Auditor
- [x] Add `--fail-on-severity` security gate
- [x] Add CSV export for audit findings
- [x] Update Webhook Validator CI with Docker build and smoke test
- [x] Add Trivy scan to Webhook Validator CI / security workflow
- [x] Add Webhook Validator `SECURITY_AUDIT.md`
- [x] Remediate Starlette dependency findings
- [x] Switch Webhook Validator runtime image to Alpine after CVE triage
- [ ] Continue KodeKloud networking fundamentals
- [ ] Continue AWS CLI hands-on practice
- [ ] Prepare for Kubernetes lab using EC2 + K3s or Minikube

---

## Progress Metrics

| Metric | Current Progress | Month 1 Target |
|---|---:|---:|
| Bandit CTF Challenges | Completed through `bandit33` | Complete available path |
| KodeKloud Labs | 13+ | 20 |
| Portfolio Projects | 2 | 2 |
| CTF Documentation Sets | 1 | 1 |
| Automated Tests | 49+ | 50+ |
| Dockerized Projects | 1 | 2 |
| CI/CD Pipelines | 2 | 2 |
| Security Alerting Integrations | 1 | 1 |
| Security Gate Features | 2 | 2 |
| GitHub Commits | 75+ | 100+ |

> Automated tests currently include 40+ tests for S3 Security Auditor and 9 tests for Webhook Validator.

---

## Skills Inventory

### Python

- ✅ CLI development with `argparse`
- ✅ JSON processing
- ✅ CSV report generation
- ✅ Logging and exception handling
- ✅ HTTP requests and webhook integration
- ✅ FastAPI microservice development
- ✅ HMAC SHA-256 validation
- ✅ Environment variable configuration
- ✅ Pytest unit testing
- ✅ Test parametrization
- ✅ Temporary file testing with `tmp_path`
- ✅ Mocking external integrations
- ✅ Dependency vulnerability remediation
- 📋 AWS automation with `boto3`

### DevOps / SRE

- ✅ Docker image build
- ✅ Non-root container execution
- ✅ Container smoke testing
- ✅ Docker healthcheck
- ✅ GitHub Actions CI
- ✅ CI job dependencies with `needs`
- ✅ Workflow path filters
- ✅ CI/CD-style failure threshold
- ✅ Git branch workflow
- ✅ Cleaning obsolete files safely
- ✅ Git over SSH with custom ports
- ✅ Git history, branch, and tag inspection
- ✅ Liveness and readiness endpoint design
- ✅ Request ID tracing
- ✅ Trivy vulnerability scanning
- ✅ Base image comparison and hardening
- 📋 Kubernetes deployment with K3s or Minikube

### Cloud Security / DevSecOps

- ✅ S3 security control logic
- ✅ Severity-based risk prioritization
- ✅ GRC-style findings and recommendations
- ✅ JSON and CSV evidence generation
- ✅ Secure webhook validation
- ✅ Secret handling with environment variables
- ✅ Production-like secret enforcement
- ✅ Basic CI/CD security practices
- ✅ Docker security basics
- ✅ Container CVE triage
- ✅ Alpine base image hardening
- ✅ Security audit documentation
- ✅ Secret exposure analysis in Git repositories
- ✅ Cron job and automation auditing
- ✅ Controlled brute force awareness in lab context
- ✅ Image vulnerability scanning
- 📋 AWS IAM and EC2 security basics

---

## Git Workflow Practices

I am using feature branches for meaningful changes.

Examples:

```bash
git switch -c feature/discord-webhook-alerts
git switch -c feature/add-pytest-coverage
git switch -c feature/s3-auditor-ci
git switch -c feature/test-discord-webhook-alerts
git switch -c feature/s3-auditor-fail-threshold
git switch -c feature/s3-auditor-csv-output
git switch -c chore/remove-obsolete-week-01
git switch -c docs/add-bandit-final-notes
git switch -c security/update-fastapi-starlette
git switch -c security/add-cve-research-notes
git switch -c security/test-alpine-base-image
```

This keeps `main` cleaner and makes every repository change easier to review.

---

## How I Explain These Projects in an Interview

### S3 Security Auditor

> I built a Python CLI tool that simulates cloud security control validation for AWS S3 buckets. It reads a JSON inventory, evaluates controls like public access, encryption, versioning, and logging, then generates structured findings with severity and remediation guidance. I added Discord alerting for high-priority issues, automated tests with pytest, mocked tests for the webhook integration, a CI workflow, a fail-on-severity option so it can act as a security gate, and CSV output for GRC-style reporting.

### Webhook Validator SecOps

> I built a FastAPI microservice that validates incoming webhooks using HMAC SHA-256. The value of the project is the end-to-end DevSecOps workflow: tests with pytest, Docker packaging, non-root container execution, GitHub Actions CI, Docker image build, Trivy vulnerability scanning, smoke testing, readiness/liveness endpoints, and CVE triage. Trivy identified dependency and base-image findings, so I updated Python dependencies, documented the CVE research, and switched the runtime image from Debian slim to Alpine after confirming the Alpine image produced no HIGH or CRITICAL findings in the tested scan.

### Bandit CTF Practice

> I completed the available OverTheWire Bandit levels through bandit33 and documented the technical lessons. The work strengthened my Linux security fundamentals through SSH, permissions, setuid binaries, cron jobs, shell scripting, Netcat, OpenSSL, brute force automation in a controlled lab, Git repository auditing, and shell escapes. I treated the CTF as structured DevSecOps practice by documenting concepts, commands, mistakes, and security lessons without committing real passwords.

### What These Projects Demonstrate Together

Together, these projects show that I can:

- Turn security requirements into code
- Build Python tools and APIs
- Validate behavior with automated tests
- Package applications in Docker
- Create CI/CD workflows
- Add basic security gates
- Manage secrets safely
- Generate both machine-readable and human-readable security findings
- Analyze container vulnerability scan output
- Distinguish fixable dependency findings from base image findings without available fixes
- Remediate dependencies safely with tests and `pip check`
- Reduce container attack surface by changing base images
- Audit repositories for secret exposure patterns
- Analyze Linux permissions and automation risks
- Work through branches like a real engineering workflow
- Explain both the technical and security value of what I build

---

## Current Learning Principle

The repository is evolving from a learning dump into a portfolio.

Current standard:

```text
Every meaningful project should have:
- Clear README
- Reproducible commands
- Tests
- Error handling
- Security considerations
- Git branch history
- CI/CD or automation where appropriate
- Machine-readable and human-readable outputs when useful
- Security audit notes when scanners are used
- Next-step roadmap
- Study notes that explain concepts, not just commands
```

---

## License

This repository is for personal learning and portfolio development.

Code projects are shared freely for educational purposes.

---

**Last Updated:** July 14, 2026  
**Current Week:** Week 2 in progress  
**Next Milestone:** Low-cost AWS EC2 + K3s/Minikube lab preparation  
**Momentum:** Strong — Bandit CTF available levels are complete, both portfolio projects now have CI, and Webhook Validator includes container scanning, CVE triage, dependency remediation, and Alpine base image hardening.
