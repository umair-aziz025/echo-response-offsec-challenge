# Investigation Report: Codex Circuit - Slack Data Exfiltration

**Incident ID:** WEEK7-CODEX-CIRCUIT  
**Investigation Date:** November 18, 2025  
**Investigator:** MR. Umair   
**Classification:** Data Exfiltration via Collaboration Tools

---

## Executive Summary

This investigation analyzed a suspected data exfiltration incident at MegaCorp where sensitive customer information was leaked through Slack collaboration tools. Through PCAP analysis of 234,337 network packets, I identified a clear chain of events showing an internal employee (Ava) sharing a customer list file, which was subsequently exfiltrated to a rogue Slack workspace by another user (James Brown).

**Key Findings:**
- **Sensitive File:** `sensitive_customer_list.xls` containing 3 customer records worth $300,000
- **Internal User:** Ava (U09KA40P3F0) shared the file at 2025-10-10 11:51:36 GMT
- **Threat Actor:** James Brown (U09KRBDV8S1) exfiltrated to rogue workspace
- **Exfiltration Method:** Upload to unauthorized Slack workspace `secret-ops-workspace.slack.com`
- **Data at Risk:** Customer names, emails, phone numbers, account values

---

## Investigation Methodology

### 1. Initial Triage
**Objective:** Understand the scope and nature of the PCAP file

**Actions Taken:**
```python
from scapy.all import rdpcap
packets = rdpcap('megacorp.pcap')
print(f"Total packets: {len(packets)}")
```

**Results:**
- Packet count: 234,337
- Capture timeframe: ~22 minutes
- Identified 1,184 HTTP packets
- Found 446 Slack API requests

### 2. Protocol Analysis
**Objective:** Identify Slack-specific traffic patterns

**Findings:**
- Slack uses HTTPS for all API communication
- File uploads use `files.upload` API endpoint
- File shares trigger `file_shared` WebSocket events
- Conversation history available via `conversations.history`

### 3. File Upload Timeline Reconstruction

**Method:**
Searched for file upload events by parsing JSON payloads in HTTP POST requests.

**Python Code:**
```python
file_events = []
for packet in packets:
    if packet.haslayer('Raw'):
        payload = packet['Raw'].load.decode('latin-1', errors='ignore')
        file_matches = re.findall(
            r'"name":"([^"]+\.(?:xls|pdf|png|docx))"[^}]*"timestamp":(\d+)',
            payload
        )
        for filename, ts in file_matches:
            file_events.append({'filename': filename, 'timestamp': int(ts)})
```

**Timeline Discovered:**
| Timestamp | GMT Time | File | Event |
|-----------|----------|------|-------|
| 1760096697 | 11:44:57 | - | Channel `company_documents` created |
| 1760096818 | 11:46:58 | architecture_diagram.png | Uploaded |
| 1760096836 | 11:47:16 | onboarding_checklist.docx | Uploaded |
| 1760096845 | 11:47:25 | meeting-minutes_2025-10-09.pdf | Uploaded |
| 1760097092 | 11:51:32 | sensitive_customer_list.xls | **Uploaded** |
| 1760097096 | 11:51:36 | sensitive_customer_list.xls | **Shared to channel** |
| 1760097468 | 11:57:48 | sensitive_customer_list.xls | **Exfiltrated to rogue workspace** |

**Critical Observation:**  
6-minute gap between internal share (11:51:36) and rogue upload (11:57:48) suggests opportunistic exfiltration.

---

## 4. User Identification

### Internal User Analysis

**Challenge:** User ID `U09KA40P3F0` had no profile data in PCAP

**Resolution Method:**
Analyzed conversation messages for context clues:

**Packet Analysis:**
```
Conversation_18.json:
{
  "text": "thanks for sharing, Ava, I am sure James could also comment",
  "user": "U09KAAYFSBY",
  "ts": "1760097020.187409"
}
```

**Draft Message (Packet 20):**
```json
{
  "user_id": "U09KA40P3F0",
  "text": "no worries, here's the latest customer",
  "channel_id": "C09L7LPF4Q1"
}
```

**Conclusion:**  
User U09KA40P3F0 = **Ava** (confirmed via conversation context)

### Threat Actor Identification

**User Profile Discovery (Packet 26916):**
```json
{
  "type": "user_change",
  "user": {
    "id": "U09KRBDV8S1",
    "team_id": "T09KSNJU27Q",
    "name": "jamesb",
    "real_name": "james brown"
  }
}
```

**Rogue Upload Confirmation (Packet 27162):**
```json
{
  "user": "U09KRBDV8S1",
  "files": [{
    "name": "sensitive_customer_list.xls",
    "size": 6656
  }],
  "team": "T09KSNJU27Q"
}
```

**Conclusion:**  
User U09KRBDV8S1 = **James Brown** (rogue workspace uploader)

---

## 5. Workspace Identification

**Legitimate Workspace:**
- Domain: `team-megacorp.slack.com`
- Team ID: `T09KR3R0PFB`
- Channel: `C09L7LPF4Q1` (company_documents)

**Rogue Workspace:**
- Domain: `secret-ops-workspace.slack.com`
- Team ID: `T09KSNJU27Q`
- Channel: `C09KSNR5F6J` (secret-ops-collaboration)
- Creator: James Brown (U09KRBDV8S1)

**Evidence:**
Channel creation event in packet 26985 shows James Brown created `secret-ops-collaboration` channel at timestamp 1760097443.

---

## 6. File Content Analysis

### Excel File Extraction

**Method:**  
Located file data in packet 21194 (multipart/form-data boundary)

**Extraction Process:**
```python
import pandas as pd
df = pd.read_excel('sensitive_customer_list.xls')
print(df.to_string())
```

**Recovered Data:**
| Row | Customer Name | Organization | Email | Phone | Account Value |
|-----|---------------|--------------|-------|-------|---------------|
| 1 | Horizon Analytics | Horizon Data Group | dave@horizondg.com | 555-0100 | $100,000 |
| 2 | Beta Retail | Beta Retail Inc. | bob@beta.com | 555-0200 | $75,000 |
| 3 | Nova Energy | Nova Energy ASA | carol@novaenergy.com | 555-0300 | $125,000 |

**Data Sensitivity Assessment:**
- **High Risk:** Customer PII (emails, phone numbers)
- **Financial Impact:** $300,000 total account value
- **Compliance:** Potential GDPR/privacy violations

---

## 7. Event Correlation

### Key Distinction: Upload vs. Share

**Upload Event (Packet 21222):**
```json
{
  "type": "message",
  "user": "U09KA40P3F0",
  "files": [{
    "id": "F09KYB2DERJ",
    "created": 1760097092,
    "timestamp": 1760097092
  }]
}
```
- Time: 11:51:32 GMT
- Action: File uploaded to Slack
- Visibility: Limited (not yet shared)

**Share Event (Packet 21237):**
```json
{
  "type": "file_shared",
  "file_id": "F09KYB2DERJ",
  "user_id": "U09KA40P3F0",
  "channel_id": "C09L7LPF4Q1",
  "ts": "1760097096.001600"
}
```
- Time: 11:51:36 GMT (4 seconds later)
- Action: File shared to channel
- Visibility: All channel members can now access

**Significance:**  
The **share event** is the critical moment when data became accessible to James Brown.

---

## Attack Chain Analysis

```
1. Ava (U09KA40P3F0) uploads sensitive_customer_list.xls
   ↓ [11:51:32 GMT - Packet 21222]
   
2. Ava shares file to #company_documents channel
   ↓ [11:51:36 GMT - Packet 21237 - file_shared event]
   
3. James Brown (member of channel) downloads file
   ↓ [Access granted via legitimate workspace]
   
4. James Brown uploads same file to rogue workspace
   ↓ [11:57:48 GMT - Packet 27162]
   
5. File now accessible on secret-ops-workspace.slack.com
   ✓ [Data exfiltration complete]
```

**Attack Duration:** 6 minutes 12 seconds

---

## Indicators of Compromise (IOCs)

### Network Indicators
- **Rogue Domain:** `secret-ops-workspace.slack.com`
- **Rogue Team ID:** `T09KSNJU27Q`
- **Rogue Channel:** `C09KSNR5F6J`

### File Indicators
- **Filename:** `sensitive_customer_list.xls`
- **File Hash (from PCAP):** F09KYB2DERJ (Slack file ID)
- **File Size:** 6,656 bytes
- **MIME Type:** `application/vnd.ms-excel`

### User Indicators
- **Suspicious User:** U09KRBDV8S1 (James Brown, jamesb)
- **Compromised User:** U09KA40P3F0 (Ava) - possibly social engineered

---

## Root Cause Analysis

**Primary Cause:**  
Insider threat - James Brown had legitimate access to both workspaces and exploited trust relationship.

**Contributing Factors:**
1. **No Data Loss Prevention (DLP):** No controls to prevent file sharing between workspaces
2. **Insufficient Monitoring:** File exfiltration not detected in real-time
3. **Weak Access Controls:** User able to be member of multiple Slack workspaces
4. **Lack of Classification:** Sensitive file not marked or protected
5. **No Egress Filtering:** Outbound file transfers not monitored

---

## Recommendations

### Immediate Actions
1. **Revoke Access:** Disable James Brown's account (U09KRBDV8S1)
2. **Audit Activity:** Review all file shares by James Brown
3. **Notify Customers:** Inform affected customers (Horizon Analytics, Beta Retail, Nova Energy)
4. **Preserve Evidence:** Secure PCAP file and Slack workspace logs

### Short-term (1-3 months)
1. **DLP Implementation:** Deploy Slack DLP to detect sensitive data patterns
2. **Workspace Policy:** Restrict users to single Slack workspace
3. **File Classification:** Implement sensitivity labels for documents
4. **Monitoring Enhancement:** Real-time alerts for file exfiltration

### Long-term (3-12 months)
1. **Zero Trust Architecture:** Implement least-privilege access model
2. **User Behavior Analytics:** Deploy UEBA to detect anomalous file activity
3. **Security Awareness:** Train staff on data handling and insider threats
4. **Incident Response:** Develop playbook for collaboration tool exfiltration

---

## Lessons Learned

### Technical Insights
1. **PCAP Analysis:** Slack API traffic contains rich forensic evidence
2. **Event Sequencing:** Upload ≠ Share - understand application-level events
3. **User Attribution:** Context clues (conversation messages) can identify users
4. **File Recovery:** Exfiltrated files can be extracted from packet captures

### Security Insights
1. **Collaboration Tools = Attack Surface:** Slack/Teams can be weaponized
2. **Insider Threats:** Trusted users with multi-workspace access pose risk
3. **Network Monitoring:** Even encrypted traffic reveals patterns and metadata
4. **Timeline Matters:** Understanding event sequence reveals attack methodology

---

## Conclusion

This investigation successfully identified a data exfiltration incident where James Brown uploaded MegaCorp's customer list to an unauthorized Slack workspace. The attack was opportunistic, occurring within 6 minutes of the file being shared internally by Ava.

Through systematic PCAP analysis, I reconstructed the complete timeline, identified all parties involved, recovered the exfiltrated data, and provided actionable recommendations to prevent future incidents.

**Incident Status:** CLOSED - Root cause identified, remediation recommended

---

**Date:** November 18, 2025  
**Investigator:** Mr. Umair  
**Case:** OffSec Echo Response - Week 7: Codex Circuit

---

*"At the heart of the Cyber Realms lies the Codex Circuit—the foundation of every permission, boundary, vault, and soulprint. But when collaboration becomes a weapon, even the most trusted systems can betray us."*

