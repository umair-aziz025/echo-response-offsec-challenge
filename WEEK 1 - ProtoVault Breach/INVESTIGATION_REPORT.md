# ProtoVault Security Incident - Investigation Report
**Date:** October 11, 2025  
**Investigator:** MR. Umair 
**Case:** Database Leak Investigation

---

## 🎯 Executive Summary

A complete database dump of the ProtoGuard Asset Management system was leaked to a publicly accessible S3 bucket. The leak originated from an automated backup script that was committed to the application's Git repository.

---

## 📋 Challenge Answers

### 1️⃣ Database Connection String
**Question:** Review the database connection string to ensure it is secure. Submit the connection string here.

**Answer:**
```
postgresql://assetdba:8d631d2207ec1debaafd806822122250@pgsql_prod_db01.protoguard.local/pgamgt?sslmode=verify-full
```

**Location:** Found in `source_code/app/app.py` at line 10

**Security Issues:**
- ❌ Hardcoded credentials in source code
- ❌ Password stored in plaintext
- ❌ No environment variables or secrets management
- ✅ SSL mode enabled (only positive aspect)

---

### 2️⃣ Source File That Leaked the Database
**Question:** Which file may have leaked the database? Provide the file name.

**Answer:**
```
backup_db.py
```

**Full Path:** `app/util/backup_db.py`

**How It Was Found:**
1. Reviewed Git commit history
2. Found suspicious commit: "Remove backup scripts" (commit 1cc71b0)
3. Recovered deleted file using: `git show 1cc71b0^:app/util/backup_db.py`

**What This File Did:**
- Connected to PostgreSQL database via SSH
- Created a pg_dump backup
- Encoded the backup using ROT13 (weak obfuscation)
- Uploaded to public S3 bucket: `protoguard-asset-management`

---

### 3️⃣ Naomi Adler's Password Hash
**Question:** Verify the contents of the leak by submitting the password hash for Naomi Adler.

**Answer:**
```
pbkdf2:sha256:600000$YQqIvcDipYLzzXPB$598fe450e5ac019cdd41b4b10c5c21515573ee63a8f4881f7d721fd74ee43d59
```

**User Details:**
- ID: 11
- First Name: Naomi
- Last Name: Adler
- Username: naomi.adler
- Specialty: Cognitive Systems Research

---

### 4️⃣ Public Address of Database Leak
**Question:** Submit the public address of the database leak, including the name of the file.

**Answer:**
```
https://protoguard-asset-management.s3.us-east-2.amazonaws.com/db_backup.xyz
```

**File Details:**
- S3 Bucket: `protoguard-asset-management`
- Region: `us-east-2` (US East - Ohio)
- File Name: `db_backup.xyz`
- Encoding: ROT13 (easily reversible)
- Access: Publicly readable (no authentication required)

---

## 🔍 Investigation Methodology

### Step 1: Source Code Analysis
- Reviewed `app.py` and found hardcoded database credentials
- Identified Flask application with PostgreSQL backend
- No evidence of secrets management or environment variables

### Step 2: Git History Analysis
```powershell
git log --oneline --all
git show 1cc71b0 --stat
git show 1cc71b0^:app/util/backup_db.py
```
- Discovered deleted `backup_db.py` file
- File contained S3 upload logic with bucket details

### Step 3: Data Exfiltration Verification
```python
# Downloaded and decoded the leaked database
import requests, codecs
response = requests.get("https://protoguard-asset-management.s3.us-east-2.amazonaws.com/db_backup.xyz")
decoded = codecs.decode(response.text, 'rot_13')
```
- Successfully downloaded 2,400+ lines of SQL dump
- Decoded ROT13 encoding
- Verified database contents including user table

### Step 4: Evidence Collection
- Located Naomi Adler's user record (ID: 11)
- Extracted password hash (pbkdf2:sha256 with 600,000 iterations)
- Documented all table structures and sensitive data

---

## 🚨 Security Vulnerabilities Identified

### Critical Issues

1. **Hardcoded Credentials** (CRITICAL)
   - Database password stored in `app.py`
   - Accessible to anyone with repository access

2. **Public S3 Bucket** (CRITICAL)
   - Entire database dump publicly accessible
   - No authentication required
   - Contains PII and system credentials

3. **Weak Encoding** (HIGH)
   - ROT13 is not encryption
   - Trivial to decode
   - Provides no real security

4. **Git History Exposure** (HIGH)
   - Deleted files still accessible in Git history
   - Sensitive scripts not properly purged

5. **Insufficient Access Controls** (MEDIUM)
   - Backup script had broad permissions
   - No least-privilege principle applied

---

## ✅ Recommended Remediation Steps

### Immediate Actions (Within 24 Hours)

1. **Revoke Compromised Credentials**
   ```sql
   -- Reset database password
   ALTER USER assetdba WITH PASSWORD 'NEW_SECURE_PASSWORD';
   ```

2. **Remove Public S3 Access**
   ```bash
   aws s3 rm s3://protoguard-asset-management/db_backup.xyz
   aws s3api put-bucket-acl --bucket protoguard-asset-management --acl private
   ```

3. **Force Password Reset for All Users**
   - Especially Naomi Adler and other exposed accounts
   - Implement 2FA immediately

4. **Purge Sensitive Data from Git History**
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch app/util/backup_db.py" \
     --prune-empty --tag-name-filter cat -- --all
   ```

### Short-Term Actions (1-2 Weeks)

5. **Implement Secrets Management**
   - Use AWS Secrets Manager or HashiCorp Vault
   - Remove all hardcoded credentials
   - Use environment variables

6. **Encrypt Backups Properly**
   - Use AES-256 or similar strong encryption
   - Store encryption keys separately
   - Never use ROT13 for security

7. **Configure Private S3 Buckets**
   - Enable encryption at rest (SSE-S3 or SSE-KMS)
   - Use IAM roles with least privilege
   - Enable S3 bucket versioning and logging

8. **Implement Database Access Monitoring**
   - Enable PostgreSQL audit logging
   - Set up alerts for suspicious activity
   - Monitor for unauthorized access attempts

### Long-Term Actions (1-3 Months)

9. **Security Training**
   - Train developers on secure coding practices
   - Conduct Git hygiene training
   - Implement secure SDLC

10. **Regular Security Audits**
    - Quarterly code reviews
    - Automated secret scanning in CI/CD
    - Penetration testing

11. **Incident Response Plan**
    - Document escalation procedures
    - Create runbooks for common incidents
    - Conduct tabletop exercises

---

## 📊 Impact Assessment

### Data Exposed
- ✅ User accounts and password hashes (pbkdf2 - moderately secure)
- ✅ Database connection credentials
- ✅ Item inventory (biological samples, prototypes, etc.)
- ✅ Internal notes and classifications
- ✅ Geographic coordinates of assets

### Systems at Risk
- PostgreSQL production database
- Flask web application
- SSH access to database server
- S3 infrastructure

### Estimated Risk Level
**CRITICAL** - Complete database exposure with attacker claiming ransom demands

---

## 🔐 Tools Used

- **Git:** Version control forensics
- **Python:** Script development and data analysis
- **Requests:** HTTP downloads
- **Codecs:** ROT13 decoding
- **AWS CLI:** S3 verification (recommended for cleanup)

---

## 📝 Conclusion

The investigation confirmed a complete database leak through an insecure backup process. The combination of hardcoded credentials, public S3 buckets, and weak encoding created a critical security vulnerability. All recommended remediation steps should be implemented immediately to prevent further exposure.

**Status:** ✅ Investigation Complete  
**Next Steps:** Initiate immediate remediation and notify affected users

---

*Report prepared by: MR. Umair*
