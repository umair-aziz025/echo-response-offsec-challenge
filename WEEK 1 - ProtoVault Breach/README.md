# Week 1 - ProtoVault Breach 🔐

**Challenge Name:** ProtoVault Database Leak Investigation  
**Difficulty:** Beginner  
**Category:** Incident Response, Digital Forensics, OSINT  
**Date Completed:** October 11, 2025

---

## 📖 Challenge Overview

In this cybersecurity incident response challenge, I investigated a database breach at **ProtoVault**, a secure facility managed by the Everbound Order. A threat actor claimed to have obtained the organization's database and issued ransom demands, threatening to expose sensitive data if their demands weren't met.

As a digital investigator, my mission was to:
1. Analyze the application source code for security vulnerabilities
2. Identify the source of the database leak
3. Locate and verify the publicly exposed database
4. Extract specific evidence to confirm the breach

---

## 🎯 Challenge Questions & Answers

### Question 1: Database Connection String
**Task:** Review the database connection string to ensure it is secure.

**Answer:**
```
postgresql://assetdba:8d631d2207ec1debaafd806822122250@pgsql_prod_db01.protoguard.local/pgamgt?sslmode=verify-full
```

**Location:** `source_code/app/app.py` (line 10)

**Security Issue:** Hardcoded credentials in source code ❌

---

### Question 2: Source File That Leaked the Database
**Task:** Identify which source file may have leaked the database.

**Answer:**
```
backup_db.py
```

**Discovery Method:** 
- Analyzed Git commit history
- Found suspicious commit: "Remove backup scripts"
- Recovered deleted file from Git history using:
  ```bash
  git show 1cc71b0^:app/util/backup_db.py
  ```

---

### Question 3: Password Hash Verification
**Task:** Verify the leaked database by submitting Naomi Adler's password hash.

**Answer:**
```
pbkdf2:sha256:600000$YQqIvcDipYLzzXPB$598fe450e5ac019cdd41b4b10c5c21515573ee63a8f4881f7d721fd74ee43d59
```

**User Details:**
- **Name:** Naomi Adler
- **Username:** naomi.adler
- **Role:** Cognitive Systems Research
- **User ID:** 11

---

### Question 4: Public Address of Database Leak
**Task:** Submit the public URL where the database was leaked.

**Answer:**
```
https://protoguard-asset-management.s3.us-east-2.amazonaws.com/db_backup.xyz
```

**Details:**
- **S3 Bucket:** protoguard-asset-management
- **Region:** us-east-2 (US East - Ohio)
- **File:** db_backup.xyz
- **Encoding:** ROT13 (easily reversible)
- **Access Level:** PUBLIC (no authentication required) 🚨

---

## 🔍 Investigation Methodology

### Phase 1: Source Code Analysis
1. **Reviewed Flask application code** (`app.py`)
   - Found hardcoded database credentials
   - No environment variables or secrets management
   - Identified potential security weaknesses

### Phase 2: Git Repository Forensics
```bash
# List all commits
git log --oneline --all

# Examine suspicious commit
git show 1cc71b0 --stat

# Recover deleted file
git show 1cc71b0^:app/util/backup_db.py
```

**Key Finding:** The `backup_db.py` script:
- Automated database backups via SSH
- Encoded backups using ROT13 (weak obfuscation)
- Uploaded to public S3 bucket
- No encryption or access controls

### Phase 3: Data Exfiltration Verification
```python
import requests
import codecs

# Download the leaked database
url = "https://protoguard-asset-management.s3.us-east-2.amazonaws.com/db_backup.xyz"
response = requests.get(url)

# Decode ROT13
decoded_db = codecs.decode(response.text, 'rot_13')

# Search for Naomi Adler
# Found user record with password hash
```

### Phase 4: Evidence Extraction
- Downloaded complete database dump (2,400+ lines)
- Decoded ROT13 encoding
- Located Naomi Adler's user record
- Verified all table structures and sensitive data

---

## 🚨 Critical Vulnerabilities Discovered

| Severity | Vulnerability | Description |
|----------|--------------|-------------|
| 🔴 **CRITICAL** | Hardcoded Credentials | Database password stored in `app.py` source code |
| 🔴 **CRITICAL** | Public S3 Bucket | Entire database dump publicly accessible without authentication |
| 🟡 **HIGH** | Weak Encoding | ROT13 provides no real security (trivial to decode) |
| 🟡 **HIGH** | Git History Exposure | Sensitive files still accessible after deletion |
| 🟠 **MEDIUM** | No Secrets Management | No use of environment variables or vault systems |
| 🟠 **MEDIUM** | Insufficient Logging | No detection of unauthorized backup access |

---

## 🛠️ Tools & Techniques Used

- **Git Forensics:** Version control history analysis
- **Python:** Automated download and decoding scripts
- **ROT13 Decoding:** Cipher analysis (codecs library)
- **S3 Analysis:** AWS cloud storage investigation
- **Source Code Review:** Security vulnerability assessment
- **OSINT:** Open source intelligence gathering

---

## 📁 Solution Files

This directory contains:

1. **`INVESTIGATION_REPORT.md`** - Comprehensive forensic analysis report
   - Detailed investigation methodology
   - Security vulnerabilities identified
   - Remediation recommendations
   - Impact assessment

2. **`analyze_leak.py`** - Python script to download and decode the leaked database
   ```python
   # Usage:
   python analyze_leak.py
   ```

3. **`README.md`** - This file (challenge overview and summary)

---

## 💡 Key Takeaways & Lessons Learned

### Security Best Practices Violated:
1. ❌ Never hardcode credentials in source code
2. ❌ Don't rely on obfuscation (ROT13) for security
3. ❌ Always make S3 buckets private by default
4. ❌ Sensitive files in Git history are never truly deleted
5. ❌ Implement proper secrets management

### Recommended Security Controls:
1. ✅ Use environment variables or secrets managers (AWS Secrets Manager, HashiCorp Vault)
2. ✅ Implement proper encryption (AES-256, not ROT13)
3. ✅ Configure S3 bucket policies with least privilege
4. ✅ Use `.gitignore` and Git history cleaning tools
5. ✅ Enable audit logging and monitoring
6. ✅ Regular security code reviews and penetration testing

---

## 🎓 Skills Demonstrated

- **Digital Forensics:** Git repository analysis and artifact recovery
- **Incident Response:** Systematic investigation methodology
- **Cryptanalysis:** Decoding and cipher identification
- **Cloud Security:** AWS S3 security analysis
- **Python Scripting:** Automation and data processing
- **Security Assessment:** Vulnerability identification and risk analysis
- **OSINT:** Public data source investigation

---

## 📊 Challenge Statistics

- **Time to Solve:** ~45 minutes
- **Files Analyzed:** 8+ source files
- **Git Commits Reviewed:** 21 commits
- **Database Records:** 2,400+ lines
- **Vulnerabilities Found:** 6 critical/high severity issues
- **Tools Used:** 5+ different tools and techniques

---

## 🏆 Challenge Completed

**Status:** ✅ SOLVED  
**All Questions Answered:** 4/4  
**Evidence Verified:** ✓  
**Report Generated:** ✓

---

## 👨‍💻 Author

**Umair Aziz**  
GitHub: [@umair-aziz025](https://github.com/umair-aziz025)  
Repository: [echo-response-offsec-challenge](https://github.com/umair-aziz025/echo-response-offsec-challenge)

---

## 📚 References

- OffSec Echo Response Event - Proving Grounds: The Gauntlet
- OWASP Top 10 - Security Misconfiguration
- AWS S3 Security Best Practices
- Git Security Best Practices
- NIST Incident Response Framework

---

*"Every artifact holds meaning, and every response leaves its own echo behind."*
