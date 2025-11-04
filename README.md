# Echo Response - OffSec Challenge Solutions 🛡️

Welcome to my solution repository for the **OffSec Echo Response** cybersecurity challenge series! This repo contains detailed writeups, investigation reports, and solution scripts for each weekly challenge from the "Proving Grounds: The Gauntlet" event.

---

## 📖 About Echo Response

> *"In the vast multiverse where magic and cybersecurity intertwine, the OffSec Legends, elite guides and guardians, have long upheld the fragile balance between the Cyber Realms. But now, shadows stir."*

Echo Response is a high-stakes cyber defense simulation featuring escalating scenarios inspired by real-world threats. Each week brings new challenges testing detection, forensics, malware analysis, and incident response skills.

---

## 📂 Challenge Solutions

### ✅ [Week 1 - ProtoVault Breach](./WEEK%201%20-%20ProtoVault%20Breach)
**Status:** COMPLETED  
**Category:** Incident Response, Digital Forensics, OSINT  
**Difficulty:** Beginner

**Scenario:** A database breach at ProtoVault with ransom demands. Investigation revealed hardcoded credentials, public S3 buckets, and Git history leaks.

**Key Skills:**
- Git forensics and artifact recovery
- ROT13 decoding
- AWS S3 security analysis
- Source code security review

**Files:**
- [Investigation Report](./WEEK%201%20-%20ProtoVault%20Breach/INVESTIGATION_REPORT.md)
- [Analysis Script](./WEEK%201%20-%20ProtoVault%20Breach/analyze_leak.py)
- [Challenge README](./WEEK%201%20-%20ProtoVault%20Breach/README.md)

---

### ✅ [Week 2 - Stealer's Shadow](./WEEK%202%20-%20Stealer's%20Shadow)
**Status:** COMPLETED  
**Category:** Incident Response, Malware Analysis, Threat Intelligence  
**Difficulty:** Intermediate

**Scenario:** Data exfiltration incident at Megacorp One (The Etherians). Sophisticated multi-stage attack using blockchain payload delivery, LOLBin abuse, and registry hijacking to steal credentials and sensitive data.

**Key Skills:**
- Sysmon log analysis and Windows forensics
- Blockchain-based payload investigation
- LOLBin (Living Off the Land Binaries) detection
- Email and browser artifact forensics
- C2 infrastructure mapping
- Credential theft analysis
- Advanced social engineering techniques

**Novel Techniques Discovered:**
- Smart contract payload delivery via Ethereum RPC
- Fake CAPTCHA social engineering
- IMEWDBLD.EXE abuse for malware download
- Registry file association hijacking

**Files:**
- [Investigation Report](./WEEK%202%20-%20Stealer's%20Shadow/INVESTIGATION_REPORT.md)
- [Analysis Script](./WEEK%202%20-%20Stealer's%20Shadow/analyze_attack.py)
- [Challenge README](./WEEK%202%20-%20Stealer's%20Shadow/README.md)
- [Sysmon Logs](./WEEK%202%20-%20Stealer's%20Shadow/log.txt)

---

### ✅ [Week 3 - Quantum Conundrum](./WEEK%203%20-%20Quantum%20Conundrum)
**Status:** COMPLETED  
**Category:** Reverse Engineering, Cryptanalysis, Binary Analysis  
**Difficulty:** Hard

**Scenario:** Break Megacorp Quantum's "unbreakable" and "quantum-proof" encryption protecting the Obscuran Key. Reverse-engineer a sophisticated multi-layer cipher, analyze binary code, and decrypt the encrypted vault to extract the hidden flag.

**Key Skills:**
- Binary reverse engineering with Ghidra
- Cryptanalysis and custom cipher breaking
- Algorithm analysis and reconstruction
- Bit manipulation and matrix operations
- Python decryption script development
- Base64 decoding and data parsing
- Security vulnerability assessment

**Novel Techniques Discovered:**
- 7-layer transformation pipeline (Ring rotation, Add/Subtract constants, Cyclic shifts, Quadrant swaps, Bit-pair swap, Variable rotation)
- Weak keystream generation via simple arithmetic
- Hardcoded salt exploitation
- Matrix-based obfuscation techniques

**Files:**
- [Investigation Report](./WEEK%203%20-%20Quantum%20Conundrum/INVESTIGATION_REPORT.md)
- [Decryption Script](./WEEK%203%20-%20Quantum%20Conundrum/solve_decrypt.py)
- [Transformation Guide](./WEEK%203%20-%20Quantum%20Conundrum/Understanding_7_Transformations.md)
- [Challenge README](./WEEK%203%20-%20Quantum%20Conundrum/README.md)

---

### ✅ [Week 4 - Echo Trail](./WEEK%204%20-%20Echo%20Trail)
**Status:** COMPLETED  
**Category:** Incident Response, Cloud Security, Digital Forensics  
**Difficulty:** Intermediate

**Scenario:** Multi-stage attack against Empathreach (NGO-Hub) involving phishing, MFA bypass, Azure cloud exploitation, and database exfiltration. The adversary seeks the Nullform Key metadata hidden deep within NGO-Hub's systems.

**Key Skills:**
- Email forensics and phishing analysis
- Network traffic analysis (PCAP)
- Azure AD log analysis and authentication investigation
- SMTP protocol analysis
- Azure Cloud Shell forensics
- Azure Arc SSH lateral movement detection
- Database exfiltration analysis
- Windows Event Log analysis (Sysmon)
- Multi-source log correlation
- MITRE ATT&CK threat mapping

**Novel Techniques Discovered:**
- Typosquatting domain abuse (mcrosoft.com)
- Azure MFA bypass patterns
- Azure Arc SSH for lateral movement
- Cloud Shell exploitation
- MariaDB mysqldump for data exfiltration

**Files:**
- [Investigation Report](./WEEK%204%20-%20Echo%20Trail/INVESTIGATION_REPORT.md)
- [Analysis Script](./WEEK%204%20-%20Echo%20Trail/analyze_logs.py)
- [Challenge README](./WEEK%204%20-%20Echo%20Trail/README.md)

---

### ✅ [Week 5 - Emerald Anomaly](./WEEK%205%20-%20Emerald%20Anomaly)
**Status:** COMPLETED  
**Category:** Incident Response, Malware Analysis, Network Forensics  
**Difficulty:** Hard

**Scenario:** Supply chain attack against MEGACORPONE through a backdoored Python MCP (Model Context Protocol) server. Sophisticated multi-stage attack using typosquatting, obfuscation, credential exfiltration, and SMTP relay validation to compromise CLIENT14 and steal employee credentials.

**Key Skills:**
- Python malware reverse engineering
- Obfuscation analysis and decoding
- Typosquatting detection and analysis
- Sysmon Event ID 22 (DNS Query) analysis
- PCAP analysis for SMTP authentication
- Base64 credential decoding
- Network IOC extraction
- Multi-stage attack chain reconstruction
- C2 infrastructure mapping

**Novel Techniques Discovered:**
- CRYPTO_SEED character substitution cipher
- GitHub domain typosquatting (avatars.githubuserc**0**ntent.com)
- MCP server supply chain backdoor
- Dual-infrastructure attack (C2 + SMTP relay)
- Azure infrastructure EHLO spoofing
- Keyword-triggered credential exfiltration

**Attack Chain:**
1. Backdoored MCP server deployed on CLIENT14
2. PowerShell commands with "pass"/"securestring" trigger exfiltration
3. Credentials sent to typosquatted domain (100.43.72.21)
4. SMTP relay (79.134.64.179) validates stolen credentials
5. Attacker gains email access for lateral movement

**Files:**
- [Investigation Report](./WEEK%205%20-%20Emerald%20Anomaly/INVESTIGATION_REPORT.md)
- [Analysis Script](./WEEK%205%20-%20Emerald%20Anomaly/analyze_backdoor.ps1)
- [Challenge README](./WEEK%205%20-%20Emerald%20Anomaly/README.md)
- [Backdoor Source](./WEEK%205%20-%20Emerald%20Anomaly/mcp_backdoor_server.py)

---

## 🎯 Learning Objectives

Through these challenges, I'm developing expertise in:

- **Incident Response:** Systematic investigation methodologies
- **Digital Forensics:** Evidence collection and analysis
- **Malware Analysis:** Threat detection and reverse engineering
- **Security Operations:** Monitoring, detection, and response
- **Cloud Security:** AWS and Azure infrastructure security
- **Python Automation:** Security tooling and scripting
- **OSINT Techniques:** Open source intelligence gathering
- **Azure Security:** Azure AD, Azure Arc, Cloud Shell investigation
- **Email Security:** Phishing detection and analysis
- **Network Forensics:** PCAP analysis and traffic inspection
- **Reverse Engineering:** Binary analysis, decompilation, and obfuscation reversal
- **Cryptanalysis:** Breaking custom encryption schemes
- **DNS Security:** Typosquatting detection and analysis
- **Supply Chain Security:** Backdoor detection in legitimate software
- **Credential Theft Analysis:** Exfiltration detection and prevention

---

## 🛠️ Tools & Technologies

- **Programming:** Python, Bash/PowerShell scripting
- **Version Control:** Git forensics
- **Cloud:** AWS (S3, IAM, Secrets Manager), Azure (Azure AD, Azure Arc, Cloud Shell)
- **Cryptography:** Encoding/decoding, cipher analysis, custom algorithm breaking
- **Security:** OWASP practices, security frameworks, MITRE ATT&CK
- **Forensics:** Log analysis, artifact recovery, PCAP analysis, Sysmon
- **Network Analysis:** Wireshark, tcpdump, SMTP protocol analysis
- **Email Analysis:** SMTP protocol analysis, phishing detection
- **Database:** SQL, MySQL/MariaDB forensics
- **Windows:** Sysmon, Event Viewer, Windows Event Logs, PowerShell forensics
- **Reverse Engineering:** Ghidra, Python decompilation, binary analysis, obfuscation reversal
- **Malware Analysis:** Static analysis, dynamic analysis, IOC extraction
- **DNS:** DNS query analysis, typosquatting detection

---

## 📊 Progress Tracker

| Week | Challenge Name | Status | Category | Difficulty |
|------|---------------|--------|----------|------------|
| 1 | ProtoVault Breach | ✅ Completed | Forensics/IR | Beginner |
| 2 | Stealer's Shadow | ✅ Completed | Malware/IR | Intermediate |
| 3 | Quantum Conundrum | ✅ Completed | Reverse Eng/Crypto | Hard |
| 4 | Echo Trail | ✅ Completed | Cloud/IR | Intermediate |
| 5 | Emerald Anomaly | ✅ Completed | Malware/Network | Hard |

---

## 🏆 Achievements

- ✅ Week 1: Complete investigation with all questions answered
- ✅ Week 2: Advanced malware analysis and blockchain-based attack detection
- ✅ Week 3: Reverse-engineered and broke "quantum-proof" encryption system
- ✅ Week 4: Cloud security incident response and Azure exploitation analysis
- ✅ Week 5: Decoded obfuscated backdoor and identified dual-infrastructure attack
- ✅ Identified 30+ critical security vulnerabilities across five challenges
- ✅ Created automated analysis scripts for log parsing and forensics
- ✅ Documented comprehensive remediation steps
- ✅ Discovered novel attack techniques:
  - Blockchain payload delivery (Week 2)
  - LOLBin chaining (Week 2)
  - Azure Arc SSH abuse (Week 4)
  - 7-layer cipher obfuscation (Week 3)
  - CRYPTO_SEED obfuscation (Week 5)
  - GitHub typosquatting (Week 5)
  - MCP supply chain backdoor (Week 5)
- ✅ Demonstrated expertise in multi-cloud environments (AWS, Azure)
- ✅ Successfully performed binary reverse engineering and cryptanalysis
- ✅ Mastered PowerShell-based forensics and log analysis
- ✅ Developed proficiency in Sysmon event analysis
- ✅ Advanced PCAP analysis and SMTP protocol forensics

---

## 📝 Repository Structure

```
echo-response-offsec-challenge/
├── README.md                          # This file
├── WEEK 1 - ProtoVault Breach/
│   ├── README.md                      # Challenge overview
│   ├── INVESTIGATION_REPORT.md        # Detailed forensic analysis
│   └── analyze_leak.py                # Solution script
├── WEEK 2 - Stealer's Shadow/
│   ├── README.md                      # Challenge overview
│   ├── INVESTIGATION_REPORT.md        # Detailed forensic analysis
│   ├── analyze_attack.py              # Solution script
│   └── log.txt                        # Sysmon event logs
├── WEEK 3 - Quantum Conundrum/
│   ├── README.md                      # Challenge overview
│   ├── INVESTIGATION_REPORT.md        # Detailed security assessment
│   ├── solve_decrypt.py               # Decryption script
│   └── Understanding_7_Transformations.md  # Transformation analysis
├── WEEK 4 - Echo Trail/
│   ├── README.md                      # Challenge overview
│   ├── INVESTIGATION_REPORT.md        # Detailed forensic analysis
│   └── analyze_logs.py                # Azure log parser script
├── WEEK 5 - Emerald Anomaly/
│   ├── README.md                      # Challenge overview
│   ├── INVESTIGATION_REPORT.md        # Detailed forensic analysis
│   ├── analyze_backdoor.ps1           # PowerShell decoder script
│   └── mcp_backdoor_server.py         # Backdoor source code
└── ...
```

---

## 🚀 Quick Start

To explore the solutions:

1. **Clone this repository:**
   ```bash
   git clone https://github.com/umair-aziz025/echo-response-offsec-challenge.git
   cd echo-response-offsec-challenge
   ```

2. **Navigate to a specific week:**
   ```bash
   cd "WEEK 1 - ProtoVault Breach"
   # or
   cd "WEEK 2 - Stealer's Shadow"
   # or
   cd "WEEK 3 - Quantum Conundrum"
   # or
   cd "WEEK 4 - Echo Trail"
   # or
   cd "WEEK 5 - Emerald Anomaly"
   ```

3. **Read the challenge writeup:**
   - Check `README.md` for challenge overview
   - Review `INVESTIGATION_REPORT.md` for detailed analysis

4. **Run the solution scripts (if applicable):**
   ```bash
   # Python scripts
   python analyze_leak.py
   
   # PowerShell scripts
   .\analyze_backdoor.ps1
   ```

---

## 📚 Learning Resources

- [OffSec Proving Grounds](https://www.offsec.com/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [AWS Security Best Practices](https://aws.amazon.com/security/best-practices/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [MITRE ATT&CK](https://attack.mitre.org/)

---

## 🤝 Connect

**Umair Aziz**  
- GitHub: [@umair-aziz025](https://github.com/umair-aziz025)
- Repository: [echo-response-offsec-challenge](https://github.com/umair-aziz025/echo-response-offsec-challenge)

---

## 📄 License

This repository is for educational purposes only. Challenge scenarios are property of OffSec. Solution writeups and scripts are my own work.

---

## ⭐ Star This Repo

If you find these solutions helpful, please consider giving this repository a star! It helps others discover these resources.

---

**Last Updated:** November 5, 2025

---

*"Will you uncover the truth before the balance collapses?"*
