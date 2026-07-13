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
- ✅ Validated **28 passing tests** for the S3 Security Auditor
- ✅ Improved **Webhook Validator SecOps** with Docker build and smoke test in GitHub Actions
- ✅ Updated GitHub Actions versions to avoid Node.js 20 deprecation warnings
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
│       ├── .dockerignore
│       ├── Dockerfile
│       ├── pyproject.toml
│       ├── requirements.txt
│       └── README.md
└── README.md
```

---

# Portfolio Projects

## 1. S3 Security Auditor

**Status:** ✅ Functional MVP + Discord Alerts + Pytest Coverage  
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
- JSON output report

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

### Example Usage

```bash
cd python-projects/auto-audit-script

pip install -r requirements.txt
python audit.py --input infrastructure.example.json --output findings.example.json
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

Latest local result:

```text
28 passed in 0.96s
```

### What This Project Demonstrates

- Python automation for security use cases
- Translating GRC controls into executable logic
- Cloud security fundamentals
- Risk prioritization
- Secure handling of secrets
- Webhook-based alerting
- Automated unit testing
- Branch-based implementation workflow

### Next Improvements

- Mock Discord webhook tests
- GitHub Actions CI for the S3 auditor
- CSV export
- More S3 controls
- Real AWS inventory using `boto3`

---

## 2. Webhook Validator SecOps

**Status:** ✅ API + Tests + Docker + CI + Docker Smoke Test  
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
- ✅ `/health` endpoint
- ✅ `/webhook` endpoint
- ✅ HMAC SHA-256 signature validation
- ✅ Secure comparison with `hmac.compare_digest()`
- ✅ Pytest test suite
- ✅ Dockerfile using `python:3.12-slim`
- ✅ Non-root container user
- ✅ `.dockerignore`
- ✅ GitHub Actions CI for Python tests
- ✅ GitHub Actions Docker build
- ✅ Automated container smoke test against `/health`
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
```

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
- Non-root container user
- Lightweight Docker image
- Automated tests in CI
- Docker smoke test in CI
- Workflow permissions limited with `contents: read`
- AWS Budget configured before cloud infrastructure work

### Next Improvements

The next sprint starts at **Day 5: Trivy**.

Planned work:

1. Add Trivy vulnerability scanning to GitHub Actions
2. Fail the build on critical vulnerabilities
3. Prepare low-cost AWS EC2 environment
4. Install K3s or Minikube on EC2
5. Create Kubernetes manifests
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

### Main Skills Practiced

- Linux file navigation and permissions
- SSH login and remote command execution
- SSH private key handling
- WSL/Linux permission troubleshooting
- Port scanning with `nmap`
- SSL/TLS service interaction with `openssl s_client`
- Netcat listeners and local daemon communication
- `setuid` binaries and privilege boundaries
- Cron job auditing in `/etc/cron.d/`
- Reading and writing shell scripts
- Brute force automation in a controlled lab
- Shell escapes through `more`, `vi`, and restricted shells
- Git repository auditing across history, branches, and tags
- Git workflow with `add`, `commit`, and `push`

### Advanced Concepts Covered

#### Linux and Security

- Compared files with `diff` to identify changed secrets.
- Used `setuid` binaries to understand privilege delegation.
- Audited cron jobs to identify automated scripts exposing secrets.
- Created a custom shell script executed by a scheduled process.
- Used `seq`, `for`, pipes, `nc`, and `grep -v` for controlled brute force automation.

#### SSH and Shell Escapes

- Copied private keys safely with `scp`.
- Fixed WSL permission issues by storing keys inside the Linux filesystem.
- Escaped from `more` into `vi`, then from `vi` into Bash.
- Escaped an uppercase-restricted shell using `$0`.

#### Git Security

- Cloned repositories over SSH using a custom port.
- Found secrets in Git history using `git log -p` and `git show`.
- Reviewed remote branches with `git branch -a`.
- Reviewed tags with `git tag` and `git show`.
- Forced a tracked file through `.gitignore` using `git add -f`.
- Completed a full Git workflow with `commit` and `push`.

### DevSecOps Lessons

Bandit reinforced several real-world DevSecOps lessons:

- Secrets should never be committed to Git, even temporarily.
- Git history, branches, tags, and metadata must be included in repository audits.
- Cron jobs and automation scripts can accidentally expose sensitive data.
- `setuid` binaries are powerful and dangerous when misconfigured.
- Services need rate limiting and brute force protections.
- Restricted shells must be configured carefully because interactive programs may allow escapes.
- Reading scripts written by others is a critical security and operations skill.

### Commands Reinforced

```bash
ls
cat
grep
cut
chmod
nano
whoami
id
pwd
diff
seq
for
echo
ssh
scp
nmap
openssl s_client
nc
cron
git clone
git log -p
git show
git branch -a
git tag
git add -f
git commit
git push
```

### Documentation Note

The detailed notes should be stored as:

```text
ctf/bandit/bandit-final-notes.md
```

No real Bandit passwords should be committed to this repository. The notes should document concepts, commands, troubleshooting steps, and lessons learned without exposing actual secrets.

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
- [x] Bandit CTF levels 0-25
- [x] Bandit CTF levels 26-33
- [x] First Python security automation project
- [x] Discord webhook alerting
- [x] Pytest coverage for S3 Security Auditor
- [x] Webhook Validator API with FastAPI
- [x] Dockerized Webhook Validator
- [x] GitHub Actions CI for tests
- [x] Docker build and smoke test in CI
- [ ] Add Trivy image scanning
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
- [ ] Add mocked tests for Discord webhook alerts
- [x] Update Webhook Validator CI with Docker build and smoke test
- [ ] Add Trivy scan to Webhook Validator CI
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
| Automated Tests | 32+ | 35+ |
| Dockerized Projects | 1 | 2 |
| CI/CD Pipelines | 1 | 2 |
| Security Alerting Integrations | 1 | 1 |
| GitHub Commits | 70+ | 100+ |

> Automated tests currently include 28 tests for S3 Security Auditor and 4 tests for Webhook Validator.

---

## Skills Inventory

### Python

- ✅ CLI development with `argparse`
- ✅ JSON processing
- ✅ Logging and exception handling
- ✅ HTTP requests and webhook integration
- ✅ FastAPI microservice development
- ✅ HMAC SHA-256 validation
- ✅ Environment variable configuration
- ✅ Pytest unit testing
- ✅ Test parametrization
- ✅ Temporary file testing with `tmp_path`
- 🔄 Mocking external integrations
- 📋 AWS automation with `boto3`

### DevOps / SRE

- ✅ Docker image build
- ✅ Non-root container execution
- ✅ Container smoke testing
- ✅ GitHub Actions CI
- ✅ CI job dependencies with `needs`
- ✅ Workflow path filters
- ✅ Git branch workflow
- ✅ Cleaning obsolete files safely
- ✅ Git over SSH with custom ports
- ✅ Git history, branch, and tag inspection
- 🔄 Trivy vulnerability scanning
- 📋 Kubernetes deployment with K3s or Minikube

### Cloud Security / DevSecOps

- ✅ S3 security control logic
- ✅ Severity-based risk prioritization
- ✅ GRC-style findings and recommendations
- ✅ Secure webhook validation
- ✅ Secret handling with environment variables
- ✅ Basic CI/CD security practices
- ✅ Docker security basics
- ✅ Secret exposure analysis in Git repositories
- ✅ Cron job and automation auditing
- ✅ Controlled brute force awareness in lab context
- 🔄 Image vulnerability scanning
- 📋 AWS IAM and EC2 security basics

### Linux & Security Fundamentals

- ✅ File permissions
- ✅ User and group management
- ✅ SSH hardening
- ✅ SSH private key handling
- ✅ Cron job auditing
- ✅ Bash automation
- ✅ Netcat and OpenSSL usage
- ✅ Port scanning with Nmap
- ✅ Controlled brute-force automation in CTF context
- ✅ `setuid` binary analysis
- ✅ Shell escapes using `more`, `vi`, and `$0`
- ✅ WSL/Linux permission troubleshooting

---

## Git Workflow Practices

I am using feature branches for meaningful changes.

Examples:

```bash
git switch -c feature/discord-webhook-alerts
git switch -c feature/add-pytest-coverage
git switch -c chore/remove-obsolete-week-01
git switch -c docs/add-bandit-final-notes
```

Repository cleanup flow:

```bash
git status
git switch -c chore/remove-obsolete-week-01
rm -rf week-01
git add -A week-01
git commit -m "Remove obsolete week 1 practice files"
git push -u origin chore/remove-obsolete-week-01
```

Bandit documentation update flow:

```bash
mkdir -p ctf/bandit
cp bandit-final-notes.md ctf/bandit/bandit-final-notes.md
git add README.md ctf/bandit/bandit-final-notes.md
git commit -m "Document completed Bandit CTF progress"
git push
```

This keeps `main` cleaner and makes every repository change easier to review.

---

## How I Explain These Projects in an Interview

### S3 Security Auditor

> I built a Python CLI tool that simulates cloud security control validation for AWS S3 buckets. It reads a JSON inventory, evaluates controls like public access, encryption, versioning, and logging, then generates structured findings with severity and remediation guidance. I also added Discord alerting for high-priority issues and automated tests with pytest to validate the audit logic.

### Webhook Validator SecOps

> I built a FastAPI microservice that validates incoming webhooks using HMAC SHA-256. The value of the project is the end-to-end DevSecOps workflow: tests with pytest, Docker packaging, non-root container execution, GitHub Actions CI, Docker image build, and a smoke test that verifies the container responds correctly before future deployment.

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
- Next-step roadmap
- Study notes that explain concepts, not just commands
```

---

## License

This repository is for personal learning and portfolio development.

Code projects are shared freely for educational purposes.

---

**Last Updated:** July 13, 2026  
**Current Week:** Week 2 in progress  
**Next Milestone:** Trivy scan in Webhook Validator CI  
**Momentum:** Strong — Bandit CTF available levels are complete, and the repository now focuses on portfolio-ready DevSecOps projects, structured documentation, and security automation.
