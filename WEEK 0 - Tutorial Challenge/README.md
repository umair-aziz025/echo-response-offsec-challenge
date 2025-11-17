# WEEK 0 - Tutorial Challenge 📚

**Status:** ✅ COMPLETED  
**Category:** Incident Response, Log Analysis, Encoding  
**Difficulty:** Easy

---

## 📖 Challenge Overview

This is the introductory tutorial challenge from the **Echo Response** series, designed to familiarize participants with the question-answering format and basic security concepts. The challenge tests fundamental skills in Base64 decoding, log analysis, and identifying common web vulnerabilities.

### 🎯 Learning Objectives

- Understanding the Echo Response answer submission format
- Base64 encoding/decoding techniques
- Web server log analysis
- Path traversal attack detection
- Security awareness fundamentals

---

## 📋 Challenge Scenario

> *"Muffin the cat clicked on a link..."*

This tutorial provides both a cybersecurity awareness message in the form of a fun poem and a practical exercise in analyzing web server access logs for suspicious activity. Participants learn how to:

1. Decode Base64-encoded content
2. Identify security incidents from log files
3. Submit answers in various accepted formats

---

## 🔍 Challenge Files

| File | Description |
|------|-------------|
| `tutorial.txt` | Base64-encoded cybersecurity awareness poem |
| `access.log` | Apache/Nginx-style access logs containing suspicious activity |
| `question.txt` | Detailed instructions on answer submission formats |
| `instruction.txt` | Password for the challenge package |

**Package Password:** `ThisIsAFunTutorial1#`

---

## ❓ Challenge Questions & Answers

### Question 1: Tutorial Message

**Task:** Decode the Base64-encoded content in `tutorial.txt` and extract the exercise answer.

**Encoded Content:**
```
TXVmZmluIHRoZSBjYXQgY2xpY2tlZCBvbiBhIGxpbmssCk5vdyBhbGwgaGlzIGZpbGVzIGJlZ2FuIHRvIHNocmluayEKSGUgc2hvdWxk4oCZdmUgY2hlY2tlZCB0aGUgc2VuZGVy4oCZcyBuYW1lLApCdXQgbm93IGhpcyBsYXB0b3AncyBub3QgdGhlIHNhbWUuCgpBIHBhc3N3b3JkIHN0cm9uZywgYSBmaXJld2FsbCB0aWdodCwKS2VlcHMgc25lYWt5IGhhY2tlcnMgb3V0IG9mIHNpZ2h0LgpTbyB0aGluayBiZWZvcmUgeW91IHN1cmYgYW5kIHBsYXnigJQKQ3liZXItc21hcnRzIHdpbGwgc2F2ZSB0aGUgZGF5IQoKVGhlIGFuc3dlciB0byB0aGlzIGV4ZXJjaXNlIGlzICJUcnlIYXJkZXIi
```

**Decoded Message:**
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

**Answer:**
```
TryHarder
```

---

### Question 2: Log Analysis - Path Traversal Attack

**Task:** Analyze the `access.log` file and identify the path traversal attack. Provide the source IP address, malicious request path, and target file.

**Answer:**

**Source IP Address:**
```
192.168.1.101
```

**Malicious Request:**
```
GET /public/plugins/welcome/../../../../../../../../home/dave/.ssh/id_rsa HTTP/1.1
```

**Target File:**
```
/home/dave/.ssh/id_rsa
```

**Attack Details:**
- **Timestamp:** 01/Oct/2025:08:17:55 +0000
- **HTTP Method:** GET
- **Status Code:** 200 (Successful - Attack succeeded!)
- **Response Size:** 1,678 bytes
- **User Agent:** Mozilla/5.0 (Windows NT 10.0; Win64; x64)
- **Directory Traversal Depth:** 8 levels (../../../../../../../../)

---

### Question 3: Additional Suspicious Activities

**Task:** Identify other suspicious activities in the access logs.

**Answer:**

**Authentication Failure:**
- **IP:** 192.168.1.20
- **Request:** POST /api/auth
- **Status:** 401 Unauthorized
- **Timestamp:** 01/Oct/2025:08:04:32 +0000
- **Note:** Followed by successful authentication attempt 8 seconds later

**Server Errors:**
1. **Upload Failure:**
   - **IP:** 172.16.0.2
   - **Request:** POST /api/upload
   - **Status:** 500 Internal Server Error
   - **User Agent:** PostmanRuntime/7.32.0

2. **Forbidden Access:**
   - **IP:** 172.16.0.2
   - **Request:** GET /metrics
   - **Status:** 403 Forbidden
   - **User Agent:** curl/7.68.0

**Missing Resource:**
- **IP:** 192.168.1.99
- **Request:** GET /favicon.ico
- **Status:** 404 Not Found

---

## 🔬 Technical Analysis

### Base64 Decoding Method

**PowerShell:**
```powershell
[System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("TXVmZmluIH..."))
```

**Python:**
```python
import base64
decoded = base64.b64decode("TXVmZmluIH...").decode('utf-8')
print(decoded)
```

**Linux/Bash:**
```bash
echo "TXVmZmluIH..." | base64 -d
```

### Path Traversal Attack Analysis

The attack exploits insufficient path validation in the web application:

```
/public/plugins/welcome/../../../../../../../../home/dave/.ssh/id_rsa
```

**Attack Chain:**
1. Start at the legitimate path: `/public/plugins/welcome/`
2. Traverse up 8 directory levels using `../`
3. Navigate to the target: `/home/dave/.ssh/id_rsa`
4. Successfully retrieve SSH private key (1,678 bytes returned)

**Vulnerability Type:** CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')

---

## 🛡️ Security Lessons Learned

### From the Poem

1. **Phishing Awareness:** Always verify sender information before clicking links
2. **Strong Authentication:** Use strong passwords and multi-factor authentication
3. **Firewall Protection:** Implement network security controls
4. **Security Mindfulness:** Think before interacting with untrusted content

### From Log Analysis

1. **Path Traversal Prevention:**
   - Validate and sanitize all user input
   - Implement proper access controls
   - Use allow-lists for file access
   - Never trust client-supplied paths

2. **Monitoring & Detection:**
   - Implement real-time log monitoring
   - Set up alerts for suspicious patterns (e.g., `../` in URLs)
   - Track failed authentication attempts
   - Monitor error rates and anomalies

3. **Incident Response:**
   - The 200 status code indicates successful data exfiltration
   - SSH private key compromise = immediate credential rotation required
   - IP 192.168.1.101 should be blocked and investigated
   - All SSH keys for user 'dave' must be regenerated

---

## 🚨 Recommendations

### Immediate Actions

1. **Revoke Compromised Credentials:**
   - Regenerate all SSH keys for user 'dave'
   - Rotate any passwords for affected accounts
   - Audit access logs for unauthorized access attempts

2. **Block Malicious IP:**
   - Add 192.168.1.101 to firewall blocklist
   - Investigate source and motivation of attack
   - Check for other attacks from same IP range

3. **Patch Vulnerability:**
   - Implement path traversal protection
   - Update web application framework
   - Add input validation and sanitization

### Long-Term Improvements

1. **Security Controls:**
   - Deploy Web Application Firewall (WAF)
   - Implement file access restrictions
   - Use principle of least privilege
   - Enable security headers (X-Content-Type-Options, etc.)

2. **Monitoring:**
   - Set up SIEM for centralized log analysis
   - Configure alerts for path traversal patterns
   - Monitor for unusual file access attempts
   - Track authentication failures

3. **Training:**
   - Security awareness training for all users
   - Phishing simulation exercises
   - Secure coding practices for developers
   - Incident response drills

---

## 📊 Attack Timeline

| Time | Event | IP Address | Status |
|------|-------|------------|--------|
| 08:02:15 | Normal homepage access | 192.168.1.10 | ✅ 200 OK |
| 08:04:32 | Failed authentication | 192.168.1.20 | ❌ 401 Unauthorized |
| 08:04:40 | Successful authentication | 192.168.1.20 | ✅ 200 OK |
| 08:15:33 | Forbidden metrics access | 172.16.0.2 | ⚠️ 403 Forbidden |
| 08:16:45 | Upload error | 172.16.0.2 | ❌ 500 Error |
| 08:17:55 | **Path traversal attack** | 192.168.1.101 | 🚨 200 OK (Success) |

---

## 🛠️ Solution Scripts

### Automated Analysis

Run the provided Python script to automatically analyze all challenge components:

```bash
python analyze_tutorial.py
```

**Script Features:**
- Base64 decoding with answer extraction
- Access log parsing and analysis
- Path traversal attack detection
- Suspicious activity identification
- Security summary report generation

**Sample Output:**
```
==================================================================================
 ECHO RESPONSE - WEEK 0: TUTORIAL CHALLENGE ANALYSIS
 Difficulty: Easy
 Category: Incident Response, Log Analysis, Encoding
==================================================================================

TUTORIAL MESSAGE DECODED
==================================================================================
Muffin the cat clicked on a link...
[Full decoded poem]
==================================================================================

✅ Exercise Answer: TryHarder

==================================================================================
ACCESS LOG ANALYSIS
==================================================================================

📊 Total log entries analyzed: 21

🚨 PATH TRAVERSAL ATTACKS DETECTED: 1
  Source IP: 192.168.1.101
  Target File: /home/dave/.ssh/id_rsa
  Status: 200 OK (Attack Successful)
  Size: 1678 bytes
```

---

## 📝 Answer Submission Formats

As explained in `question.txt`, the Echo Response grading system accepts multiple answer formats:

### Accepted Formats

**Single Answer:**
```
TryHarder
```

**IP Address (Multiple):**
```
192.168.1.101
```
or
```
- 192.168.1.101
- 192.168.1.20
- 172.16.0.2
```

**Text Format:**
```
The answer is TryHarder
```

**List Format with Details:**
```
- Source IP: 192.168.1.101
- Target: /home/dave/.ssh/id_rsa
- Status: Successful (200)
```

### Important Notes

- ✅ All required components must be included
- ❌ Extra or incorrect information will be marked wrong
- ❌ Duplicate entries will be marked wrong
- ✅ Order and formatting style don't matter (as long as complete)

---

## 📚 Files in This Repository

```
WEEK 0 - Tutorial Challenge/
├── README.md                    # This file - Complete challenge writeup
├── INVESTIGATION_REPORT.md      # Detailed forensic analysis report
├── analyze_tutorial.py          # Automated analysis script
├── access.log                   # Web server access logs
└── tutorial.txt                 # Base64-encoded challenge message
```

---

## 🎓 Skills Demonstrated

- ✅ Base64 encoding/decoding
- ✅ Web server log analysis
- ✅ Path traversal vulnerability identification
- ✅ Security incident investigation
- ✅ Python scripting for automation
- ✅ Regular expression pattern matching
- ✅ Security awareness and best practices
- ✅ Technical documentation and reporting

---

## 🔗 Related Challenges

This tutorial challenge serves as an introduction to the Echo Response series:

- **WEEK 1 - ProtoVault Breach:** Git forensics and AWS security
- **WEEK 2 - Stealer's Shadow:** Advanced malware analysis
- **WEEK 3 - Quantum Conundrum:** Reverse engineering and cryptanalysis
- **WEEK 4 - Echo Trail:** Cloud security and Azure investigation
- **WEEK 5 - Emerald Anomaly:** Supply chain attack analysis
- **WEEK 6 - Nullform Vault:** UPX-packed malware reverse engineering

---

## 🏆 Completion Status

- ✅ Base64 message decoded
- ✅ Tutorial answer extracted: "TryHarder"
- ✅ Path traversal attack identified
- ✅ Malicious IP identified: 192.168.1.101
- ✅ Target file identified: /home/dave/.ssh/id_rsa
- ✅ Additional security incidents documented
- ✅ Analysis script created
- ✅ Remediation recommendations provided

---

**Challenge Completed:** November 17, 2025  
**Investigator:** Umair Aziz  
**Repository:** [echo-response-offsec-challenge](https://github.com/umair-aziz025/echo-response-offsec-challenge)

---

*"Try Harder - The OffSec Motto"* 💪
