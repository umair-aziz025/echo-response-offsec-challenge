# Week 8 - Last Ascent 🏔️⚡

## Challenge Overview

**Challenge Name:** Last Ascent  
**Category:** ICS/SCADA Forensics, Incident Response, Privilege Escalation  
**Difficulty:** Insane  
**Status:** ✅ COMPLETED

---

## 🎯 Scenario

At the culmination of the Proving Grounds: The Gauntlet event, we face the **Last Ascent** - a critical incident response scenario targeting Megacorp One's Energy Systems Division. Autonomous wind turbines have been manipulated and taken out of MegaCorp One's control.

The power stabilization layer has been compromised, and the **Codex Circuit's** protective perimeter is now vulnerable. The threat actor has achieved the unthinkable - complete control over critical infrastructure through a sophisticated multi-stage attack.

---

## 🔍 Challenge Questions

### Q1: Powergrid Shutdown Analysis
**Question:** Identify how the Powergrid was shut down. State the technical status of the turbines after the attack (flags, control bits, output states) and provide the IP address of the system from which the attack was performed.

**Answer:**
- Turbine Status: Turbines forced into STOP state, `run=0`, `speed register=0`, `lockout bit=1`
- Attacker IP: `192.168.1.253`

---

### Q2: Attacker Knowledge Source
**Question:** From where did the attacker gain the knowledge necessary to perform this attack? If from a file, include the complete filename and its SHA-256 hash. If from a website, provide the full URL beginning with "https://".

**Answer:**
- File: `WT-PLC_Turbine_Control_Manual.pdf`
- SHA-256: `635598615d4a9823b36163796fdc3c45702280097bad8df23fc1b8c39c9d7101`

---

### Q3: RESOURCES Machine Compromise
**Question:** How was the attacker able to compromise the RESOURCES machine? Provide the name of the exploited program and the SHA-256 hash of the malicious file used in the compromise.

**Answer:**
- Exploited Program: `MonitorTool.exe`
- Malicious File SHA-256: `E6E4D51009F5EFE2FA1FA112C3FDEEA381AB06C4609945B056763B401C4F3333`

---

### Q4: Pivot Information
**Question:** What two pieces of information did the attacker obtain on the RESOURCES system that enabled them to pivot to the next system in the attack path?

**Answer:**
- SSH Username: `vyos`
- SSH Private Key: `router2.privkey` (for host 192.168.1.253)

---

### Q5: Credential Harvesting
**Question:** Enter the username and password of the user that performed the attack in question 3, and the SHA-256 hash of the program responsible for capturing or collecting these login credentials.

**Answer:**
- Username: `carmen.santos` (or MEGACORPONE\carmen.santos)
- Password: `Qwerty09!`
- Program: `ssp.dll` (Security Support Provider)
- SHA-256: `566DEE9A89CE772E640CDB1126480F83EE048CEA4B7661A9427AF42A9FAB8B46`

---

### Q6: Initial Access Vector
**Question:** Identify and analyze the initial access vector. Provide the domain (without suffixes or prefixes) where the payload for initial access was loaded from and the program (including its version) that was exploited or targeted.

**Answer:**
- Domain: `microsoft-login` (full domain: microsoft-login.com)
- Exploited Program: Chrome version `137.0.7151.56`

---

### Q7: Privilege Escalation
**Question:** How did the attacker elevate their privileges on CLIENT8? Provide the name and SHA-256 hash of the program responsible for privilege escalation, and the CVE related to the vulnerability used.

**Answer:**
- Program: `BitLockerDeviceEncrypton.exe` (note the typo - masquerading technique!)
- SHA-256: `20DA751A1B158693C04A392FD499898B055E059EC273841E5026C15E691B6AEA`
- CVE: `CVE-2024-35250`

---

## 🔗 Complete Attack Chain

```
Phishing (microsoft-login.com)
         │
         ▼
   Initial Access (Chrome 137.0.7151.56)
         │
         ▼
   Privilege Escalation (CVE-2024-35250)
   BitLockerDeviceEncrypton.exe → ks.sys/MSKSSRV
         │
         ▼
   Credential Harvesting (ssp.dll → LSASS)
   Captured: carmen.santos:Qwerty09!
         │
         ▼
   Lateral Movement (SSH via router2.privkey)
   CLIENT8 → Router2 (192.168.1.253)
         │
         ▼
   SCADA Compromise (MonitorTool.exe exploit)
   Access to RESOURCES server
         │
         ▼
   ICS Manipulation (Modbus commands)
   PLCs forced into 24-hour lockout
         │
         ▼
   💥 TURBINES SHUTDOWN 💥
```

---

## 🛠️ Key Skills Demonstrated

- **ICS/SCADA Forensics** - Modbus protocol analysis, PLC manipulation detection
- **Windows Forensics** - Sysmon log analysis, registry examination
- **Privilege Escalation Analysis** - CVE-2024-35250 kernel exploitation
- **Credential Theft Detection** - SSP DLL injection into LSASS
- **Browser Forensics** - Chrome history and artifact analysis
- **Network Forensics** - SSH pivot detection, Modbus traffic analysis
- **Binary Analysis** - Masquerading technique detection
- **MITRE ATT&CK Mapping** - Comprehensive technique identification

---

## 📁 Files

| File | Description |
|------|-------------|
| [INVESTIGATION_REPORT.md](./INVESTIGATION_REPORT.md) | Complete forensic investigation report |
| [README.md](./README.md) | This file - challenge overview |

---

## 🏆 Key Findings

### Novel Techniques Discovered
- **Typo-squatting in filenames** - BitLockerDeviceEncrypton.exe (missing 'i')
- **CVE-2024-35250** - Kernel Streaming driver vulnerability exploitation
- **SSP credential harvesting** - Malicious DLL injection into LSASS
- **IT-OT pivot attack** - From workstation to SCADA through SSH
- **Modbus protocol abuse** - Triggering protective lockout intentionally

### Indicators of Compromise (IOCs)

| Type | Value |
|------|-------|
| Malicious Domain | `microsoft-login.com` |
| CVE | `CVE-2024-35250` |
| Attacker IP | `192.168.1.253` |
| ssp.dll Hash | `566DEE9A89CE772E640CDB1126480F83EE048CEA4B7661A9427AF42A9FAB8B46` |
| Exploit Hash | `20DA751A1B158693C04A392FD499898B055E059EC273841E5026C15E691B6AEA` |

---

## 📚 References

- [CVE-2024-35250 - NIST NVD](https://nvd.nist.gov/vuln/detail/CVE-2024-35250)
- [MITRE ATT&CK - T1068 Exploitation for Privilege Escalation](https://attack.mitre.org/techniques/T1068/)
- [MITRE ATT&CK - T1547.005 Security Support Provider](https://attack.mitre.org/techniques/T1547/005/)

---

**Challenge Completed:** November 26, 2025  
**Investigator:** MR. Umair
