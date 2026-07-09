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
- 🎯 **Bandit CTF:** Levels 0-21 completed (21 security challenges!)
- 🛠️ **KodeKloud:** 7 hands-on labs completed
- 📚 **Multi-platform learning:** KillerCoda, LabEx, Exercism rotation established
- 📝 **Documentation:** 17+ comprehensive knowledge guides created
- 💻 **Commands Mastered:** 50+ Linux commands with real-world context
- 🚀 **First Portfolio Project:** S3 Security Auditor deployed

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

*Cloud & DevOps:*
- AWS CLI basics (EC2, S3 operations)
- Azure CLI (SSH key management)
- Git workflow (feature branches, merge practices)
- SCP file transfers

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

**Planned Enhancements:**
1. ✅ Discord webhook alerting (completed!)
2. Add pytest unit tests
3. GitHub Actions CI/CD pipeline
4. CSV export option
5. Additional S3 security controls
6. Real AWS integration with boto3
7. Expand to IAM, EC2, Security Groups

**Why This Project:**  
Bridges my security compliance background with technical DevSecOps automation. Demonstrates understanding of cloud security controls, risk prioritization, and automated auditing—core skills for cloud security and DevSecOps roles.

---

## Learning Platforms

| Platform | Status | Focus Area | Progress |
|----------|--------|------------|----------|
| [Bandit CTF](https://overthewire.org/wargames/bandit/) | ✅ Active | Security challenges | 21/34 levels |
| [KodeKloud](https://kodekloud.com) | ✅ Active | System administration | 7 labs |
| [KillerCoda](https://killercoda.com) | ✅ Active | Interactive scenarios | 2 lessons |
| [LabEx](https://labex.io) | ✅ Active | Hands-on Linux labs | 4 labs |
| [Exercism.org](https://exercism.org/tracks/bash) | ✅ Active | Bash scripting | 1 exercise |
| AWS Free Tier | 📋 Planned | Cloud hands-on | Next |

**Why multi-platform?** Each platform teaches the same concepts differently, reinforcing learning through varied approaches. Bandit CTF adds security-focused problem-solving that aligns with DevSecOps goals.

---

## Roadmap

### Phase 1: Foundations (Months 1-3)
**Status:** 🔄 In Progress - Week 1 of 12 complete

- [x] Week 1: Linux fundamentals intensive
- [x] **Week 1 Bonus:** First Python portfolio project (S3 Security Auditor)
- [x] **Week 1 Bonus:** Bandit CTF levels 0-21 (security mindset development)
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

- [ ] Complete Bandit CTF levels 22-34
- [ ] Add pytest tests to S3 Security Auditor
- [ ] KodeKloud: Networking fundamentals module
- [ ] AWS CLI hands-on: S3 and IAM operations
- [ ] GitHub Actions CI/CD for S3 auditor (stretch goal)

---

## Progress Metrics

| Metric | Week 1 | Month 1 Target |
|--------|--------|----------------|
| CTF Challenges | 21 | 34 (all Bandit) |
| Labs Completed | 11 | 20 |
| Guides Created | 17+ | 25 |
| Portfolio Projects | 1 ✅ | 1-2 |
| GitHub Commits | ~70+ | 100 |
| Learning Hours | ~28 | 48 |

**Week 1 Analysis:** Exceeded hourly target by 150%+ due to high engagement with CTF challenges and first project. This pace is sustainable with current momentum.

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

---

## Skills Inventory

### Linux & Command Line
**Level:** Intermediate Beginner  
**Evidence:** 21 Bandit CTF levels, 7 KodeKloud labs, 50+ commands documented

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
**Evidence:** Bandit CTF levels 0-21

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
- ✅ Security finding generation
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
- 📋 Git rebase (planned)

### DevSecOps Concepts
**Level:** Learning  
**Evidence:** Security automation project, GRC background

- ✅ Security control automation
- ✅ Finding generation and remediation guidance
- ✅ Framework mapping (NIST, ISO, CIS)
- ✅ Webhook alerting for security events
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

**Approach:**
- Hands-on practice over theory
- Real terminal work, not just reading
- Build reference materials as I learn
- Ask "why" not just "how"
- Connect everything to DevSecOps context
- **Ship small projects early to validate learning**
- **Security-first thinking in all exercises**

---

## Week 1 Retrospective

### What Went Well
- Exceeded learning hour target (28 vs 12 planned)
- Completed first portfolio project ahead of schedule
- Bandit CTF proved highly engaging and educational
- Multi-platform strategy working excellently
- Security mindset developing naturally through CTF

### Key Learnings
- **WSL filesystem matters:** SSH keys need proper Linux paths (~/.ssh/)
- **Encoding ≠ Encryption:** Critical security distinction learned
- **setuid is powerful:** Privilege escalation concepts clarified
- **Remote SSH execution:** Opens automation possibilities
- **Python isn't scary:** Built working CLI tool from beginner level

### Challenges Overcome
- WSL permission issues with SSH keys (solved with filesystem migration)
- OpenSSL noise in output (learned -quiet flag)
- Understanding setuid behavior (researched and practiced)
- Bandit Level 18 shell trap (learned remote execution workaround)

### Momentum Factors
- Security-focused challenges > generic tutorials
- Real problems > synthetic exercises
- Building something useful > following recipes
- Weekend deep dives = maximum productivity

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
**Momentum:** Exceptional - Week 1 crushed expectations! 21 CTF levels + first project deployed 🚀