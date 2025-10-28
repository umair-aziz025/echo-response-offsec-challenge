# Echo Trail - Security Incident Investigation Report
**Date:** October 28, 2025  
**Investigator:** MR. Umair  
**Case:** NGO-Hub Breach - Empathreach Infiltration  
**Target:** Empathreach (NGO-Hub)  
**Compromised System:** DB Server, Cloud Infrastructure  
**Compromised User:** elena.nygaard@ngohubcloud.onmicrosoft.com

---

## 🎯 Executive Summary

Empathreach, home of NGO-Hub (a vast humanitarian nexus connecting relief efforts across high-risk zones), suffered a sophisticated multi-stage cyber attack. The adversary successfully compromised user credentials through phishing, bypassed MFA protections, gained access to Azure Cloud Shell, laterally moved to the database server, and exfiltrated sensitive donor records.

**Attack Severity:** 🔴 CRITICAL

**Key Findings:**
- ✅ Complete attack chain reconstructed from initial phishing to data exfiltration
- ✅ Phishing infrastructure identified with typosquatting domain
- ✅ Azure MFA bypass technique documented
- ✅ Lateral movement via Azure Arc SSH connection mapped
- ✅ Database exfiltration via mysqldump utility confirmed
- ✅ All 10 investigation objectives achieved

**Strategic Context:**
The adversary now seeks the **Nullform Key**, the third and final Primal Key. Deep within Empathreach's layered systems lies an ancient artifact containing metadata—a locator for the Nullform Key. This breach represents a critical threat to the balance of the Cyber Realms.

---

## 📋 Detailed Investigation Findings

### 1️⃣ Initial Compromise Vector - Phishing Email

**Question:** Which file was attached to the phishing email that started the compromise?

#### Answer:
```
Filename: ngo_update.png
```

#### Evidence:
The phishing campaign targeted NGO-Hub staff with emails disguised as security verification requests. Analysis of the `.eml` files in the evidence package revealed:

**Email Details:**
- **Subject:** "Security Verification | Action Required"
- **Sender:** Spoofed to appear legitimate
- **Attachment:** `ngo_update.png` - A malicious image file likely containing embedded malicious content or serving as a lure
- **Technique:** Social engineering exploiting trust in organizational security communications

#### Impact Assessment:
- 🔴 **HIGH:** Successful credential harvesting
- 🔴 **HIGH:** Initial access vector for entire attack chain
- 🟡 **MEDIUM:** User training gap identified

---

### 2️⃣ Phishing Infrastructure - Malicious URL

**Question:** What was the entire URL associated with the phishing page?

#### Answer:
```
http://login.mcrosoft.com/login.html
```

#### Analysis:

**Typosquatting Technique:**
- **Legitimate:** microsoft.com
- **Malicious:** mcrosoft.com (missing 'i')
- **Attack Type:** Homograph/typosquatting domain
- **Protocol:** HTTP (unencrypted - red flag)

**Phishing Page Characteristics:**
- Mimicked legitimate Microsoft/Azure login portal
- Captured credentials in plaintext
- No SSL/TLS encryption
- Hosted on attacker-controlled infrastructure

**Network Evidence:**
Packet capture (`network_capture.pcapng`) shows HTTP traffic to this domain during the incident timeframe.

#### Security Implications:
- Users failed to notice typosquatting
- HTTP vs HTTPS not verified by victim
- Browser security warnings potentially ignored

---

### 3️⃣ Credential Interception Mechanism

**Question:** What is likely the PHP attacker file name responsible for intercepting the credentials?

#### Answer:
```
login.php
```

#### Technical Analysis:

**Server-Side Component:**
- **File:** login.php
- **Function:** Credential harvesting backend
- **Method:** POST request handler
- **Actions:**
  1. Receives username/password from fake login form
  2. Logs credentials to attacker database/file
  3. Potentially redirects victim to legitimate site (to avoid suspicion)

**How It Was Identified:**
- Standard naming convention for credential phishing sites
- Typical PHP backend for form processing
- Matches attack pattern from email analysis

---

### 4️⃣ Compromised Credentials

**Question:** What is the valid Azure password obtained through phishing?

#### Answer:
```
Jopa373424
```

**Full Password Format (as provided):**
```
q4 - Jopa373424
```

#### Compromised Account Details:
- **Username:** elena.nygaard@ngohubcloud.onmicrosoft.com
- **Display Name:** Elena Nygaard
- **User ID:** e07a00dd-6d0e-4f9a-b493-7999c5a33864
- **Account Type:** Azure AD Member
- **Tenant:** ngohubcloud.onmicrosoft.com

#### Password Security Analysis:
- ✅ Reasonable length (10 characters)
- ✅ Contains uppercase and numbers
- ❌ No special characters
- ❌ Potentially dictionary-based (Jopa)
- 🔴 **CRITICAL:** Password compromised via phishing

---

### 5️⃣ Mail Server Analysis - SMTP EHLO

**Question:** What hostname did the attacker present in EHLO?

#### Answer:
```
attacker01
```

#### SMTP Protocol Analysis:

**Evidence Source:** `hmailserver_2025-08-15.log`

**SMTP EHLO Command:**
The EHLO (Extended Hello) command in SMTP is used by the sending server to identify itself. The attacker's mail server presented the hostname `attacker01` during the SMTP handshake.

**Significance:**
- Reveals attacker infrastructure naming convention
- Poor operational security (OpSec) - obvious attacker hostname
- Indicates dedicated phishing infrastructure
- Suggests multiple attacker systems (01 implies others exist)

**Mail Server Details:**
- **Protocol:** SMTP
- **Date:** 2025-08-15
- **Direction:** Inbound phishing emails to NGO-Hub
- **Sender Hostname:** attacker01

---

### 6️⃣ MFA Failure Analysis

**Question:** What failure specific message is provided in Azure when MFA is not succeeding?

#### Answer:
```
Authentication failed during strong authentication request.
```

#### Azure MFA Analysis:

**Evidence Source:** `InteractiveSignIns_2025-08-14_2025-08-15.xlsx`

**MFA Failure Timeline:**
Multiple MFA authentication failures observed before successful login:
- `2025-08-15T08:05:09Z` - Authentication failed during strong authentication request
- `2025-08-15T08:05:12Z` - Authentication failed during strong authentication request
- `2025-08-15T08:06:12Z` - Authentication failed during strong authentication request
- `2025-08-15T08:06:43Z` - Authentication failed during strong authentication request
- `2025-08-15T08:06:48Z` - Authentication failed during strong authentication request
- `2025-08-15T08:07:08Z` - Authentication failed during strong authentication request

**Other Related Messages:**
- "Strong Authentication is required" (Error Code: 50074)
- "This occurred due to 'Keep me signed in' interrupt" (Error Code: 50140)

**Attack Pattern:**
The attacker attempted multiple MFA challenges before successfully bypassing or satisfying the requirement, suggesting:
1. MFA fatigue attack
2. Social engineering to obtain MFA code
3. Compromised MFA method (SMS/authenticator)
4. Session token theft

---

### 7️⃣ Successful Authentication Timestamp

**Question:** At what specific timestamp the attacker succeeded in logging in with the victim account? Format the answer as HH:MM:SS

#### Answer:
```
08:15:49
```

**Full Timestamp:** `2025-08-15T08:15:49Z`

#### Login Success Details:

**Evidence Source:** Azure Interactive Sign-ins Log

**Successful Login Event:**
- **Timestamp:** 2025-08-15T08:15:49Z (UTC)
- **User:** elena.nygaard@ngohubcloud.onmicrosoft.com
- **IP Address:** 203.0.113.10 (Attacker IP)
- **Location:** N/A
- **User Agent:** Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
- **Application:** Azure Portal
- **Resource:** Azure Resource Manager
- **Status:** Success
- **MFA Result:** MFA requirement satisfied by claim in the token
- **Authentication Type:** Multifactor authentication

**Attack Timeline:**
1. **08:02:59 - 08:07:08** → Multiple MFA failures
2. **08:08:31** → "Keep me signed in" interrupt
3. **08:15:49** → ✅ **SUCCESSFUL LOGIN**
4. **08:16:09 - 08:16:31** → Subsequent successful authenticated requests
5. **08:48:26** → Cloud Shell session initiated

**Time to Breach:** Approximately 13 minutes from first attempt to successful login

---

### 8️⃣ Azure Cloud Shell - Lateral Movement

**Question:** Which Azure CLI subcommand initiated the server connection from Cloud Shell?

#### Answer:
```
ssh arc
```

**Full Command:**
```bash
az ssh arc --subscription 65f29041-a905-45dd-aebd-6fbf877ed89e --resource-group ngo1 --name db --local-user enygaard
```

#### Evidence Analysis:

**Source:** `cloudshell_session.log`

**Session Start:** `2025-08-15 08:48:26+00:00`

**Command Breakdown:**
- **Tool:** Azure CLI (`az`)
- **Subcommand:** `ssh arc`
- **Target:** Azure Arc-enabled server
- **Subscription ID:** 65f29041-a905-45dd-aebd-6fbf877ed89e
- **Resource Group:** ngo1
- **Server Name:** db
- **Local User:** enygaard

#### Azure Arc SSH Details:

**What is Azure Arc SSH?**
Azure Arc SSH (`az ssh arc`) enables secure SSH connections to Azure Arc-enabled servers through Azure without requiring direct network connectivity or public IP addresses.

**Attack Significance:**
- Lateral movement from Azure Cloud Shell to on-premises database server
- Leveraged legitimate Azure Arc infrastructure
- Used compromised user context for authentication
- Target: Database server containing sensitive donor information

**Target System:**
- **Hostname:** DB
- **Domain:** ngo-hub.com
- **FQDN:** DB.ngo-hub.com
- **IP Address:** 192.168.50.109
- **OS:** Microsoft Windows Server (Version 10.0.20348.4052)
- **Database:** MySQL/MariaDB (Port 3306)

---

### 9️⃣ Data Exfiltration - Target Table

**Question:** From which table were records extracted?

#### Answer:
```
donorrecords
```

#### Database Exfiltration Analysis:

**Evidence Source:** `db_dump.sql`

**SQL Dump Contents:**
The database dump file contains SQL statements to recreate and populate the `donorrecords` table.

**Table Structure:**
```sql
CREATE TABLE donorrecords (
    id INT PRIMARY KEY,
    donor_name VARCHAR(255),
    email VARCHAR(255),
    donation_amount DECIMAL(10,2),
    donation_date DATE,
    campaign VARCHAR(255),
    -- Additional sensitive fields
);
```

**Data Sensitivity:**
- 🔴 **CRITICAL:** Personally Identifiable Information (PII)
- 🔴 **CRITICAL:** Financial information (donation amounts)
- 🔴 **CRITICAL:** Contact information for NGO donors
- 🟡 **MEDIUM:** Campaign attribution data

**Exfiltration Method:**
MySQL dump utility (`mysqldump.exe`) was used to export the complete table structure and data.

**Impact:**
- Donor privacy compromised
- Potential for targeted phishing campaigns
- Reputational damage to NGO-Hub
- GDPR/data protection regulation violations
- Loss of donor trust

---

### 🔟 Exfiltration Tool - Process Image

**Question:** Which process image shows execution of the mysqldump.exe utility?

#### Answer:
```
C:\Program Files\MariaDB 12.0\bin\mysqldump.exe
```

#### Process Execution Analysis:

**Evidence Source:** `sysmon.evtx` (Sysmon Event Logs)

**Process Details:**
- **Image Path:** `C:\Program Files\MariaDB 12.0\bin\mysqldump.exe`
- **Parent Process:** Remote SSH session (via Azure Arc)
- **User Context:** ngo-hub\enygaard
- **Target Database:** MySQL/MariaDB database
- **Output:** `db_dump.sql`

**MySQLDump Command Structure (Typical):**
```bash
mysqldump.exe -u [username] -p[password] -h [host] [database] > db_dump.sql
```

**Attack Technique:**
- **MITRE ATT&CK:** T1005 (Data from Local System)
- **MITRE ATT&CK:** T1119 (Automated Collection)
- **MITRE ATT&CK:** T1560 (Archive Collected Data)

**Why MariaDB 12.0?**
MariaDB is a MySQL-compatible database system. Version 12.0 indicates a recent installation, suggesting the organization was running modern database infrastructure.

---

## 🔍 Complete Attack Chain Reconstruction

### Timeline of Events

```
Phase 1: Initial Compromise (Phishing)
├─ T-0: Phishing email sent with ngo_update.png attachment
├─ T+1: Victim clicks link to http://login.mcrosoft.com/login.html
├─ T+2: Credentials captured by login.php
└─ Result: Username & password compromised (elena.nygaard / Jopa373424)

Phase 2: MFA Bypass & Authentication (2025-08-15 08:02-08:15)
├─ 08:02:59: Initial login attempt
├─ 08:05-08:07: Multiple MFA failures
├─ 08:08:31: "Keep me signed in" interrupt
├─ 08:15:49: ✅ Successful authentication
└─ Result: Full Azure access obtained

Phase 3: Cloud Access & Reconnaissance (08:15-08:48)
├─ 08:15:49: Azure Portal access
├─ 08:16:09-08:16:31: Resource enumeration
├─ 08:48:26: Cloud Shell session initiated
└─ Result: Azure Arc infrastructure discovered

Phase 4: Lateral Movement (08:48+)
├─ Command: az ssh arc --resource-group ngo1 --name db
├─ Target: Database server (DB.ngo-hub.com)
├─ User: enygaard
└─ Result: Database server access achieved

Phase 5: Data Exfiltration (Post-SSH)
├─ Tool: C:\Program Files\MariaDB 12.0\bin\mysqldump.exe
├─ Target: donorrecords table
├─ Output: db_dump.sql
└─ Result: Sensitive donor data exfiltrated
```

---

## 🛡️ MITRE ATT&CK Mapping

### Tactics & Techniques Used

| Tactic | Technique ID | Technique Name | Evidence |
|--------|--------------|----------------|----------|
| **Initial Access** | T1566.001 | Phishing: Spearphishing Attachment | ngo_update.png |
| **Initial Access** | T1566.002 | Phishing: Spearphishing Link | http://login.mcrosoft.com/login.html |
| **Credential Access** | T1056.001 | Input Capture: Keylogging | login.php credential harvesting |
| **Credential Access** | T1621 | Multi-Factor Authentication Request Generation | MFA bypass attempts |
| **Defense Evasion** | T1656 | Impersonation | Typosquatting domain (mcrosoft.com) |
| **Lateral Movement** | T1021.004 | Remote Services: SSH | az ssh arc command |
| **Collection** | T1005 | Data from Local System | Database access |
| **Collection** | T1119 | Automated Collection | mysqldump.exe |
| **Exfiltration** | T1041 | Exfiltration Over C2 Channel | Database dump transfer |

---

## 🚨 Indicators of Compromise (IOCs)

### Network Indicators

**Malicious Domains:**
```
login.mcrosoft.com (Phishing site - Typosquatting)
```

**Attacker IP Addresses:**
```
203.0.113.10 (Successful Azure login)
```

**Attacker Infrastructure:**
```
Hostname: attacker01 (SMTP EHLO)
```

### File Indicators

**Phishing Attachments:**
```
ngo_update.png (SHA-256: [Not provided in evidence])
```

**Malicious Files:**
```
login.php (Credential harvesting backend)
```

**Exfiltrated Data:**
```
db_dump.sql (Database dump containing donorrecords)
```

### Process Indicators

**Suspicious Process Execution:**
```
C:\Program Files\MariaDB 12.0\bin\mysqldump.exe
- Parent: SSH session from Azure Arc
- User: ngo-hub\enygaard
```

### User Accounts

**Compromised Accounts:**
```
Primary: elena.nygaard@ngohubcloud.onmicrosoft.com
Secondary: enygaard (Database server local account)
```

---

## 🔧 Artifacts Analyzed

### Evidence Package Contents

| Artifact | Type | Purpose | Key Findings |
|----------|------|---------|--------------|
| `network_capture.pcapng` | PCAP | Network traffic analysis | HTTP traffic to phishing domain |
| `Cache.zip` | Browser Cache | Chrome browsing history | Phishing site visits |
| `InteractiveSignIns_2025-08-14_2025-08-15.xlsx` | Azure Logs | Authentication analysis | MFA failures, successful login timestamp |
| `hmailserver_2025-08-15.log` | Mail Logs | Email server analysis | SMTP EHLO: attacker01 |
| `Security Verification *.eml` | Email Files | Phishing emails | ngo_update.png attachment |
| `cloudshell_session.log` | Session Logs | Cloud Shell activity | az ssh arc command |
| `db_dump.sql` | Database Export | Exfiltrated data | donorrecords table contents |
| `sysmon.evtx` | Event Logs | Process monitoring | mysqldump.exe execution |
| `ssh.evtx` | Event Logs | SSH connections | Azure Arc SSH sessions |
| `event_logs.evtx` | Event Logs | System events | Authentication events |

---

## 📊 Impact Assessment

### Business Impact

**Immediate:**
- 🔴 **CRITICAL:** Complete donor database compromise
- 🔴 **CRITICAL:** PII exposure for all donors
- 🔴 **CRITICAL:** Financial data (donation amounts) exposed
- 🟡 **HIGH:** Unauthorized Azure infrastructure access
- 🟡 **HIGH:** Lateral movement to database servers

**Long-Term:**
- Loss of donor trust and confidence
- Regulatory fines (GDPR, CCPA, etc.)
- Reputational damage to humanitarian mission
- Potential loss of future donations
- Legal liability for data breach

### Technical Impact

- Complete cloud environment compromise (Azure)
- Database server unauthorized access
- Credential compromise (multiple accounts)
- Potential persistent access mechanisms
- Lateral movement pathways established

---

## 🛠️ Recommendations

### Immediate Actions (0-24 Hours)

1. **Account Remediation:**
   - ✅ Reset password for elena.nygaard@ngohubcloud.onmicrosoft.com
   - ✅ Reset password for enygaard (database server)
   - ✅ Force password reset for all users
   - ✅ Revoke all active Azure sessions

2. **Access Control:**
   - ✅ Disable Azure Arc SSH access temporarily
   - ✅ Review and restrict Cloud Shell permissions
   - ✅ Implement Conditional Access policies

3. **Infrastructure:**
   - ✅ Block domain: login.mcrosoft.com
   - ✅ Block IP: 203.0.113.10
   - ✅ Block SMTP from: attacker01

4. **Data Protection:**
   - ✅ Rotate database credentials
   - ✅ Enable database audit logging
   - ✅ Implement database encryption at rest

### Short-Term Actions (1-7 Days)

1. **MFA Enhancement:**
   - Deploy phishing-resistant MFA (FIDO2, Windows Hello)
   - Implement MFA for all privileged accounts
   - Enable number matching for push notifications
   - Configure MFA fatigue protection

2. **Security Monitoring:**
   - Deploy Azure Sentinel or similar SIEM
   - Enable Microsoft Defender for Cloud
   - Configure alerts for:
     - Unusual login locations
     - Cloud Shell usage
     - Database access patterns
     - Azure Arc SSH connections

3. **User Training:**
   - Conduct phishing awareness training
   - Implement phishing simulation exercises
   - Train users on typosquatting detection
   - Educate on MFA best practices

4. **Email Security:**
   - Implement DMARC, SPF, and DKIM
   - Deploy email security gateway
   - Enable link protection and rewriting
   - Implement attachment sandboxing

### Long-Term Actions (1-3 Months)

1. **Zero Trust Architecture:**
   - Implement least privilege access model
   - Deploy Privileged Access Workstations (PAWs)
   - Implement Just-In-Time (JIT) access
   - Deploy Privileged Identity Management (PIM)

2. **Data Protection:**
   - Classify sensitive data (donor information)
   - Implement Data Loss Prevention (DLP)
   - Deploy Azure Information Protection
   - Regular data access reviews

3. **Incident Response:**
   - Develop comprehensive IR playbook
   - Conduct tabletop exercises
   - Establish 24/7 SOC monitoring
   - Create breach notification procedures

4. **Compliance:**
   - GDPR compliance assessment
   - Data breach notification (if required)
   - Third-party security audit
   - Regulatory reporting (as needed)

---

## 📝 Lessons Learned

### What Went Wrong

1. **User Security Awareness:** Victim fell for typosquatting phishing attack
2. **MFA Implementation:** MFA was eventually bypassed (fatigue/social engineering)
3. **Email Security:** Phishing emails reached user inbox
4. **Privileged Access:** Over-permissioned Azure accounts
5. **Database Security:** Insufficient access controls on database server
6. **Monitoring:** Delayed detection of suspicious activities

### What Went Right

1. **Logging:** Comprehensive logs enabled full attack reconstruction
2. **Evidence Preservation:** All artifacts retained for forensic analysis
3. **Azure Arc:** Logging of SSH connections provided visibility
4. **Sysmon:** Process execution monitoring captured mysqldump usage
5. **Mail Logs:** SMTP logs revealed attacker infrastructure

---

## 🎓 Investigation Methodology

### Tools Used

- **Email Analysis:** Outlook, Python email parsing
- **Network Analysis:** Wireshark (pcapng analysis)
- **Log Analysis:** Excel, PowerShell, Python scripts
- **Database Analysis:** SQL viewer, text editors
- **Timeline Analysis:** Custom Python scripts
- **Event Log Analysis:** Event Viewer, Sysmon

### Investigation Workflow

1. **Evidence Collection:** Gathered all artifacts from evidence package
2. **Timeline Creation:** Established chronological order of events
3. **Artifact Analysis:** Deep-dive into each evidence type
4. **Pattern Recognition:** Identified attack techniques and TTPs
5. **IOC Extraction:** Documented all indicators of compromise
6. **Report Generation:** Comprehensive documentation of findings

---

## ✅ Investigation Objectives - Complete

| # | Question | Answer | Status |
|---|----------|--------|--------|
| 1 | Phishing attachment file | ngo_update.png | ✅ |
| 2 | Phishing URL | http://login.mcrosoft.com/login.html | ✅ |
| 3 | PHP credential harvester | login.php | ✅ |
| 4 | Compromised password | Jopa373424 | ✅ |
| 5 | SMTP EHLO hostname | attacker01 | ✅ |
| 6 | MFA failure message | Authentication failed during strong authentication request. | ✅ |
| 7 | Successful login timestamp | 08:15:49 | ✅ |
| 8 | Azure CLI subcommand | ssh arc | ✅ |
| 9 | Exfiltrated table | donorrecords | ✅ |
| 10 | mysqldump.exe path | C:\Program Files\MariaDB 12.0\bin\mysqldump.exe | ✅ |

**Investigation Status:** ✅ **COMPLETE - ALL OBJECTIVES ACHIEVED**

---

## 🏁 Conclusion

The Echo Trail investigation successfully reconstructed a sophisticated multi-stage attack against Empathreach's NGO-Hub infrastructure. The adversary demonstrated advanced capabilities including:

- Social engineering through phishing campaigns
- Typosquatting domain abuse
- MFA bypass techniques
- Azure cloud infrastructure exploitation
- Lateral movement via Azure Arc SSH
- Database exfiltration using legitimate tools

The attack represents a significant threat to the Nullform Key metadata, the final piece needed by the adversary to complete their collection of the three Primal Keys.

**All 10 investigation objectives have been successfully answered, providing Empathreach with the intelligence needed to fortify their defenses against future incursions.**

---

**Report Completed:** October 28, 2025  
**Investigator:** MR. Umair  
**Case Status:** ✅ CLOSED - All objectives achieved  
**Next Steps:** Implement recommended security controls and continue monitoring for additional adversary activity

---

*"Every artifact holds meaning, and every response leaves its own echo behind."*
