# Tutorial Challenge - Security Incident Investigation Report

**Date:** October 7, 2025  
**Investigator:** MR. Umair  
**Case:** Echo Response - Week 0 Tutorial  
**Difficulty:** Easy  
**Category:** Incident Response, Log Analysis, Encoding

---

## 🎯 Executive Summary

This tutorial challenge introduces participants to the Echo Response series through two distinct exercises: decoding a Base64-encoded cybersecurity awareness message and analyzing web server logs for malicious activity. 

**Key Findings:**
- Successfully decoded Base64-encoded tutorial content containing security awareness poem
- Identified successful path traversal attack targeting SSH private keys
- Detected unauthorized access from IP address 192.168.1.101
- Confirmed exfiltration of 1,678 bytes (SSH private key for user 'dave')
- Attack succeeded with HTTP 200 status, indicating critical security breach

**Severity:** HIGH - SSH private key compromise enables unauthorized system access

---

## 📋 Investigation Objectives

1. Decode Base64-encoded content from `tutorial.txt`
2. Extract the exercise answer from decoded message
3. Analyze web server access logs for suspicious activity
4. Identify path traversal attacks and other security incidents
5. Document attack vectors, impact, and remediation steps

---

## 🔍 Evidence Collection

### Evidence Files

| File Name | Type | Size | Description |
|-----------|------|------|-------------|
| tutorial.txt | Text | ~500 bytes | Base64-encoded cybersecurity poem |
| access.log | Log File | 21 entries | Apache/Nginx web server access logs |
| question.txt | Text | ~4 KB | Answer format instructions |
| instruction.txt | Text | 58 bytes | Package password information |

### Chain of Custody

- **Collection Date:** November 17, 2025
- **Source:** OffSec Echo Response Challenge Platform
- **Package Password:** ThisIsAFunTutorial1#
- **Integrity:** SHA256 hashes verified (if applicable)

---

## 📊 Part 1: Base64 Decoding Analysis

### Encoded Content Analysis

**File:** tutorial.txt  
**Encoding:** Base64  
**Original Content:**
```
TXVmZmluIHRoZSBjYXQgY2xpY2tlZCBvbiBhIGxpbmssCk5vdyBhbGwgaGlzIGZpbGVzIGJlZ2FuIHRvIHNocmluayEKSGUgc2hvdWxk4oCZdmUgY2hlY2tlZCB0aGUgc2VuZGVy4oCZcyBuYW1lLApCdXQgbm93IGhpcyBsYXB0b3AncyBub3QgdGhlIHNhbWUuCgpBIHBhc3N3b3JkIHN0cm9uZywgYSBmaXJld2FsbCB0aWdodCwKS2VlcHMgc25lYWt5IGhhY2tlcnMgb3V0IG9mIHNpZ2h0LgpTbyB0aGluayBiZWZvcmUgeW91IHN1cmYgYW5kIHBsYXnigJQKQ3liZXItc21hcnRzIHdpbGwgc2F2ZSB0aGUgZGF5IQoKVGhlIGFuc3dlciB0byB0aGlzIGV4ZXJjaXNlIGlzICJUcnlIYXJkZXIi
```

### Decoding Process

**Method 1 - PowerShell:**
```powershell
[System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($base64String))
```

**Method 2 - Python:**
```python
import base64
decoded = base64.b64decode(encoded_string).decode('utf-8')
```

**Method 3 - Linux:**
```bash
echo "$base64String" | base64 -d
```

### Decoded Message

```
Muffin the cat clicked on a link,
Now all his files began to shrink!
He should've checked the sender's name,
But now his laptop's not the same.

A password strong, a firewall tight,
Keeps sneaky hackers out of sight.
So think before you surf and play—
Cyber-smarts will save the day!

The answer to this exercise is "TryHarder"
```

### Security Awareness Lessons

The decoded poem teaches fundamental cybersecurity principles:

1. **Phishing Awareness**
   - "Muffin clicked on a link" → Don't click suspicious links
   - "Should've checked the sender's name" → Verify email senders
   - **Impact:** Ransomware infection ("files began to shrink")

2. **Defense in Depth**
   - "A password strong, a firewall tight" → Multiple security layers
   - Strong authentication + network security
   - Principle of least privilege

3. **Security Mindfulness**
   - "Think before you surf and play" → User awareness is critical
   - "Cyber-smarts will save the day" → Education prevents breaches

### Answer Extraction

**Exercise Answer:** `TryHarder`

This aligns with the famous OffSec motto: "Try Harder" - encouraging persistence and problem-solving in cybersecurity challenges.

---

## 📊 Part 2: Access Log Analysis

### Log File Overview

- **Total Entries:** 21
- **Date Range:** October 1, 2025 (08:02:15 - 08:20:10)
- **Time Span:** ~18 minutes
- **Unique IP Addresses:** 10
- **Log Format:** Apache/Nginx Combined Log Format

### Normal Traffic Baseline

```
192.168.1.10  - Homepage access (200 OK)
192.168.1.15  - Login page access (200 OK)
192.168.1.30  - Dashboard access + static assets (200 OK)
10.0.0.5      - API calls (200 OK, 204 No Content)
192.168.1.15  - Logout (302 Redirect)
```

### Suspicious Activity Detection

#### 🚨 Critical Finding: Path Traversal Attack

**Log Entry (Line 16):**
```
192.168.1.101 - - [01/Oct/2025:08:17:55 +0000] "GET /public/plugins/welcome/../../../../../../../../home/dave/.ssh/id_rsa HTTP/1.1" 200 1678 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
```

**Attack Analysis:**

| Field | Value | Analysis |
|-------|-------|----------|
| **Source IP** | 192.168.1.101 | Internal network range (192.168.1.x) |
| **Timestamp** | 08:17:55 UTC | October 1, 2025 |
| **Method** | GET | Read-only operation |
| **Path** | `/public/plugins/welcome/../../../../../../../../home/dave/.ssh/id_rsa` | 8-level directory traversal |
| **HTTP Version** | HTTP/1.1 | Standard protocol |
| **Status Code** | 200 OK | ⚠️ **Attack Successful** |
| **Response Size** | 1,678 bytes | SSH private key size |
| **User Agent** | Mozilla/5.0 (Windows NT 10.0) | Legitimate browser UA |
| **Referrer** | - (None) | Direct URL access |

**Attack Breakdown:**

1. **Legitimate Base Path:** `/public/plugins/welcome/`
   - Appears to be a valid application endpoint
   - Likely intended for plugin management

2. **Directory Traversal:** `../../../../../../../../`
   - 8 levels of parent directory navigation
   - Each `../` moves up one directory level
   - Breaks out of web root directory

3. **Target Path:** `/home/dave/.ssh/id_rsa`
   - User: `dave`
   - File: SSH private key (RSA)
   - Location: Standard Linux SSH key location

4. **Success Indicators:**
   - HTTP 200 OK status
   - 1,678 bytes returned (typical RSA key size)
   - No error message or redirect

**Vulnerability:** CWE-22 - Improper Limitation of a Pathname to a Restricted Directory

**MITRE ATT&CK Mapping:**
- **Tactic:** T1083 - File and Directory Discovery
- **Tactic:** T1552.004 - Unsecured Credentials: Private Keys
- **Technique:** Path Traversal for credential access

### Authentication-Related Events

#### Failed Authentication Attempt

**Log Entry (Line 3):**
```
192.168.1.20 - - [01/Oct/2025:08:04:32 +0000] "POST /api/auth HTTP/1.1" 401 543 "-" "Mozilla/5.0 (X11; Linux x86_64)"
```

**Analysis:**
- **IP:** 192.168.1.20
- **Status:** 401 Unauthorized
- **Size:** 543 bytes (error response)
- **User Agent:** Linux Chrome browser

#### Successful Authentication

**Log Entry (Line 4):**
```
192.168.1.20 - - [01/Oct/2025:08:04:40 +0000] "POST /api/auth HTTP/1.1" 200 1023 "-" "Mozilla/5.0 (X11; Linux x86_64)"
```

**Analysis:**
- Same IP address (192.168.1.20)
- **8 seconds later** - Successful login
- **Status:** 200 OK
- **Size:** 1,023 bytes (likely includes auth token)

**Assessment:** Likely legitimate user who mistyped password initially. Time gap (8 seconds) suggests manual retry, not brute force automation.

### Error Responses

#### 1. Forbidden Access to Metrics Endpoint

**Log Entry (Line 13):**
```
172.16.0.2 - - [01/Oct/2025:08:15:33 +0000] "GET /metrics HTTP/1.1" 403 350 "-" "curl/7.68.0"
```

**Analysis:**
- **IP:** 172.16.0.2 (different subnet - 172.16.x.x)
- **Endpoint:** `/metrics` (monitoring/observability)
- **Status:** 403 Forbidden (access denied)
- **User Agent:** curl (command-line tool)
- **Assessment:** Proper security control - metrics endpoint protected

#### 2. Internal Server Error on Upload

**Log Entry (Line 14):**
```
172.16.0.2 - - [01/Oct/2025:08:16:45 +0000] "POST /api/upload HTTP/1.1" 500 1024 "-" "PostmanRuntime/7.32.0"
```

**Analysis:**
- **Same IP:** 172.16.0.2
- **Endpoint:** `/api/upload`
- **Status:** 500 Internal Server Error
- **User Agent:** Postman (API testing tool)
- **Assessment:** Application error, not security issue (likely development/testing)

#### 3. Missing Favicon

**Log Entry (Line 10):**
```
192.168.1.99 - - [01/Oct/2025:08:11:57 +0000] "GET /favicon.ico HTTP/1.1" 404 490 "-" "Mozilla/5.0 (Windows NT 10.0)"
```

**Analysis:**
- **Status:** 404 Not Found
- **Assessment:** Cosmetic issue, no security impact

---

## 🎯 Timeline of Events

```
08:02:15 - Normal activity begins (homepage access)
08:03:05 - User accesses login page
08:04:32 - Failed authentication attempt (192.168.1.20)
08:04:40 - Successful authentication (192.168.1.20) 
08:06:12 - Dashboard access with static assets
08:10:01 - API data retrieval (10.0.0.5)
08:11:57 - Favicon 404 error
08:12:00 - Apache internal health check
08:13:22 - User logout
08:15:33 - Forbidden metrics access attempt (172.16.0.2)
08:16:45 - Upload API error (172.16.0.2)
08:17:17 - Logo image request
08:17:55 - 🚨 PATH TRAVERSAL ATTACK (192.168.1.101) 🚨
08:18:01 - Request timeout (408)
08:18:05 - User profile access
08:19:30 - Terms of service page
08:19:44 - User notifications API
08:20:10 - User settings API
```

**Critical Incident:** 08:17:55 UTC - SSH private key exfiltration

---

## 🔬 Impact Assessment

### Confidentiality Impact: **HIGH**

- ✅ **Compromised:** SSH private key for user 'dave'
- ⚠️ **Risk:** Unauthorized SSH access to systems where this key is authorized
- 🚨 **Scope:** All servers/systems trusting dave's public key

### Integrity Impact: **MEDIUM**

- If attacker gains SSH access, they can:
  - Modify files and configurations
  - Plant backdoors
  - Tamper with logs (anti-forensics)
  - Escalate privileges

### Availability Impact: **MEDIUM**

- Potential for:
  - Ransomware deployment
  - Resource exhaustion
  - Service disruption
  - Data destruction

### Overall Risk Rating: **CRITICAL**

**Reasoning:**
1. Attack was **successful** (200 OK response)
2. SSH keys enable **persistent access**
3. No user interaction required for exploitation
4. Lateral movement opportunities
5. Difficult to detect post-compromise activity

---

## 🛡️ Root Cause Analysis

### Vulnerability Details

**Type:** Path Traversal (Directory Traversal)  
**CWE:** CWE-22 - Improper Limitation of a Pathname to a Restricted Directory  
**OWASP:** A01:2021 - Broken Access Control

### Why the Attack Succeeded

1. **Insufficient Input Validation**
   - Application didn't sanitize `../` sequences
   - No restriction on parent directory references
   - Path normalization not implemented

2. **Missing Access Controls**
   - No chroot jail or filesystem restrictions
   - Web server process has excessive file read permissions
   - No allow-list for accessible directories

3. **Lack of Detection**
   - No WAF (Web Application Firewall) deployed
   - No intrusion detection for path traversal patterns
   - Logging exists but no real-time alerting

### Vulnerable Code Pattern (Hypothetical)

```python
# VULNERABLE CODE (Example)
@app.route('/public/plugins/<path:plugin_path>')
def serve_plugin(plugin_path):
    # NO SANITIZATION - DANGEROUS!
    file_path = f'/var/www/public/plugins/{plugin_path}'
    return send_file(file_path)
```

**Problem:** Direct concatenation of user input into file path without validation.

---

## 🚨 Remediation Steps

### Immediate Actions (0-24 Hours)

1. **Incident Response**
   ```bash
   # Block malicious IP immediately
   sudo iptables -A INPUT -s 192.168.1.101 -j DROP
   
   # Check for unauthorized SSH sessions
   sudo last -f /var/log/wtmp | grep dave
   sudo journalctl -u ssh | grep 192.168.1.101
   ```

2. **Credential Rotation**
   ```bash
   # Revoke compromised SSH key for user 'dave'
   sudo su - dave
   cd ~/.ssh
   mv id_rsa id_rsa.COMPROMISED_$(date +%Y%m%d)
   mv id_rsa.pub id_rsa.pub.COMPROMISED_$(date +%Y%m%d)
   
   # Generate new key pair
   ssh-keygen -t ed25519 -C "dave@company.com"
   
   # Update authorized_keys on all servers
   # Deploy new public key to authorized systems
   ```

3. **Forensic Evidence Collection**
   ```bash
   # Preserve logs before they rotate
   sudo cp /var/log/apache2/access.log /evidence/access.log.$(date +%Y%m%d_%H%M%S)
   sudo cp /var/log/auth.log /evidence/auth.log.$(date +%Y%m%d_%H%M%S)
   
   # Check for signs of key usage
   sudo grep "192.168.1.101" /var/log/auth.log
   ```

4. **System Audit**
   ```bash
   # Check for other compromised files accessed by this IP
   sudo grep "192.168.1.101" /var/log/apache2/access.log
   
   # Look for suspicious processes
   sudo ps auxf | grep dave
   
   # Check for backdoors
   sudo find /tmp -type f -mtime -1
   sudo find /home/dave -type f -mtime -1
   ```

### Short-Term Fixes (24-72 Hours)

1. **Patch Vulnerability**
   ```python
   # SECURE CODE (Example)
   import os
   from werkzeug.security import safe_join
   
   @app.route('/public/plugins/<path:plugin_path>')
   def serve_plugin(plugin_path):
       # Validate and sanitize input
       if '..' in plugin_path or plugin_path.startswith('/'):
           abort(403)
       
       # Use safe_join to prevent directory traversal
       base_dir = '/var/www/public/plugins'
       file_path = safe_join(base_dir, plugin_path)
       
       # Verify the file is within allowed directory
       if not file_path.startswith(base_dir):
           abort(403)
       
       return send_file(file_path)
   ```

2. **Deploy WAF Rules**
   ```nginx
   # Nginx: Block path traversal attempts
   location ~ \.\. {
       deny all;
       return 403;
   }
   
   location ~ /\.ssh/ {
       deny all;
       return 403;
   }
   ```

3. **Implement Monitoring**
   ```bash
   # Set up alert for path traversal patterns
   # Example: Fail2ban filter
   [Definition]
   failregex = ^<HOST>.*"GET.*\.\..*"
   ignoreregex =
   ```

### Long-Term Security Enhancements

1. **Security Controls**
   - Deploy Web Application Firewall (ModSecurity, CloudFlare WAF)
   - Implement Content Security Policy (CSP) headers
   - Use principle of least privilege for web server process
   - Enable chroot jail for web application

2. **Code Security**
   - Conduct secure code review
   - Implement input validation library
   - Use parameterized file access functions
   - Enable static application security testing (SAST)

3. **Monitoring & Detection**
   - Deploy SIEM solution (Splunk, ELK Stack, Wazuh)
   - Create alerts for:
     - Multiple `../` in URLs
     - Access to sensitive file paths
     - Unusual response sizes (e.g., 1678 bytes from static endpoint)
   - Implement file integrity monitoring (AIDE, Tripwire)

4. **Access Controls**
   - Implement role-based access control (RBAC)
   - Use allow-lists for file access
   - Restrict web server filesystem permissions
   - Enable SELinux/AppArmor policies

5. **Security Training**
   - Developer training on secure coding practices
   - Security awareness for operations team
   - Incident response drills
   - Regular vulnerability assessments

---

## 📈 Indicators of Compromise (IOCs)

### Network Indicators

| Indicator Type | Value | Severity | Context |
|----------------|-------|----------|---------|
| IP Address | 192.168.1.101 | CRITICAL | Path traversal attack source |
| User Agent | Mozilla/5.0 (Windows NT 10.0; Win64; x64) | INFO | Common browser UA (may be spoofed) |

### File System Indicators

| Indicator | Location | Description |
|-----------|----------|-------------|
| Accessed File | /home/dave/.ssh/id_rsa | SSH private key exfiltrated |
| Web Log | /var/log/apache2/access.log | Contains attack evidence |

### Behavioral Indicators

- GET request with multiple `../` sequences
- Access to files outside web root
- 1,678 byte response from plugin endpoint (unusual)
- Direct URL access (no referrer header)

---

## 🎓 Lessons Learned

### What Went Right ✅

1. **Logging Enabled:** Attack was captured in access logs
2. **Authentication Controls:** 401/403 responses show some access controls exist
3. **Error Handling:** 500 errors logged for troubleshooting

### What Went Wrong ❌

1. **Input Validation:** No sanitization of file paths
2. **Access Controls:** Insufficient filesystem restrictions
3. **Monitoring:** No real-time alerting for attacks
4. **Incident Response:** Delayed detection (tutorial exercise, but critical in production)

### Recommendations for Future

1. **Security-First Development**
   - Security requirements in design phase
   - Threat modeling for new features
   - Secure coding standards enforcement

2. **Defense in Depth**
   - Multiple layers of security controls
   - Assume one layer will fail
   - Redundant monitoring and detection

3. **Continuous Improvement**
   - Regular security assessments
   - Penetration testing
   - Bug bounty program
   - Post-incident reviews

---

## 📝 Investigation Conclusions

### Summary of Findings

1. ✅ **Tutorial Decoded:** Base64 poem successfully decoded, answer "TryHarder" extracted
2. 🚨 **Critical Vulnerability:** Path traversal vulnerability identified and confirmed
3. 🔴 **Successful Attack:** SSH private key for user 'dave' exfiltrated by 192.168.1.101
4. ⚠️ **Additional Issues:** Minor authentication failures and server errors detected
5. 📊 **Impact:** HIGH - Potential for unauthorized SSH access and lateral movement

### Recommendations Summary

| Priority | Action | Timeline |
|----------|--------|----------|
| 🔴 CRITICAL | Revoke compromised SSH key | Immediate |
| 🔴 CRITICAL | Block malicious IP (192.168.1.101) | Immediate |
| 🟠 HIGH | Patch path traversal vulnerability | 24 hours |
| 🟠 HIGH | Deploy WAF with path traversal rules | 72 hours |
| 🟡 MEDIUM | Implement real-time log monitoring | 1 week |
| 🟢 LOW | Security awareness training | 1 month |

### Case Status

**Status:** ✅ INVESTIGATION COMPLETE  
**Severity:** CRITICAL (High Confidentiality Impact)  
**Remediation:** IN PROGRESS (Requires immediate credential rotation)  
**Follow-up:** Security audit recommended within 30 days

---

## 📚 References

### CVE & Vulnerability Databases

- **CWE-22:** Improper Limitation of a Pathname to a Restricted Directory  
  https://cwe.mitre.org/data/definitions/22.html

- **OWASP A01:2021:** Broken Access Control  
  https://owasp.org/Top10/A01_2021-Broken_Access_Control/

### MITRE ATT&CK Framework

- **T1083:** File and Directory Discovery  
  https://attack.mitre.org/techniques/T1083/

- **T1552.004:** Unsecured Credentials: Private Keys  
  https://attack.mitre.org/techniques/T1552/004/

### Security Best Practices

- OWASP Path Traversal Prevention Cheat Sheet
- NIST SP 800-53: Security and Privacy Controls
- CIS Benchmarks for Web Application Security

---

## 📎 Appendices

### Appendix A: Full Access Log (21 Entries)

<details>
<summary>Click to expand complete access.log</summary>

```
192.168.1.10 - - [01/Oct/2025:08:02:15 +0000] "GET / HTTP/1.1" 200 4523 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0"
192.168.1.15 - - [01/Oct/2025:08:03:05 +0000] "GET /login HTTP/1.1" 200 1321 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
192.168.1.20 - - [01/Oct/2025:08:04:32 +0000] "POST /api/auth HTTP/1.1" 401 543 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
192.168.1.20 - - [01/Oct/2025:08:04:40 +0000] "POST /api/auth HTTP/1.1" 200 1023 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
[... remaining 17 entries ...]
192.168.1.101 - - [01/Oct/2025:08:17:55 +0000] "GET /public/plugins/welcome/../../../../../../../../home/dave/.ssh/id_rsa HTTP/1.1" 200 1678 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
```

</details>

### Appendix B: Decoding Methods

**PowerShell:**
```powershell
[System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("TXVmZmluIH..."))
```

**Python:**
```python
import base64
base64.b64decode("TXVmZmluIH...").decode('utf-8')
```

**Bash:**
```bash
echo "TXVmZmluIH..." | base64 -d
```

### Appendix C: Analysis Script

See `analyze_tutorial.py` for automated forensic analysis tool.

---

**Report Prepared By:** MR. Umair  
**Date:** October 7, 2025  

---

*End of Investigation Report*
