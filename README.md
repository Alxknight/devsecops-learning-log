# DevSecOps Learning Journey

> **12-Month Transformation:** Security Compliance Analyst → DevSecOps Engineer  
> **Timeline:** July 2026 - July 2027  
> **Target Role:** Junior DevOps Engineer or Cloud Security Analyst

## About This Journey

I'm documenting my transition from 2.5 years of security compliance work (questionnaires, SOC 2, UAR) into hands-on DevSecOps engineering. This repository tracks my daily learning, blockers, wins, and progress across a structured 12-month roadmap.

**Time Commitment:**
- Weeks 1-16: 12 hours/week (working two jobs)
- Weeks 17-52: 15-20 hours/week (full focus)

**Target Location:** Remote positions (based in Mexico)  
**Platform Focus:** AWS

---

## Current Status

### Week 1 Complete ✅ (July 2-8, 2026)

**Milestone Achievements:**
- 🎯 **Bandit CTF:** Levels 0-17 completed (security-focused Linux challenges)
- 🛠️ **KodeKloud:** 6 hands-on labs completed
- 📚 **Multi-platform learning:** KillerCoda, LabEx, Exercism rotation established
- 📝 **Documentation:** 17 comprehensive knowledge guides created
- 💻 **Commands Mastered:** 40+ Linux commands with real-world context
- 🚀 **First Portfolio Project:** S3 Security Auditor deployed

**Skills Acquired:**
- Linux fundamentals (file system, navigation, special characters)
- Package management (RPM, YUM, DPKG, APT)
- File permissions (chmod, chown, stat)
- User management (useradd, usermod, service accounts)
- Cron job scheduling
- SSH operations (keys, SCP transfers)
- Security tools (base64, ROT13, netcat, nmap, openssl)
- **Python development** (CLI, JSON processing, logging, exception handling)
- Python virtual environments (venv, pip)
- Cloud CLI basics (AWS EC2, Azure SSH key pairs)
- **Webhook integration** (Discord alerts)
- **Git workflow** (feature branches, merge practices)

---

## Projects

### 🔐 S3 Security Auditor

**Status:** ✅ Functional MVP  
**Folder:** [`auto-audit-script/`](./auto-audit-script/)  
**Language:** Python 3

A CLI tool that audits simulated AWS S3 bucket configurations and detects common cloud security misconfigurations.

**What it does:**
- Reads JSON inventory of S3 buckets (simulated)
- Evaluates 4 security controls:
  - Public access detection (critical in production)
  - Encryption validation
  - Versioning check
  - Access logging verification
- Generates structured JSON findings with severity prioritization
- Maps findings to security frameworks (NIST CSF, ISO 27001, CIS AWS)
- Sends Discord webhook alerts for high-priority issues

**Key Features:**
- Professional logging instead of print statements
- Exception handling with custom `AuditError` class
- Secure secret management via environment variables
- Severity-based risk prioritization (critical/high/medium/low)
- GRC-style finding generation with recommendations

**Example Usage:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run basic audit
python audit.py --input infrastructure.example.json --output findings.example.json

# Run with Discord alerts (high and critical only)
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/your-webhook"
python audit.py --input infrastructure.example.json --output findings.example.json --notify-severity high
```

**Skills Demonstrated:**
- Python CLI development with `argparse`
- JSON processing and validation
- Cloud security fundamentals (AWS S3)
- Security control automation
- Risk prioritization
- Framework mapping (simplified GRC approach)
- Webhook integration
- Environment-based configuration
- Git feature branch workflow

**Current Limitations:**
- Uses simulated JSON data (no real AWS connection yet)
- No `boto3` integration (planned enhancement)
- Simplified framework mapping
- No automated tests yet (next priority)

**Planned Enhancements:**
1. Add pytest unit tests
2. GitHub Actions CI/CD pipeline
3. CSV export option
4. Additional S3 security controls
5. Build failure thresholds
6. Real AWS integration with boto3
7. Expand to IAM, EC2, Security Groups

**Why This Project:**  
Bridges my security compliance background with technical DevSecOps automation. Demonstrates understanding of cloud security controls, risk prioritization, and automated auditing—core skills for cloud security and DevSecOps roles.

---

## Learning Platforms

| Platform | Status | Focus Area |
|----------|--------|------------|
| [KillerCoda](https://killercoda.com) | ✅ Active | Interactive Linux scenarios |
| [LabEx](https://labex.io) | ✅ Active | Hands-on Linux labs |
| [KodeKloud](https://kodekloud.com) | ✅ Active | System administration |
| [Bandit CTF](https://overthewire.org/wargames/bandit/) | ✅ Active | Security challenges |
| [Exercism.org](https://exercism.org/tracks/bash) | ✅ Active | Bash scripting track |
| AWS Free Tier | 📋 Planned | Cloud hands-on practice |

**Why multi-platform?** Each platform teaches the same concepts differently, reinforcing learning through varied approaches.

---

## Roadmap

### Phase 1: Foundations (Months 1-3)
**Status:** 🔄 In Progress - Week 1 of 12 complete

- [x] Week 1: Linux fundamentals intensive
- [x] **Week 1 Bonus:** First Python portfolio project (S3 Security Auditor)
- [ ] Week 2-4: Bash scripting, file operations, networking basics
- [ ] Week 5-8: AWS basics (S3, IAM, EC2, CloudWatch)
- [ ] Week 9-12: Git workflows, Docker fundamentals

### Phase 2: Automation & Infrastructure (Months 4-6)
- [ ] Terraform basics
- [ ] CI/CD pipelines (GitHub Actions)
- [ ] Python for automation (expand S3 auditor)
- [ ] Infrastructure as Code

### Phase 3: Security Integration (Months 7-9)
- [ ] AWS security services
- [ ] Container security
- [ ] Secret management
- [ ] Security scanning in pipelines

### Phase 4: Advanced & Portfolio (Months 10-12)
- [ ] Kubernetes basics
- [ ] Monitoring and logging
- [ ] 3-5 portfolio projects (1/5 complete)
- [ ] Resume and job applications

---

## Week 2 Goals (July 9-15)

- [ ] Add pytest tests to S3 Security Auditor
- [ ] Bandit CTF levels 18-25 (privilege escalation)
- [ ] KodeKloud: Networking fundamentals module
- [ ] AWS CLI hands-on: S3 and IAM operations
- [ ] Consider GitHub Actions for S3 auditor

---

## Progress Metrics

| Metric | Week 1 | Month 1 Target |
|--------|--------|----------------|
| CTF Challenges | 17 | 30 |
| Labs Completed | 9 | 20 |
| Guides Created | 17 | 25 |
| Portfolio Projects | 1 | 1-2 |
| GitHub Commits | ~60+ | 100 |
| Learning Hours | ~25 | 48 |

---

## Key Resources Created

### Week 1 Documentation (17 guides)

**Fundamentals:**
1. Git Essential Guide - From basics to emergency commands
2. Bash Automation Guide - Scripts, error handling, debugging
3. Bash Fundamentals From Zero - Understanding every symbol
4. jq JSON Guide - Parsing for DevSecOps
5. Linux Basic Commands - Essential CLI reference

**System Administration:**
6. Linux System Internals - Kernel, dmesg, block devices
7. Linux User Environment - Shells, PATH, aliases, PS1
8. Linux System Architecture - systemd, filesystem hierarchy
9. Linux Package Management - RPM, YUM, DPKG, APT
10. Linux Permissions - chmod, chown, stat deep dive
11. User Management - useradd, usermod, service accounts
12. Cron Scheduling - Syntax and troubleshooting

**Security:**
13. Bandit CTF Guide - OverTheWire walkthrough
14. Security Tools Reference - base64, ROT13, netcat, nmap, openssl
15. SSH Operations - Keys, SCP, remote commands

**Cloud & Automation:**
16. Python Virtual Environments - venv, pip, requirements.txt
17. Cloud CLI Operations - AWS EC2, Azure SSH keys

---

## Learning Principles

**What's Working:**
- ✅ Multi-platform rotation prevents burnout
- ✅ Weekend deep dives for complex topics
- ✅ Documentation while learning cements knowledge
- ✅ Security-focused challenges maintain motivation
- ✅ Daily consistency (even 1-2 hours makes progress)
- ✅ **Project-based learning accelerates skill acquisition**

**Approach:**
- Hands-on practice over theory
- Real terminal work, not just reading
- Build reference materials as I learn
- Ask "why" not just "how"
- Connect everything to DevSecOps context
- **Ship small projects early to validate learning**

---

## Skills Inventory

### Linux & Command Line
**Level:** Intermediate Beginner  
**Evidence:** 17 Bandit CTF levels, 6 KodeKloud labs, 40+ commands documented

- ✅ File system navigation and operations
- ✅ Package management (RHEL and Debian families)
- ✅ Permissions and ownership
- ✅ User management
- ✅ Cron scheduling
- ✅ SSH operations
- 🔄 Bash scripting (in progress)
- 📋 Networking commands (planned)

### Python
**Level:** Intermediate Beginner  
**Evidence:** S3 Security Auditor project

- ✅ CLI development with argparse
- ✅ JSON file processing
- ✅ Logging and exception handling
- ✅ HTTP requests and webhook integration
- ✅ Environment variable management
- ✅ File I/O operations
- 📋 Testing with pytest (planned)
- 📋 boto3 for AWS (planned)

### Cloud Security
**Level:** Foundational  
**Evidence:** S3 Security Auditor, S3/IAM labs

- ✅ AWS S3 security controls
- ✅ Risk prioritization by severity
- ✅ Cloud security best practices
- 📋 IAM policies and permissions (in progress)
- 📋 AWS security services (planned)

### Git & Version Control
**Level:** Intermediate Beginner  
**Evidence:** Feature branch workflow, daily commits

- ✅ Basic workflows (add, commit, push, pull)
- ✅ Feature branch development
- ✅ Merge practices
- ✅ .gitignore and secret management
- 📋 Pull request workflow (planned)
- 📋 Git rebase and advanced operations (planned)

### DevSecOps Concepts
**Level:** Learning  
**Evidence:** Security automation project, GRC background

- ✅ Security control automation
- ✅ Finding generation and remediation guidance
- ✅ Framework mapping (NIST, ISO, CIS)
- ✅ Webhook alerting for security events
- 📋 CI/CD security integration (planned)
- 📋 Secret scanning (planned)

---

## Contact & Collaboration

**Status:** Open to connecting with others on similar journeys

- Learning in public to stay accountable
- Open to feedback and suggestions
- Interested in study groups or peer learning
- Building portfolio for remote DevSecOps positions

---

## License

This learning log is for personal documentation. Code projects are shared freely under MIT license for others on similar paths.

---

**Last Updated:** July 8, 2026  
**Next Milestone:** Complete Month 1 foundations (July 31, 2026)  
**Momentum:** Strong - Week 1 exceeded expectations, first project shipped! 🚀
