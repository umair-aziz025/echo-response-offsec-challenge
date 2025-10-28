# WEEK 4 - Echo Trail 🔍

**Challenge:** Echo Trail - NGO-Hub Breach Investigation  
**Date:** October 28, 2025  
**Status:** ✅ COMPLETED  
**Category:** Incident Response, Cloud Security, Digital Forensics  
**Difficulty:** Intermediate

---

## 📖 Challenge Overview

### Scenario

*"The adversary now holds two of the three Primal Keys – the Etherian and the Obscuran. Only one remains: the Nullform Key, a relic of entropy and rebirth, said to lie dormant beneath the ruins of lost systems."*

Deep within **Empathreach** (home of NGO-Hub), a vast humanitarian nexus connecting relief efforts across high-risk zones, lies an ancient artifact containing metadata—a locator for the **Nullform Key**. Subtle signs of intrusion have emerged: strange outbound traffic, hints of lateral movement, and irregular authentication spikes.

**Mission:** Map the adversary's previous infiltration, chart their movements, and ensure Empathreach is fortified against future incursions.

---

## 🎯 Investigation Objectives

Analyze the provided artifacts to answer the following questions:

1. ✅ Which file was attached to the phishing email that started the compromise?
2. ✅ What was the entire URL associated with the phishing page?
3. ✅ What is likely the PHP attacker file name responsible for intercepting the credentials?
4. ✅ What is the valid Azure password obtained through phishing?
5. ✅ What hostname did the attacker present in EHLO?
6. ✅ What failure specific message is provided in Azure when MFA is not succeeding?
7. ✅ At what specific timestamp the attacker succeeded in logging in with the victim account?
8. ✅ Which Azure CLI subcommand initiated the server connection from Cloud Shell?
9. ✅ From which table were records extracted?
10. ✅ Which process image shows execution of the mysqldump.exe utility?

---

## 📦 Available Artifacts

The evidence package (`echo_trail.zip`, password: `EchoTrail123`) contains:

| Artifact | Type | Description |
|----------|------|-------------|
| `network_capture.pcapng` | Network Capture | Packet capture from incident timeframe |
| `Cache.zip` | Browser Data | Chrome browser raw cache files |
| `InteractiveSignIns_2025-08-14_2025-08-15.xlsx` | Azure Logs | Entra ID Sign-in logs |
| `hmailserver_2025-08-15.log` | Mail Logs | Mail server message trace logs |
| `Security Verification *.eml` | Email Files | Phishing email samples |
| `cloudshell_session.log` | Session Logs | Azure Cloud Shell session recording |
| `db_dump.sql` | Database Dump | Exfiltrated database records |
| `sysmon.evtx` | Event Logs | Sysmon process monitoring logs |
| `ssh.evtx` | Event Logs | SSH connection event logs |
| `event_logs.evtx` | Event Logs | Windows security event logs |

---

## 🔑 Key Findings

### Attack Summary

**Victim:** Elena Nygaard (elena.nygaard@ngohubcloud.onmicrosoft.com)  
**Target Organization:** Empathreach / NGO-Hub  
**Attack Type:** Multi-stage phishing → Credential theft → MFA bypass → Cloud exploitation → Data exfiltration

### Attack Chain

```
1. Initial Compromise (Phishing)
   └─ Email with ngo_update.png attachment
   └─ Malicious link: http://login.mcrosoft.com/login.html
   └─ Credential harvesting via login.php

2. Authentication Bypass
   └─ Multiple MFA failures (08:05-08:07 UTC)
   └─ Successful login: 08:15:49 UTC
   └─ Azure Portal access gained

3. Lateral Movement
   └─ Azure Cloud Shell initiated (08:48:26 UTC)
   └─ Command: az ssh arc --resource-group ngo1 --name db
   └─ Target: Database server (DB.ngo-hub.com)

4. Data Exfiltration
   └─ Tool: mysqldump.exe (MariaDB 12.0)
   └─ Target: donorrecords table
   └─ Output: db_dump.sql
```

### Critical IOCs

**Domains:**
- `login.mcrosoft.com` (Typosquatting - Microsoft)

**IP Addresses:**
- `203.0.113.10` (Attacker authentication source)

**Compromised Credentials:**
- Username: `elena.nygaard@ngohubcloud.onmicrosoft.com`
- Password: `Jopa373424`

**Malicious Infrastructure:**
- SMTP Hostname: `attacker01`

---

## 🛠️ Analysis Techniques

### 1. Email Forensics
- Analyzed `.eml` files to identify phishing attachments
- Extracted sender information and email headers
- Identified social engineering tactics

### 2. Network Traffic Analysis
- Wireshark analysis of `network_capture.pcapng`
- HTTP traffic inspection to phishing domain
- DNS resolution tracking

### 3. Azure Log Analysis
- Excel/PowerShell parsing of Azure sign-in logs
- Timeline reconstruction of authentication events
- MFA failure pattern analysis
- Successful login timestamp identification

### 4. Mail Server Log Analysis
- SMTP protocol analysis from `hmailserver` logs
- EHLO hostname extraction
- Email routing investigation

### 5. Cloud Shell Forensics
- Session log parsing (`cloudshell_session.log`)
- Azure CLI command extraction
- Lateral movement technique identification

### 6. Database Forensics
- SQL dump analysis (`db_dump.sql`)
- Table structure examination
- Exfiltrated data assessment

### 7. Windows Event Log Analysis
- Sysmon process monitoring review
- Process execution tracking (mysqldump.exe)
- Parent-child process relationships

---

## 📊 MITRE ATT&CK Mapping

| Tactic | Technique | Evidence |
|--------|-----------|----------|
| Initial Access | T1566.001 - Phishing: Spearphishing Attachment | ngo_update.png |
| Initial Access | T1566.002 - Phishing: Spearphishing Link | http://login.mcrosoft.com/login.html |
| Credential Access | T1056.001 - Input Capture: Keylogging | login.php |
| Credential Access | T1621 - Multi-Factor Authentication Request Generation | MFA bypass attempts |
| Defense Evasion | T1656 - Impersonation | Typosquatting domain |
| Lateral Movement | T1021.004 - Remote Services: SSH | az ssh arc |
| Collection | T1005 - Data from Local System | Database access |
| Collection | T1119 - Automated Collection | mysqldump.exe |
| Exfiltration | T1041 - Exfiltration Over C2 Channel | Database dump |

---

## 🔬 Technical Deep Dive

### Phishing Infrastructure

**Domain Typosquatting:**
```
Legitimate: microsoft.com
Malicious:  mcrosoft.com (missing 'i')
```

**Credential Harvesting Flow:**
1. Victim receives "Security Verification" email
2. Clicks malicious link to fake Microsoft login
3. Enters credentials into phishing form
4. `login.php` captures and stores credentials
5. Possible redirect to legitimate site (to avoid suspicion)

### MFA Bypass Analysis

**Timeline of MFA Attempts:**
- Multiple "Strong Authentication is required" prompts
- Repeated "Authentication failed during strong authentication request"
- Eventually successful: "MFA requirement satisfied by claim in the token"

**Possible Bypass Methods:**
1. MFA Fatigue Attack (repeated prompts until victim approves)
2. Social Engineering (victim provides MFA code)
3. Session Token Theft
4. Compromised Authentication Method

### Azure Arc SSH Exploitation

**Command Executed:**
```bash
az ssh arc --subscription 65f29041-a905-45dd-aebd-6fbf877ed89e \
           --resource-group ngo1 \
           --name db \
           --local-user enygaard
```

**Why This Matters:**
- Azure Arc enables management of on-premises servers through Azure
- SSH access bypasses traditional firewall rules
- Legitimate Azure service abused for lateral movement
- Difficult to detect without proper cloud monitoring

### Database Exfiltration

**Tool:** MariaDB mysqldump utility  
**Path:** `C:\Program Files\MariaDB 12.0\bin\mysqldump.exe`

**Typical Command:**
```bash
mysqldump -u username -p password -h host database_name > db_dump.sql
```

**Impact:**
- Complete `donorrecords` table exfiltrated
- PII exposure (donor names, emails)
- Financial data (donation amounts)
- Campaign attribution data
- GDPR/compliance violations

---

## 💡 Lessons Learned

### Security Gaps Identified

1. **User Awareness:**
   - Failed to recognize typosquatting domain
   - Did not verify HTTPS before entering credentials
   - Susceptible to social engineering

2. **Email Security:**
   - Phishing emails reached inbox
   - No link protection or URL rewriting
   - Insufficient email filtering

3. **MFA Implementation:**
   - MFA bypass was successful
   - No phishing-resistant MFA (FIDO2)
   - Possible MFA fatigue vulnerability

4. **Cloud Security:**
   - Overly permissive Azure access
   - Azure Arc SSH not properly restricted
   - Cloud Shell permissions too broad

5. **Database Security:**
   - Insufficient database access controls
   - No data exfiltration detection
   - Missing audit logging

---

## 🛡️ Recommended Mitigations

### Immediate Actions

1. **Reset all compromised credentials**
2. **Revoke active Azure sessions**
3. **Block malicious domain and IP**
4. **Disable Azure Arc SSH temporarily**
5. **Enable database audit logging**

### Short-Term Actions

1. **Deploy phishing-resistant MFA (FIDO2)**
2. **Implement Conditional Access policies**
3. **Enable Microsoft Defender for Cloud**
4. **Conduct security awareness training**
5. **Implement email security gateway**

### Long-Term Actions

1. **Adopt Zero Trust architecture**
2. **Implement Privileged Access Management**
3. **Deploy Data Loss Prevention (DLP)**
4. **Establish 24/7 SOC monitoring**
5. **Conduct regular security audits**

---

## 📚 Skills Demonstrated

- ✅ **Email Forensics:** Phishing email analysis and IOC extraction
- ✅ **Network Analysis:** PCAP analysis with Wireshark
- ✅ **Cloud Security:** Azure AD log analysis and investigation
- ✅ **Log Analysis:** Multi-source log correlation (SMTP, Azure, Sysmon, Windows Event Logs)
- ✅ **Timeline Analysis:** Chronological attack chain reconstruction
- ✅ **Database Forensics:** SQL dump analysis and data impact assessment
- ✅ **Incident Response:** Complete IR lifecycle from detection to remediation
- ✅ **MITRE ATT&CK:** Threat mapping and TTPs identification
- ✅ **Python Scripting:** Custom analysis tools for log parsing
- ✅ **Reporting:** Comprehensive technical documentation

---

## 📁 Repository Contents

```
WEEK 4 - Echo Trail/
├── README.md (this file)
├── INVESTIGATION_REPORT.md (detailed findings)
├── analyze_logs.py (Azure sign-in log parser)
└── evidence/
    ├── network_capture.pcapng
    ├── Cache.zip
    ├── InteractiveSignIns_2025-08-14_2025-08-15.xlsx
    ├── hmailserver_2025-08-15.log
    ├── cloudshell_session.log
    ├── db_dump.sql
    ├── sysmon.evtx
    ├── ssh.evtx
    ├── event_logs.evtx
    └── *.eml (phishing emails)
```

---

## 🏆 Challenge Completion

**Status:** ✅ **ALL 10 OBJECTIVES COMPLETED**

| Question | Answer | Evidence Source |
|----------|--------|----------------|
| Q1 | ngo_update.png | Email files (.eml) |
| Q2 | http://login.mcrosoft.com/login.html | Email/network analysis |
| Q3 | login.php | Phishing infrastructure analysis |
| Q4 | Jopa373424 | Credential capture simulation |
| Q5 | attacker01 | hmailserver_2025-08-15.log |
| Q6 | Authentication failed during strong authentication request. | Azure sign-in logs |
| Q7 | 08:15:49 | Azure sign-in logs |
| Q8 | ssh arc | cloudshell_session.log |
| Q9 | donorrecords | db_dump.sql |
| Q10 | C:\Program Files\MariaDB 12.0\bin\mysqldump.exe | sysmon.evtx |

---

## 🔗 Resources

- [Azure Arc SSH Documentation](https://learn.microsoft.com/en-us/azure/azure-arc/servers/ssh-arc-overview)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [Sysmon Documentation](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)
- [Azure AD Sign-in Logs](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-ins)

---

**Investigator:** MR. Umair  
**Date Completed:** October 28, 2025  
**Challenge Series:** OffSec Echo Response - Proving Grounds: The Gauntlet

---

*"Map the adversary's previous infiltration, chart their movements, and ensure Empathreach is fortified against future incursions."*
