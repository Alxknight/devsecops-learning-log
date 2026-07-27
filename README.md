# DevSecOps Learning Journey

> **Career transition:** Security Compliance / GRC → DevSecOps, Cloud Security, and SRE-style engineering  
> **Repository status:** Active learning repository with the first portfolio project cycle completed  
> **Next milestone:** A comprehension-first DevSecOps project with public study and validation evidence

## About This Repository

This repository documents my transition from **Security Compliance and GRC** into hands-on **DevSecOps, Cloud Security, and reliability engineering**.

It contains portfolio projects, Linux and security labs, CTF notes, troubleshooting exercises, and reproducible learning artifacts. The purpose is not only to show working code, but also to demonstrate how security requirements can be translated into tests, automation, containers, CI/CD controls, and infrastructure practices.

The first project cycle is now considered complete. Its two main projects are being preserved as finished learning milestones rather than continuously expanded.

---

## Current Status

### First Portfolio Cycle — Completed

The following projects reached the final scope defined for this stage of my learning journey:

| Project | Final status | Main focus |
|---|---|---|
| [S3 Security Auditor](python-projects/auto-audit-script/) | Complete for its simulated-audit scope | Python security automation, GRC controls, testing, reporting, and CI security gates |
| [Webhook Validator SecOps](python-projects/webhook-validator-secops/) | Complete for its local DevSecOps delivery scope | FastAPI, HMAC, Docker, CI/CD, Trivy, and local Kubernetes |
| [OverTheWire Bandit Notes](ctf/bandit/) | Available path completed through `bandit33` | Linux security, Git inspection, permissions, automation risks, and shell problem solving |

These projects will remain available as evidence of the first stage of my technical transition. They are not currently under active feature development.

---

## Why the Methodology Is Changing

The first project cycle helped me gain hands-on exposure to Python, testing, Docker, GitHub Actions, vulnerability scanning, Kubernetes, Linux, and cloud fundamentals.

It also revealed an important limitation in my learning process: I was sometimes producing and integrating code faster than I could fully explain it. A working implementation is useful, but it is not enough if I cannot defend the architecture, trace the execution flow, explain the purpose of each dependency, or describe the tradeoffs behind a technical decision.

The next stage keeps the same professional objective but changes the method.

```text
Previous emphasis
Build more features → make the pipeline work → document the result

New emphasis
Study the problem → explain the design → implement a small change
→ validate understanding → preserve evidence → commit
```

This is not a reset of the learning journey. It is a move from **implementation-first practice** toward **comprehension-first engineering**.

---

## Next Project — In Preparation

My next project will be published after its structure and validation process are defined.

The project will still focus on DevSecOps and secure software delivery, but every meaningful code change will be connected to evidence that I studied and validated the concepts involved.

### Planned Evidence for Each Meaningful Change

A feature or architectural change should answer questions such as:

- What problem does this change solve?
- Why does this component or function exist?
- Why was this technology, library, protocol, or service selected?
- What alternatives were considered?
- How does data move through the system?
- What security or reliability risks does the change introduce?
- How was the behavior tested?
- Can I explain the implementation without relying only on the generated code?

The exact format is still being refined, but the intended workflow is:

```text
1. Define the problem
2. Study the required concepts
3. Record the architecture or technical decision
4. Implement one controlled change
5. Test the behavior
6. Complete a comprehension-validation session
7. Record mistakes, corrections, and remaining gaps
8. Create the commit
```

### Proposed Definition of Done

A meaningful change will not be considered complete only because the code runs. It should also include enough evidence to show that I can:

- Explain its purpose in plain language.
- Identify the main execution and data flow.
- Explain the role of the libraries and services used.
- Describe at least one relevant security consideration.
- Interpret the test results.
- Reproduce the change from the documentation.
- Defend the decision in a technical interview.

This methodology is intended to make future progress slower, more deliberate, and more credible.

---

## Completed Portfolio Projects

## 1. S3 Security Auditor

**Status:** Complete learning version  
**Folder:** `python-projects/auto-audit-script/`  
**Focus:** Cloud Security, GRC Automation, Python, and CI/CD security gates

The S3 Security Auditor is a Python CLI that evaluates a simulated JSON inventory of S3 buckets. It detects common misconfigurations and generates structured findings.

### Final Capabilities

- Public-access, encryption, versioning, and logging checks
- Environment-aware severity assignment
- JSON and CSV reports
- GRC-style recommendations and simplified framework mappings
- Optional Discord webhook notifications
- Environment-variable secret handling
- `pytest` coverage, including mocked webhook tests
- GitHub Actions CI
- `--fail-on-severity` behavior for pipeline-style blocking
- Explicit error handling and exit codes

### Scope Boundary

The project intentionally uses simulated local inventory. It does not connect to a real AWS account or inspect live IAM policies, bucket policies, or ACLs.

---

## 2. Webhook Validator SecOps

**Status:** Complete local DevSecOps learning version  
**Folder:** `python-projects/webhook-validator-secops/`  
**Focus:** Secure API delivery, containers, CI/CD, vulnerability management, and Kubernetes

Webhook Validator SecOps is a FastAPI service that verifies incoming webhook signatures with **HMAC SHA-256**.

### Final Capabilities

- `/health`, `/ready`, and `/webhook` endpoints
- HMAC SHA-256 verification with `hmac.compare_digest()`
- Environment-based secret configuration
- Request tracing through `X-Request-ID`
- Safe logging without exposing secrets, signatures, or complete payloads
- Automated tests with `pytest`
- Alpine-based Docker image
- Numeric non-root UID/GID
- Docker health check
- GitHub Actions tests, image build, Trivy scan, and smoke test
- CVE triage documented in `SECURITY_AUDIT.md`
- Kubernetes Namespace, Secret, Deployment, and Service manifests
- Readiness and liveness probes
- Resource requests and limits
- Restricted container security context
- Reproducible local deployment with Minikube and Bash scripts

### Scope Boundary

The final version demonstrates a secure local delivery path. Publishing the image to a registry and deploying it to a managed or public cloud environment are not part of this completed scope.

---

## Supporting Technical Practice

The repository also includes structured practice beyond the two main projects.

| Area | Practical work completed |
|---|---|
| Linux | Permissions, ownership, users, groups, SSH hardening, services, logs, archives, cron, and troubleshooting |
| Git | Branch workflows, repository cleanup, `.gitignore`, history inspection, tags, forks, and bare repositories |
| Security labs | OverTheWire Bandit through `bandit33`, secret exposure patterns, `setuid`, restricted shells, and automation risks |
| AWS | Budgets, S3 versioning, security groups, subnets, and foundational CLI practice |
| Azure | SSH keys, virtual machines, VNets, resource groups, and CLI validation |
| MLOps foundations | Dependency locking, generated-artifact cleanup, virtual environments, and Jupyter troubleshooting |
| Containers | Docker builds, non-root execution, health checks, smoke tests, Alpine migration, and Trivy scanning |
| Kubernetes | Minikube, manifests, Secrets, probes, resource controls, security contexts, and deployment troubleshooting |

---

## Repository Structure

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
│   │   ├── tests/
│   │   └── README.md
│   └── webhook-validator-secops/
│       ├── app/
│       ├── tests/
│       ├── k8s/
│       ├── scripts/
│       ├── Dockerfile
│       ├── pyproject.toml
│       ├── requirements.txt
│       ├── SECURITY_AUDIT.md
│       └── README.md
└── README.md
```

---

## Skills Demonstrated So Far

### Python and Application Development

- CLI design with `argparse`
- JSON and CSV processing
- Logging and exception handling
- FastAPI endpoints
- HMAC validation
- Environment-based configuration
- Unit tests, parametrization, temporary files, and mocks

### DevOps and SRE Foundations

- Git feature-branch workflow
- GitHub Actions CI
- Job dependencies and path filters
- Docker image creation
- Non-root containers
- Health and readiness design
- Container smoke testing
- Kubernetes manifests and local deployment
- Linux service and application troubleshooting

### DevSecOps and Cloud Security

- Security control automation
- Severity-based risk prioritization
- Machine-readable and human-readable evidence
- Secret-handling practices
- CI security gates
- Dependency and base-image vulnerability triage
- Container attack-surface reduction
- Kubernetes security contexts and resource controls
- Foundational AWS and Azure CLI practice

---

## How I Present This Learning Stage

The first project cycle demonstrates that I can take small applications and connect them to practical engineering and security workflows.

The S3 Security Auditor translates cloud-control requirements into executable Python checks, tests, structured evidence, alerting, and pipeline exit behavior.

The Webhook Validator demonstrates a local end-to-end delivery path: application code, automated tests, containerization, CI, vulnerability scanning, security hardening, and Kubernetes deployment.

The next project will add another requirement: the repository must show not only **what I built**, but also **how I validated that I understood it**.

---

## Repository Principles Going Forward

```text
Working code is required, but not sufficient.

A strong project should include:
- A clearly defined problem
- Reproducible commands
- Tests and failure scenarios
- Security and reliability considerations
- Technical decision records
- Architecture and data-flow explanations
- Evidence of comprehension validation
- Honest limitations
- A history of small, explainable commits
```

---

## License

This repository is maintained for personal learning and portfolio development. Code and notes are shared for educational purposes.

---

**Last updated:** July 27, 2026  
**Current stage:** First portfolio cycle completed  
**Next milestone:** Publish a comprehension-first DevSecOps project with study and validation evidence attached to meaningful changes
