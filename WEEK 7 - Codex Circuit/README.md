# Week 7 - Codex Circuit 🌐

**Challenge Name:** Slack Data Exfiltration Investigation  
**Difficulty:** Easy  
**Category:** Network Forensics, Incident Response, PCAP Analysis  
**Date Completed:** November 18, 2025

---

## 📖 Challenge Overview

At the heart of the Cyber Realms lies the **Codex Circuit**, the foundation of every permission, boundary, vault, and soulprint. With Voidweaver, the Emerald Bear Wizard, ready to activate it using the Trinary Cipher, a critical alert pierces the chaos: confidential MegaCorp documents have surfaced on a public forum.

The Security Operations Center suspects internal misuse of collaboration tools. If Voidweaver gains access, everything could unravel.

This challenge involves analyzing captured network traffic (`megacorp.pcap`) to uncover whether sensitive data was exfiltrated via Slack, identifying the users involved, and determining whether the data now lies in enemy hands.

**Provided Artifacts:**
- `megacorp.pcap` - Network packet capture (234,337 packets, ~325MB)
- Challenge questions and context files

**Mission:** Analyze the PCAP, identify the exfiltration, and answer key investigative questions.

---

## 🎯 Challenge Questions & Solutions

### Question 1: File Type of Exfiltrated Document
**Task:** What was the file type of the exfiltrated document?

**Answer:** `Excel spreadsheet (.xls)`

**Discovery Method:**
- Analyzed file upload messages in the PCAP
- Found `sensitive_customer_list.xls` with MIME type `application/vnd.ms-excel`
- File size: 6656 bytes
- Located in packet 21222 (internal upload) and packet 27162 (rogue upload)

---

### Question 2: User Who Uploaded to Rogue Workspace
**Task:** Which user uploaded the sensitive file to the rogue workspace?

**Answer:** `James Brown`

**Discovery Method:**
- Searched for `user_change` and `user_profile_changed` events in PCAP
- Found user profile in packet 26916:
  ```json
  {
    "id": "U09KRBDV8S1",
    "name": "jamesb",
    "real_name": "james brown"
  }
  ```
- Confirmed upload to rogue workspace in packet 27162
- Rogue workspace: `secret-ops-workspace.slack.com` (Team ID: T09KSNJU27Q)

---

### Question 3: GMT Time File Was Shared Internally
**Task:** At what GMT time was the sensitive file shared internally, within the legitimate company?

**Answer:** `2025-10-10 11:51:36 GMT`

**Discovery Method:**
- Distinguished between file **upload** and file **share** events
- File uploaded: timestamp `1760097092` = 2025-10-10 11:51:32 GMT (packet 21222)
- File shared to channel: `file_shared` event at timestamp `1760097096.001600` (packet 21237)
- The share event is when it became accessible to the team

**Key Evidence:**
```json
{
  "type": "file_shared",
  "file_id": "F09KYB2DERJ",
  "user_id": "U09KA40P3F0",
  "channel_id": "C09L7LPF4Q1",
  "ts": "1760097096.001600"
}
```

---

### Question 4: Internal User Who Shared the Document
**Task:** Which internal user initially shared the sensitive document?

**Answer:** `Ava`

**Discovery Method:**
- User ID `U09KA40P3F0` uploaded the file (packet 21222)
- No full user profile found in PCAP for this user
- Found context in conversation messages:
  - "thanks for sharing, Ava" (User U09KAAYFSBY thanking Ava)
  - "thank you Emma and Ava" (User U09KLC2V202 acknowledging Ava)
- Confirmed Ava = U09KA40P3F0 based on conversation context
- File shared with message: "no worries, here's the latest customer"

---

### Question 5: Rogue Server FQDN
**Task:** What domain hostname FQDN is associated with the rogue server?

**Answer:** `secret-ops-workspace.slack.com`

**Discovery Method:**
- Analyzed all Slack workspace domains in PCAP
- Legitimate workspace: `team-megacorp.slack.com` (Team ID: T09KR3R0PFB)
- Rogue workspace found in packet 27162:
  ```
  Workspace: secret-ops-workspace.slack.com
  Team ID: T09KSNJU27Q
  Channel: C09KSNR5F6J (secret-ops-collaboration)
  ```
- Confirmed exfiltration when James Brown uploaded the same file to this rogue workspace

---

### Question 6: File Uploaded Before Sensitive One
**Task:** Which file was uploaded right before the sensitive one?

**Answer:** `meeting-minutes_2025-10-09.pdf`

**Discovery Method:**
- Extracted chronological file upload timeline from PCAP:

| Time (GMT) | File | User |
|------------|------|------|
| 2025-10-10 11:46:58 | architecture_diagram.png | U09KA40P3F0 |
| 2025-10-10 11:47:16 | onboarding_checklist.docx | U09KA40P3F0 |
| 2025-10-10 11:47:25 | **meeting-minutes_2025-10-09.pdf** | U09KA40P3F0 |
| 2025-10-10 11:51:32 | sensitive_customer_list.xls | U09KA40P3F0 |

- The file uploaded immediately before the sensitive file was `meeting-minutes_2025-10-09.pdf`

---

### Question 7: Last Customer Email Address
**Task:** What is the email address of the last customer listed in the sensitive file?

**Answer:** `carol@novaenergy.com`

**Discovery Method:**
- Extracted the Excel file from PCAP (packet 21194 contained file data)
- Parsed `sensitive_customer_list.xls` using pandas
- Found 3 customers in the spreadsheet:

| Customer | Organization | Email | Account Value |
|----------|-------------|-------|---------------|
| Horizon Analytics | Horizon Data Group | dave@horizondg.com | $100,000 |
| Beta Retail | Beta Retail Inc. | bob@beta.com | $75,000 |
| **Nova Energy** | **Nova Energy ASA** | **carol@novaenergy.com** | **$125,000** |

- Last customer (row 3): **Nova Energy** with email `carol@novaenergy.com`

---

## 🔍 Technical Analysis Details

### PCAP Statistics
- **Total Packets:** 234,337
- **Capture Duration:** ~22 minutes (1760096413 to 1760097734)
- **HTTP Packets:** 1,184
- **Slack API Requests:** 446

### Key Packet Numbers
- **Packet 12662-12664:** Channel `company_documents` created by U09KA40P3F0
- **Packet 21194:** Excel file data in multipart/form-data
- **Packet 21222:** Internal file upload to MegaCorp workspace
- **Packet 21237:** `file_shared` event (file shared to channel)
- **Packet 26916:** James Brown user profile data
- **Packet 27162:** Rogue workspace upload by James Brown

### Timeline of Events
1. **11:44:57 GMT** - `company_documents` channel created
2. **11:46:58 GMT** - `architecture_diagram.png` uploaded
3. **11:47:16 GMT** - `onboarding_checklist.docx` uploaded
4. **11:47:25 GMT** - `meeting-minutes_2025-10-09.pdf` uploaded
5. **11:51:32 GMT** - `sensitive_customer_list.xls` uploaded by Ava
6. **11:51:36 GMT** - File shared to channel (file_shared event)
7. **11:57:48 GMT** - Same file exfiltrated to rogue workspace by James Brown

---

## 🛠️ Tools & Techniques Used

**Analysis Tools:**
- **Scapy** - Python packet manipulation and PCAP analysis
- **Pandas** - Excel file parsing
- **Python regex** - Pattern matching for user profiles, timestamps, file events

**Key Techniques:**
1. **HTTP POST Analysis** - Examining Slack API requests (`files.upload`, `conversations.history`)
2. **JSON Parsing** - Extracting structured data from API responses
3. **Timeline Reconstruction** - Building chronological sequence of events
4. **User Correlation** - Matching user IDs with names from conversation context
5. **File Extraction** - Recovering uploaded Excel file from packet payload
6. **Timestamp Conversion** - Converting Unix timestamps to GMT format

---

## 🐍 Python Scripts

### 1. analyze_slack_exfiltration.py
A comprehensive PCAP analysis tool for Slack forensics.

**Features:**
- Loads PCAP using Scapy
- Searches for file upload events
- Extracts JSON payloads from HTTP packets
- Identifies user profiles and conversation messages
- Converts Unix timestamps to GMT format

**Key Functions:**
- `rdpcap()` - Load PCAP file
- `re.findall()` - Extract patterns from payloads
- Timestamp conversion (Unix → GMT)
- JSON parsing for Slack API responses

### 2. find_exfiltration.py
Focused script for detecting data exfiltration events in PCAP.

**Features:**
- Searches for file upload events to rogue workspaces
- Identifies suspicious file transfer patterns
- Extracts exfiltration timestamps and user information

**Key Functions:**
- Packet filtering for suspicious Slack traffic
- JSON event parsing for rogue workspace uploads
- Timestamp conversion and validation

### 3. question.txt
Challenge questions file containing the 7 investigation questions.

**Python Script:** `analyze_slack_exfiltration.py`

---

## 🏆 Key Findings

**Incident Summary:**
- **Threat Actor:** James Brown (U09KRBDV8S1)
- **Internal Victim:** Ava (U09KA40P3F0)
- **Exfiltrated Data:** Customer list with 3 records, total account value $300,000
- **Attack Vector:** Insider threat - James Brown had access to legitimate workspace, then uploaded sensitive file to rogue workspace
- **Data Loss:** Customer names, organizations, email addresses, phone numbers, account values

**Security Implications:**
- Internal collaboration tools can be weaponized for data exfiltration
- User with access to multiple Slack workspaces poses insider threat risk
- File sharing events should be monitored and logged
- Sensitive customer data exposed to unauthorized workspace

---

## 📚 Lessons Learned

1. **Network Monitoring:** PCAP analysis can reveal data exfiltration via collaboration tools
2. **Slack Forensics:** File upload/share events leave distinct traces in network traffic
3. **User Attribution:** Conversation context can identify users when profile data is incomplete
4. **Timeline Analysis:** Distinguishing between upload and share events is critical
5. **Data Recovery:** Excel files can be extracted and analyzed from packet captures

---

## 🔗 References

- **OffSec Proving Grounds:** Echo Response Challenge Series
- **Scapy Documentation:** https://scapy.net/
- **Slack API:** File upload and sharing event structures

---

**Challenge Status:** ✅ Completed  
**All Questions Answered:** 7/7  
