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

### Week 2 In Progress 🔄 (July 9-15, 2026)

Week 2 has officially started. The current focus is to continue strengthening Linux, security fundamentals, Python automation, testing practices, and AWS basics while improving the first portfolio project.

**Week 2 Progress So Far:**
- 🧪 **Pytest Coverage Added:** S3 Security Auditor now has automated unit tests
- ✅ **Test Result:** 28 tests passing locally
- ⚙️ **Pytest Configuration:** Added `pytest.ini` to solve local import path configuration
- 🌿 **Branch Workflow Practice:** New feature work implemented through dedicated branches
- 🔐 **Portfolio Project Improvement:** S3 Security Auditor is becoming more production-like



### Week 2 Additional Milestones (July 10)

- ✅ **Bandit CTF:** Advanced from levels **21 → 25**
- ✅ **KodeKloud:** Completed additional Linux, Git, AWS, Azure and MLOps/Jupyter labs
- ✅ **Linux Administration:** User expiration, supplementary groups, SSH hardening with `PermitRootLogin no`
- ✅ **Git:** Cloned bare repositories and practiced remote repository workflows
- ✅ **AWS:** Created Security Groups using AWS CLI
- ✅ **Azure:** Provisioned Ubuntu VM using Azure CLI and troubleshot authorization issues
- ✅ **MLOps:** Diagnosed and repaired JupyterLab configuration and networking issues
- ✅ **Bash Automation:** First custom shell script executed through cron
- ✅ **Security:** Automated brute force exercise with `seq`, `for`, `nc` and `grep` in a controlled environment

### Week 1 Complete ✅ (July 2-8, 2026)

**Milestone Achievements:**
- 🎯 **Bandit CTF:** Levels 0-21 completed (25 security challenges!)
- 🛠️ **KodeKloud:** 7 hands-on labs completed
- 📚 **Multi-platform learning:** KillerCoda, LabEx, Exercism rotation established
- 📝 **Documentation:** 17+ comprehensive knowledge guides created
- 💻 **Commands Mastered:** 50+ Linux commands with real-world context
- 🚀 **First Portfolio Project:** S3 Security Auditor deployed
- 🔔 **Discord Alerting:** Webhook notifications added for high-priority audit findings

**Skills Acquired:**

*Linux Fundamentals:*
- File system navigation and special characters
- Package management (RPM, YUM, DPKG, APT)
- File permissions (chmod, chown, stat)
- User management (useradd, usermod, service accounts)
- Cron job scheduling
- Compression and archiving (tar, gzip, zcat)
- File search (find, grep -rl)
- I/O redirection (>, 2>, stdout vs stderr)

*Security Tools:*
- Port scanning (nmap with service detection)
- SSL/TLS connections (openssl s_client)
- Netcat listeners and TCP connections
- SSH advanced (private keys, remote execution, permissions)
- Encoding tools (base64, ROT13, xxd)
- setuid binaries and privilege escalation concepts

*Python Development:*
- CLI development (argparse, logging)
- JSON processing and validation
- HTTP requests and webhook integration
- Exception handling
- Environment variable management
- Virtual environments (venv, pip)
- Automated unit testing with pytest
- Test configuration with pytest.ini
- Temporary file testing with tmp_path
- Parametrized test cases with pytest.mark.parametrize

*Cloud & DevOps:*
- AWS CLI basics (EC2, S3 operations)
- Azure CLI (SSH key management)
- Git workflow (feature branches, merge practices)
- SCP file transfers
- Branch-based feature development
- Test validation before merging changes

---

## Projects

### 🔐 S3 Security Auditor

**Status:** ✅ Functional MVP + Discord Alerts + Pytest Coverage  
**Folder:** [`python-projects/auto-audit-script/`](./python-projects/auto-audit-script/)  
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
- Runs automated tests to validate audit logic and input validation

**Key Features:**
- Professional logging instead of print statements
- Exception handling with custom `AuditError` class
- Secure secret management via environment variables
- Severity-based risk prioritization (critical/high/medium/low)
- GRC-style finding generation with recommendations
- Optional Discord webhook integration
- Severity threshold filtering for notifications
- Automated pytest coverage for core audit logic

**Example Usage:**
```bash
# Install runtime dependencies
pip install -r requirements.txt

# Run basic audit
python audit.py --input infrastructure.example.json --output findings.example.json

# Run with Discord alerts (high and critical only)
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/your-webhook"
python audit.py --input infrastructure.example.json --output findings.example.json --notify-severity high
```

**Testing:**
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run tests with verbose output
pytest -v
```

**Latest Test Result:**
```text
28 passed in 0.96s
```

**Test Coverage Includes:**
- Public production bucket detection
- Public staging bucket detection
- Secure bucket behavior
- Missing encryption detection
- Missing versioning detection
- Missing access logging detection
- Invalid bucket object handling
- Missing or invalid bucket name handling
- Severity assignment logic
- Notification severity threshold logic
- Valid JSON loading
- Missing file handling
- Invalid JSON handling
- Invalid JSON structure handling

**Skills Demonstrated:**
- Python CLI development with `argparse`
- JSON processing and validation
- Cloud security fundamentals (AWS S3)
- Security control automation
- Risk prioritization
- Framework mapping (simplified GRC approach)
- Webhook integration
- Environment-based configuration
- Automated testing with pytest
- Test parametrization
- Temporary file testing
- Git feature branch workflow

**Implementation Branches Completed:**
1. ✅ Production-ready S3 security auditor
2. ✅ Discord webhook alerting
3. ✅ Pytest coverage for S3 audit logic

**Planned Enhancements:**
1. ✅ Discord webhook alerting (completed)
2. ✅ Pytest unit tests (completed - 28 passing tests)
3. Add mocked tests for Discord webhook behavior
4. GitHub Actions CI/CD pipeline
5. CSV export option
6. Additional S3 security controls
7. Real AWS integration with boto3
8. Expand to IAM, EC2, Security Groups

**Why This Project:**  
Bridges my security compliance background with technical DevSecOps automation. Demonstrates understanding of cloud security controls, risk prioritization, automated auditing, alerting, and professional software practices such as feature branching and automated testing—core skills for cloud security and DevSecOps roles.

---

## Learning Platforms

| Platform | Status | Focus Area | Progress |
|----------|--------|------------|----------|
| [Bandit CTF](https://overthewire.org/wargames/bandit/) | ✅ Active | Security challenges | 25/34 levels |
| [KodeKloud](https://kodekloud.com) | ✅ Active | System administration | 7 labs |
| [KillerCoda](https://killercoda.com) | ✅ Active | Interactive scenarios | 2 lessons |
| [LabEx](https://labex.io) | ✅ Active | Hands-on Linux labs | 4 labs |
| [Exercism.org](https://exercism.org/tracks/bash) | ✅ Active | Bash scripting | 1 exercise |
| AWS Free Tier | 📋 Planned | Cloud hands-on | Next |

**Why multi-platform?** Each platform teaches the same concepts differently, reinforcing learning through varied approaches. Bandit CTF adds security-focused problem-solving that aligns with DevSecOps goals.

---

## Roadmap

### Phase 1: Foundations (Months 1-3)
**Status:** 🔄 In Progress - Week 2 of 12

- [x] Week 1: Linux fundamentals intensive
- [x] **Week 1 Bonus:** First Python portfolio project (S3 Security Auditor)
- [x] **Week 1 Bonus:** Discord webhook alerting for S3 Security Auditor
- [x] **Week 1 Bonus:** Bandit CTF levels 0-25 (security mindset development)
- [x] **Week 2:** Pytest coverage for S3 Security Auditor
- [ ] Week 2-4: Complete Bandit CTF, bash scripting, networking basics
- [ ] Week 5-8: AWS basics (S3, IAM, EC2, CloudWatch)
- [ ] Week 9-12: Git workflows, Docker fundamentals

### Phase 2: Automation & Infrastructure (Months 4-6)
- [ ] Terraform basics
- [ ] CI/CD pipelines (GitHub Actions for S3 auditor)
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
- [ ] 3-5 portfolio projects (1/5 complete ✅)
- [ ] Resume and job applications

---

## Week 2 Goals (July 9-15)

**Status:** 🔄 In Progress

- [ ] Complete Bandit CTF levels 22-34
- [x] Add pytest tests to S3 Security Auditor
- [ ] Add mocked tests for Discord webhook alerting
- [ ] KodeKloud: Networking fundamentals module
- [ ] AWS CLI hands-on: S3 and IAM operations
- [ ] GitHub Actions CI/CD for S3 auditor (stretch goal)

---

## Progress Metrics

| Metric | Current Progress | Month 1 Target |
|--------|------------------|----------------|
| CTF Challenges | 21 | 34 (all Bandit) |
| Labs Completed | 17 | 20 |
| Guides Created | 17+ | 25 |
| Portfolio Projects | 1 ✅ | 1-2 |
| Automated Tests | 28 ✅ | 30+ |
| GitHub Commits | ~70+ | 100 |
| Learning Hours | ~28+ | 48 |

**Progress Analysis:** Week 1 exceeded the original hourly target due to high engagement with CTF challenges and the first project. Week 2 has started with a strong professional improvement: automated pytest coverage for the S3 Security Auditor.

---

## Key Commands Mastered This Week

### Security & Networking
```bash
# Port scanning
nmap -sV -p 31000-32000 localhost

# SSL/TLS manual connection
openssl s_client -connect localhost:31790 -quiet

# Netcat listener
echo "password" | nc -l -p 12345 &

# SSH with private key
ssh -i ~/.ssh/keyfile user@host -p 2220

# Remote command execution
ssh user@host -p 2220 "cat readme"

# Secure file transfer
scp -P 2220 user@host:/path/file .
```

### File Operations
```bash
# Create compressed tarball
tar -czvf archive.tar.gz directory/

# Extract gzip file
gunzip file.gz

# Read compressed file without extracting
zcat file.gz > output.txt

# Find files by name
find /path -type f -name "filename"

# Find files containing text
grep -rl "search text" /path

# Compare files
diff file1 file2 | grep "^>"
```

### I/O Redirection
```bash
# Redirect stdout
command > output.txt

# Redirect stderr
command 2> error.txt

# Create file with echo
echo "content" > file.txt
```

### Permissions & Privilege
```bash
# Secure SSH key permissions
chmod 600 keyfile

# Execute setuid binary
./setuid-binary command
```

### Python Testing
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run pytest
pytest

# Run pytest with verbose output
pytest -v

# Create pytest configuration
cat > pytest.ini << 'EOF'
[pytest]
pythonpath = .
testpaths = tests
EOF
```

### Git Branch Workflow
```bash
# Create and switch to a feature branch
git switch -c feature/add-pytest-coverage

# Check current branch and changes
git status
git branch

# Stage and commit changes
git add .
git commit -m "Add pytest coverage for S3 audit logic"

# Push branch to GitHub
git push -u origin feature/add-pytest-coverage
```

---

## Skills Inventory

### Linux & Command Line
**Level:** Intermediate Beginner  
**Evidence:** 21 Bandit CTF levels, 13 KodeKloud labs, 50+ commands documented

- ✅ File system navigation and operations
- ✅ Package management (RHEL and Debian families)
- ✅ Permissions and ownership
- ✅ User management
- ✅ Cron scheduling
- ✅ SSH operations (keys, remote execution, SCP)
- ✅ Compression and archiving (tar, gzip, zcat)
- ✅ File search (find, grep)
- ✅ I/O redirection (stdout, stderr)
- 🔄 Bash scripting (in progress)
- 📋 Networking commands (planned)

### Security Tools
**Level:** Foundational  
**Evidence:** Bandit CTF levels 0-25

- ✅ Port scanning (nmap)
- ✅ SSL/TLS connections (openssl)
- ✅ Netcat for TCP connections
- ✅ Encoding tools (base64, ROT13, xxd)
- ✅ Privilege escalation concepts (setuid)
- ✅ SSH key security
- 📋 Vulnerability scanning (planned)
- 📋 SIEM concepts (planned)

### Python
**Level:** Intermediate Beginner  
**Evidence:** S3 Security Auditor project with Discord alerting and pytest coverage

- ✅ CLI development with argparse
- ✅ JSON file processing
- ✅ Logging and exception handling
- ✅ HTTP requests and webhook integration
- ✅ Environment variable management
- ✅ File I/O operations
- ✅ Testing with pytest
- ✅ Test parametrization
- ✅ Input validation testing
- ✅ Temporary file testing with tmp_path
- 📋 Mocking external services (planned)
- 📋 boto3 for AWS (planned)

### Cloud Security
**Level:** Foundational  
**Evidence:** S3 Security Auditor, S3/IAM labs

- ✅ AWS S3 security controls
- ✅ Risk prioritization by severity
- ✅ Cloud security best practices
- ✅ Security finding generation
- ✅ Alerting for high-priority security findings
- 📋 IAM policies and permissions (in progress)
- 📋 AWS security services (planned)

### Git & Version Control
**Level:** Intermediate Beginner  
**Evidence:** Feature branch workflow, daily commits, branch-based implementation work

- ✅ Basic workflows (add, commit, push, pull)
- ✅ Feature branch development
- ✅ Merge practices
- ✅ .gitignore and secret management
- ✅ Branch-based implementation workflow
- 📋 Pull request workflow (planned)
- 📋 Git rebase (planned)

### DevSecOps Concepts
**Level:** Learning  
**Evidence:** Security automation project, webhook alerting, pytest coverage, GRC background

- ✅ Security control automation
- ✅ Finding generation and remediation guidance
- ✅ Framework mapping (NIST, ISO, CIS)
- ✅ Webhook alerting for security events
- ✅ Automated test validation for security logic
- ✅ Privilege escalation awareness
- 📋 CI/CD security integration (planned)
- 📋 Secret scanning (planned)

---

## Learning Principles

**What's Working:**
- ✅ Multi-platform rotation prevents burnout
- ✅ Weekend deep dives for complex topics
- ✅ Documentation while learning cements knowledge
- ✅ **Security CTF challenges maintain high motivation**
- ✅ Daily consistency (even 1-2 hours makes progress)
- ✅ **Project-based learning accelerates skill acquisition**
- ✅ **Problem-solving mindset through Bandit CTF**
- ✅ **Feature branches make new implementations safer**
- ✅ **Automated tests increase confidence before merging changes**

**Approach:**
- Hands-on practice over theory
- Real terminal work, not just reading
- Build reference materials as I learn
- Ask "why" not just "how"
- Connect everything to DevSecOps context
- **Ship small projects early to validate learning**
- **Security-first thinking in all exercises**
- **Use branches for every meaningful implementation**
- **Add tests as projects become more realistic**

---

## Week 1 Retrospective

### What Went Well
- Exceeded learning hour target (28 vs 12 planned)
- Completed first portfolio project ahead of schedule
- Added Discord alerting to make the project more realistic
- Bandit CTF proved highly engaging and educational
- Multi-platform strategy working excellently
- Security mindset developing naturally through CTF

### Key Learnings
- **WSL filesystem matters:** SSH keys need proper Linux paths (~/.ssh/)
- **Encoding ≠ Encryption:** Critical security distinction learned
- **setuid is powerful:** Privilege escalation concepts clarified
- **Remote SSH execution:** Opens automation possibilities
- **Python isn't scary:** Built working CLI tool from beginner level
- **Webhooks add operational value:** Alerts make security findings actionable
- **Branch workflow is safer:** Feature branches isolate changes before merge

### Challenges Overcome
- WSL permission issues with SSH keys (solved with filesystem migration)
- OpenSSL noise in output (learned -quiet flag)
- Understanding setuid behavior (researched and practiced)
- Bandit Level 18 shell trap (learned remote execution workaround)
- Discord webhook secret handling (solved with environment variables)

### Momentum Factors
- Security-focused challenges > generic tutorials
- Real problems > synthetic exercises
- Building something useful > following recipes
- Weekend deep dives = maximum productivity
- Small portfolio improvements compound quickly

---

## Week 2 Notes

### What Has Started Well
- Added automated tests early in the week
- Validated project logic with 28 passing tests
- Solved pytest local import issue using `pytest.ini`
- Continued using feature branches for clean implementation work

### Current Technical Learning
- Pytest test structure
- Parametrized test cases
- Temporary file testing with `tmp_path`
- Local Python import path configuration
- Testing security control logic before adding more features

### Next Recommended Implementation
The next professional improvement should be a new branch for mocked Discord webhook tests:

```bash
git switch -c feature/test-discord-webhook-alerts
```

This would demonstrate how to test external integrations without sending real messages to Discord.

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

**Last Updated:** July 9, 2026  
**Current Week:** Week 2 in progress (July 9-15, 2026)  
**Next Milestone:** Complete Month 1 foundations (July 31, 2026)  
**Momentum:** Strong - Week 2 started with 28 passing tests added to the first portfolio project 🚀


---

## Week 2 Technical Highlights (Updated)

### New KodeKloud Skills
- Linux user lifecycle management (`useradd -e`, `chage`)
- Supplementary groups with `usermod -aG`
- SSH hardening and configuration auditing using `grep` and `sed`
- Git bare repository cloning
- AWS Security Group creation with AWS CLI
- Azure VM provisioning with Azure CLI
- JupyterLab troubleshooting (ports, root directory, services)
- Service validation using `ss`, `systemctl` and process inspection

### Bandit CTF Progress (Levels 21–25)

**New concepts mastered:**
- Cron job auditing
- Reading and understanding automation scripts
- Dynamic file generation with `md5sum`
- Writing executable Bash scripts
- File permission management with `chmod`
- Secure temporary workspace usage
- Bash automation (`for`, `seq`, pipes)
- Netcat communication with local daemons
- Controlled brute-force automation
- Thinking like both an attacker and defender by analyzing automation, permissions and exposed secrets

### Updated Progress
- **Bandit:** 25 / 34 levels completed
- **KodeKloud Labs:** 13 completed
- **Portfolio Project:** 1 production-style project with testing
- **Python Tests:** 28 passing