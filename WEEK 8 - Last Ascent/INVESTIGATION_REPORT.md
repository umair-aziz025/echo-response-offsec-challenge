# Week 8 - Last Ascent: ICS/SCADA Incident Response Investigation

## Wind Turbine SCADA Infrastructure Forensic Analysis

**Challenge:** Last Ascent (Week 8)  
**Investigator:** MR. Umair  
**Date:** November 26, 2025  
**Target:** Megacorp One Energy Systems Division - Wind Farm SCADA Infrastructure  
**Impact:** Power stabilization layer compromised, Codex Circuit protective perimeter vulnerable

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Challenge Overview](#challenge-overview)
3. [Q1: Powergrid Shutdown Analysis](#question-1-powergrid-shutdown-analysis)
4. [Q2: Attacker Knowledge Source](#question-2-attacker-knowledge-source)
5. [Q3: RESOURCES Machine Compromise](#question-3-resources-machine-compromise)
6. [Q4: Pivot Information](#question-4-pivot-information)
7. [Q5: Credential Harvesting Analysis](#question-5-credential-harvesting-analysis)
8. [Q6: Phishing Domain & Browser Analysis](#question-6-phishing-domain--browser-analysis)
9. [Q7: Privilege Escalation Analysis](#question-7-privilege-escalation-analysis)
10. [Complete Attack Chain](#complete-attack-chain)
11. [Network Topology](#network-topology)
12. [Evidence Chain - Linking CVE-2024-35250](#evidence-chain---linking-cve-2024-35250)
13. [Indicators of Compromise](#indicators-of-compromise-iocs)
14. [MITRE ATT&CK Mapping](#mitre-attck-mapping)
15. [Recommendations](#recommendations)

---

## Executive Summary

This report documents the comprehensive forensic analysis of a sophisticated multi-stage cyberattack against Megacorp One's Wind Farm SCADA infrastructure. The threat actor employed a coordinated attack chain spanning:

1. **Initial Access** - Phishing attack via fake Microsoft login domain
2. **Privilege Escalation** - CVE-2024-35250 kernel vulnerability exploitation
3. **Credential Harvesting** - SSP DLL injection to capture plaintext credentials
4. **Lateral Movement** - SSH pivot using stolen credentials and private keys
5. **ICS/SCADA Manipulation** - Modbus commands to shutdown wind turbines

The attack resulted in autonomous wind turbines being forced into a 24-hour lockout state, compromising the power stabilization layer and exposing the Codex Circuit protective perimeter.

---

## Challenge Overview

**Incident:** Autonomous wind turbines manipulated and taken out of MegaCorp One's control  
**Affected Systems:** CLIENT8 workstation, RESOURCES server, Router2, PLCs (4 turbines)  
**Attack Duration:** Approximately 4-5 hours from initial access to turbine shutdown

---

## Question 1: Powergrid Shutdown Analysis

### Question
> Identify how the Powergrid was shut down. State the technical status of the turbines after the attack (flags, control bits, output states) and provide the IP address of the system from which the attack was performed.

### Answer
| Field | Value |
|-------|-------|
| **Turbine Status** | Turbines forced into STOP state, run=0, speed register=0, lockout bit=1 |
| **Attacker IP** | `192.168.1.253` |

### Evidence Collection

#### 1.1 Identifying the Attacker IP Address

**Source File:** `RESOURCES\System32\winevt\Logs\Microsoft-Windows-Sysmon%4Operational.evtx`

**Method:** Parsed Sysmon Event ID 3 (Network Connection) logs using python-evtx

```python
import Evtx.Evtx as evtx

evtx_path = r'RESOURCES\System32\winevt\Logs\Microsoft-Windows-Sysmon%4Operational.evtx'

with evtx.Evtx(evtx_path) as log:
    for record in log.records():
        xml = record.xml()
        if '192.168.1.253' in xml:
            print(xml[:3000])
```

**Key Evidence Found:**
```xml
<Event>
  <System>
    <EventID>3</EventID>  <!-- Network Connection -->
    <TimeCreated SystemTime="2025-10-30 08:59:58.343"/>
    <Computer>RESOURCES.scada.megacorpone.com</Computer>
  </System>
  <EventData>
    <Data Name="Protocol">tcp</Data>
    <Data Name="SourceIp">192.168.1.2</Data>
    <Data Name="DestinationIp">192.168.1.253</Data>
    <Data Name="DestinationPort">22</Data>
  </EventData>
</Event>
```

#### 1.2 Understanding Turbine Technical Status

**Source File:** `RESOURCES\Shares\SCADA\docs\WT-PLC_Turbine_Control_Manual.pdf`

**Modbus Register Map from Manual:**

| Register Type | Address | Description |
|--------------|---------|-------------|
| Holding Register | 0 | Rotor speed setpoint (0–10000 = 0–100%) |
| Discrete Input | 2 | Turbine stopped (speed = 0%) |
| Discrete Input | 3 | Lockout active (1 = 24-hour protection mode engaged) |

**Attack Mechanism:**
The attacker triggered the protective lockout by making rapid consecutive speed commands (>20% change within 2 minutes), which:
1. Automatically engages the 24-hour lockout
2. Forces speed to 0% (`run=0`, `speed register=0`)
3. Sets lockout bit to 1 (`lockout bit=1`)

---

## Question 2: Attacker Knowledge Source

### Question
> From where did the attacker gain the knowledge necessary to perform this attack? If from a file, include the complete filename and its SHA-256 hash.

### Answer
| Field | Value |
|-------|-------|
| **Filename** | `WT-PLC_Turbine_Control_Manual.pdf` |
| **Location** | `RESOURCES\Shares\SCADA\docs\` |
| **SHA-256** | `635598615d4a9823b36163796fdc3c45702280097bad8df23fc1b8c39c9d7101` |

### Evidence Collection

**Hash Verification:**
```powershell
certutil -hashfile "RESOURCES\Shares\SCADA\docs\WT-PLC_Turbine_Control_Manual.pdf" SHA256
```

**Output:**
```
SHA256 hash: 635598615d4a9823b36163796fdc3c45702280097bad8df23fc1b8c39c9d7101
```

**Key Information in Manual:**
- Complete Modbus Register Map (coils, discrete inputs, holding registers)
- Operating procedures with Python code examples
- Lockout trigger conditions (>20% change in 2 minutes)
- Modbus TCP ports (1502-1505 for turbines)

---

## Question 3: RESOURCES Machine Compromise

### Question
> How was the attacker able to compromise the RESOURCES machine? Provide the name of the exploited program and the SHA-256 hash of the malicious file used in the compromise.

### Answer
| Field | Value |
|-------|-------|
| **Exploited Program** | `MonitorTool.exe` |
| **Malicious File SHA-256** | `E6E4D51009F5EFE2FA1FA112C3FDEEA381AB06C4609945B056763B401C4F3333` |

### Evidence Collection

**Source Files:**
- `RESOURCES\Shares\Monitoring\MonitorTool.xml` (Scheduled Task)
- `RESOURCES\Shares\Monitoring\monitor.log` (Execution Log)

**Scheduled Task Analysis:**
```xml
<Task>
  <Triggers>
    <TimeTrigger>
      <Repetition>
        <Interval>PT10M</Interval>  <!-- Runs every 10 minutes -->
      </Repetition>
    </TimeTrigger>
  </Triggers>
  <Actions>
    <Exec>
      <Command>C:\Shares\Monitoring\MonitorTool.exe</Command>
    </Exec>
  </Actions>
</Task>
```

**Attack Timeline from Logs:**
```
C:\Shares\Monitoring\CheckHealth.exe not found
Backing up PCAPs off of router2
...
Executing C:\Shares\Monitoring\CheckHealth.exe  <-- Malicious file executed!
```

**Attack Mechanism:** Binary Planting / DLL Search Order Hijacking
- MonitorTool.exe runs as a scheduled task every 10 minutes
- Attacker placed malicious CheckHealth.exe in the Monitoring share
- MonitorTool.exe executed the malware with elevated privileges

---

## Question 4: Pivot Information

### Question
> What two pieces of information did the attacker obtain on the RESOURCES system that enabled them to pivot to the next system in the attack path?

### Answer
| Field | Value |
|-------|-------|
| **SSH Username** | `vyos` |
| **SSH Private Key** | `router2.privkey` (for host 192.168.1.253) |

### Evidence Collection

**Source File:** `CLIENT8\amara.okafor\.ssh\router2.privkey`

```powershell
Get-ChildItem "CLIENT8\amara.okafor\.ssh" -Recurse
# Output: router2.privkey
```

**Key Metadata:**
```
-----BEGIN OPENSSH PRIVATE KEY-----
nukingdragons@blackarch  <-- Attacker attribution
-----END OPENSSH PRIVATE KEY-----
```

---

## Question 5: Credential Harvesting Analysis

### Question
> How did the attacker harvest credentials on CLIENT8? Enter the SHA-256 hash of the tool or technique responsible for the credential harvesting.

### Answer
| Field | Value |
|-------|-------|
| **Tool** | `ssp.dll` (Security Support Provider) |
| **Location** | `CLIENT8\System32\ssp.dll` |
| **SHA-256** | `566DEE9A89CE772E640CDB1126480F83EE048CEA4B7661A9427AF42A9FAB8B46` |

### Investigation Process

#### Understanding SSP Credential Harvesting

Security Support Provider (SSP) is a Windows authentication mechanism. Attackers can register a malicious SSP DLL that gets loaded by LSASS (Local Security Authority Subsystem Service). Once loaded, the malicious SSP intercepts all authentication attempts and captures plaintext credentials.

#### File Timestamp Evidence

```powershell
Get-ChildItem "CLIENT8\System32" | Where-Object { $_.Name -eq "ssp.dll" }
```

**Output:**
```
Name     Length  LastWriteTime        
----     ------  -------------        
ssp.dll  14848   10/30/2025 4:49:20 AM  <-- Attack timestamp!
```

#### Hash Verification

```powershell
$hash = (Get-FileHash "CLIENT8\System32\ssp.dll" -Algorithm SHA256).Hash
# Output: 566DEE9A89CE772E640CDB1126480F83EE048CEA4B7661A9427AF42A9FAB8B46
```

**Captured Credentials:**
- Username: `carmen.santos`
- Password: `Qwerty09!`
- These credentials were used to pivot to the RESOURCES server

---

## Question 6: Phishing Domain & Browser Analysis

### Question
> What is the domain of the phishing website and the user's browser name along with its version accessed by Amara on CLIENT8?

### Answer
| Field | Value |
|-------|-------|
| **Phishing Domain** | `microsoft-login.com` |
| **Browser** | Google Chrome |
| **Version** | `137.0.7151.56` |

### Investigation Process

#### Extracting Chrome Version

```powershell
$versionPath = "CLIENT8\amara.okafor\AppData\Local\Google\Chrome\User Data\Last Version"
Get-Content $versionPath
# Output: 137.0.7151.56
```

#### Analyzing Chrome History

```powershell
$historyPath = "CLIENT8\amara.okafor\AppData\Local\Google\Chrome\User Data\Default\History"
[System.Text.Encoding]::UTF8.GetString([System.IO.File]::ReadAllBytes($historyPath)) | 
    Select-String -Pattern "microsoft-login" -AllMatches
```

**Output:** Multiple references to `microsoft-login` domain found

### Phishing Attack Analysis

- **Malicious Domain:** `microsoft-login.com` - Typosquatting domain mimicking Microsoft
- **Legitimate Domain:** `login.microsoftonline.com` or `login.microsoft.com`
- **Attack Flow:** User received phishing email → Clicked link → Visited fake login → Credentials harvested

---

## Question 7: Privilege Escalation Analysis

### Question
> How did the attacker elevate their privileges on CLIENT8? Enter the name and SHA-256 hash of the program responsible for the elevation of privileges. What is the CVE related to the vulnerability that was used to escalate their privileges?

### Answer
| Field | Value |
|-------|-------|
| **Program Name** | `BitLockerDeviceEncrypton.exe` |
| **Location** | `CLIENT8\System32\BitLockerDeviceEncrypton.exe` |
| **SHA-256** | `20DA751A1B158693C04A392FD499898B055E059EC273841E5026C15E691B6AEA` |
| **CVE** | `CVE-2024-35250` |

### Investigation Process

#### File Discovery - Masquerading Technique

```powershell
Get-ChildItem "CLIENT8\System32" | Where-Object { $_.Name -like "*BitLocker*" }
```

**Output:**
```
Name                          Length  LastWriteTime        
----                          ------  -------------        
BitLockerDeviceEncryption.exe 184320  5/7/2022 12:39:28 PM   <-- Legitimate
BitLockerDeviceEncrypton.exe  29184   10/30/2025 4:43:50 AM  <-- MALICIOUS (typo!)
```

**Key Observation:** The malicious filename has a TYPO - "Encrypton" instead of "Encryption"!
This is a classic masquerading technique to blend in with legitimate system files.

#### Timeline Evidence

| Timestamp | Event |
|-----------|-------|
| 04:43:50 AM | BitLockerDeviceEncrypton.exe placed in System32 |
| 04:43-04:49 | CVE-2024-35250 exploitation occurs |
| 04:49:20 AM | ssp.dll placed in System32 (requires SYSTEM privileges) |

**The 6-minute gap proves the privilege escalation succeeded** - writing to System32 requires SYSTEM privileges!

#### CVE-2024-35250 Technical Details

| Field | Value |
|-------|-------|
| **Vulnerability** | Windows Kernel-Mode Driver Elevation of Privilege |
| **Component** | ks.sys (Kernel Streaming Service / MSKSSRV) |
| **Attack Method** | Improper IOCTL handling in kernel driver |
| **CVSS Score** | 7.8 (High) |
| **Result** | Local privilege escalation from user to SYSTEM |

---

## Complete Attack Chain

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                         COMPLETE ATTACK TIMELINE                                ║
╠════════════════════════════════════════════════════════════════════════════════╣
║                                                                                 ║
║  PHASE 1: INITIAL ACCESS                                                        ║
║  ├─> Phishing email sent to amara.okafor@megacorpone.com                       ║
║  ├─> User visits microsoft-login.com (fake Microsoft portal)                   ║
║  ├─> Browser: Chrome 137.0.7151.56                                             ║
║  └─> Credentials harvested via fake login page                                 ║
║                                                                                 ║
║  PHASE 2: PRIVILEGE ESCALATION (10/30/2025 ~04:43 AM)                          ║
║  ├─> Attacker deploys BitLockerDeviceEncrypton.exe (note typo)                 ║
║  ├─> Exploits CVE-2024-35250 (ks.sys/MSKSSRV vulnerability)                    ║
║  └─> Gains NT AUTHORITY\SYSTEM privileges                                      ║
║                                                                                 ║
║  PHASE 3: CREDENTIAL HARVESTING (10/30/2025 ~04:49 AM)                         ║
║  ├─> Deploys ssp.dll to System32                                               ║
║  ├─> Registers malicious SSP with LSASS                                        ║
║  ├─> Intercepts all authentication attempts                                    ║
║  └─> Captures carmen.santos:Qwerty09!                                          ║
║                                                                                 ║
║  PHASE 4: LATERAL MOVEMENT                                                      ║
║  ├─> SSH pivot using vyos credentials + router2.privkey                        ║
║  ├─> Access to RESOURCES server via MonitorTool.exe exploit                    ║
║  └─> Pivot through router2 (192.168.1.253) to SCADA network                    ║
║                                                                                 ║
║  PHASE 5: ICS/SCADA MANIPULATION                                                ║
║  ├─> Obtained turbine control knowledge from PDF manual                        ║
║  ├─> Sent Modbus commands to PLCs (192.168.2.1-192.168.2.4)                    ║
║  └─> Triggered 24-hour lockout on all wind turbines                            ║
║                                                                                 ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

---

## Network Topology

```
┌─────────────────────────────────────────────────────────────────┐
│                    Corporate Network                             │
│  ┌──────────────┐                    ┌──────────────┐           │
│  │   CLIENT8    │                    │  RESOURCES   │           │
│  │ 192.168.1.x  │                    │ 192.168.1.2  │           │
│  │ (Workstation)│                    │(SCADA Server)│           │
│  └──────────────┘                    └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ SSH (port 22)
                              ▼
                    ┌──────────────┐
                    │   Router2    │
                    │192.168.1.253 │
                    │   (VyOS)     │
                    └──────────────┘
                              │
                              │ Modbus TCP
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SCADA Network                               │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐                │
│  │ PLC 1  │  │ PLC 2  │  │ PLC 3  │  │ PLC 4  │                │
│  │.2.1:1502│  │.2.2:1503│  │.2.3:1504│  │.2.4:1505│               │
│  └────────┘  └────────┘  └────────┘  └────────┘                │
│       │           │           │           │                      │
│       ▼           ▼           ▼           ▼                      │
│   Turbine 1   Turbine 2   Turbine 3   Turbine 4                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Evidence Chain - Linking CVE-2024-35250

### How Do We Know BitLockerDeviceEncrypton.exe and CVE-2024-35250 Are Connected?

#### 1. Sysmon Evidence - MSKSSRV Driver (CVE-2024-35250 Target)

From the 78MB Sysmon Operational logs:

```xml
<EventData>
  <Data Name='ImageLoaded'>C:\Windows\System32\drivers\mskssrv.sys</Data>
  <Data Name='Hashes'>SHA256=6B712ADDF7C6B583F23F518BF35F7ECBBFA632F14E29EBE2A8E38043B1269E74</Data>
  <Data Name='Signed'>true</Data>
  <Data Name='Signature'>Microsoft Windows</Data>
</EventData>
```

**10 references to mskssrv.sys found** - This is the exact driver targeted by CVE-2024-35250!

#### 2. Registry Evidence - Kernel Streaming Driver Stack

```
STACKID: \driver\ksthunk,\driver\mskssrv,\driver\swenum
Service: mskssrv
DriverName: mskssrv.sys
```

#### 3. Binary Analysis - Kernel Exploitation APIs

Strings extracted from BitLockerDeviceEncrypton.exe:
- `K32EnumDeviceDrivers` - Driver enumeration API
- `NtQuerySystemInformation` - System information query
- `GetSystemTimeAsFileTime` - Timing for exploitation
- `KERNEL32.dll` - Kernel operations

#### 4. Timeline Correlation - Proof of Success

| Time | Event | Significance |
|------|-------|--------------|
| 04:43:50 | BitLockerDeviceEncrypton.exe created | Exploit tool deployed |
| 04:43-04:49 | 6-minute window | Exploitation occurs |
| 04:49:20 | ssp.dll created in System32 | REQUIRES SYSTEM privileges |

**The fact that ssp.dll was written to System32 PROVES the privilege escalation succeeded!**

---

## Indicators of Compromise (IOCs)

### File Hashes (SHA-256)

| Hash | Filename | Description |
|------|----------|-------------|
| `566DEE9A89CE772E640CDB1126480F83EE048CEA4B7661A9427AF42A9FAB8B46` | ssp.dll | SSP Credential Harvester |
| `20DA751A1B158693C04A392FD499898B055E059EC273841E5026C15E691B6AEA` | BitLockerDeviceEncrypton.exe | CVE-2024-35250 Exploit |
| `635598615d4a9823b36163796fdc3c45702280097bad8df23fc1b8c39c9d7101` | WT-PLC_Turbine_Control_Manual.pdf | Knowledge Source |
| `E6E4D51009F5EFE2FA1FA112C3FDEEA381AB06C4609945B056763B401C4F3333` | MonitorTool.exe | Exploited Binary |

### Malicious Domains

| Domain | Type | Purpose |
|--------|------|---------|
| `microsoft-login.com` | Phishing | Credential harvesting via fake Microsoft login |

### Network Indicators

| IP Address | Role | Protocol |
|------------|------|----------|
| `192.168.1.253` | Attacker Pivot (Router2) | SSH/Modbus |
| `192.168.2.1-192.168.2.4` | Target PLCs | Modbus TCP |

### File Paths (Attacker Artifacts)

```
C:\Windows\System32\ssp.dll
C:\Windows\System32\BitLockerDeviceEncrypton.exe
CLIENT8\amara.okafor\.ssh\router2.privkey
```

### CVE References

| CVE ID | Description | Severity |
|--------|-------------|----------|
| CVE-2024-35250 | Windows Kernel-Mode Driver EoP (ks.sys) | High (7.8) |

---

## MITRE ATT&CK Mapping

| Technique ID | Technique Name | Description |
|--------------|----------------|-------------|
| T1566.002 | Phishing: Spearphishing Link | Fake Microsoft login page |
| T1003.001 | OS Credential Dumping: LSASS Memory | SSP credential harvesting |
| T1547.005 | Boot or Logon Autostart: SSP | Malicious SSP DLL registration |
| T1068 | Exploitation for Privilege Escalation | CVE-2024-35250 exploit |
| T1036.005 | Masquerading: Match Legitimate Name | BitLockerDeviceEncrypton.exe (typo) |
| T1021.004 | Remote Services: SSH | Pivot via router2.privkey |
| T1574.001 | Hijack Execution Flow: DLL Search Order | MonitorTool.exe exploitation |
| T1485 | Data Destruction | Turbine lockout (ICS impact) |

---

## Recommendations

### Immediate Actions
1. **Isolate CLIENT8** from the network
2. **Reset all credentials** for amara.okafor and carmen.santos
3. **Block domain** microsoft-login.com at network perimeter
4. **Deploy IOC signatures** to EDR/SIEM
5. **Manual turbine restart** after 24-hour lockout expires

### Long-term Mitigations
1. **Patch CVE-2024-35250** on all Windows systems
2. **Enable Credential Guard** to protect LSASS
3. **Implement phishing-resistant MFA** (FIDO2/WebAuthn)
4. **Network segmentation** between IT and OT networks
5. **Monitor SSP registry keys** for unauthorized modifications
6. **ICS-specific monitoring** for Modbus protocol anomalies
7. **Remove unnecessary documentation** from SCADA shares

---

## Tools Used

| Tool | Purpose |
|------|---------|
| `python-evtx` | Parse Windows Event Logs (.evtx) |
| `PyMuPDF (fitz)` | Extract text from PDF documents |
| `certutil` | Calculate SHA-256 file hashes |
| `PowerShell` | File system enumeration and analysis |
| `Sysmon` | Process and network monitoring analysis |
| `SQLite` | Chrome History database analysis |

---

## Conclusion

The attacker employed a sophisticated multi-stage attack leveraging:

1. **Social Engineering** via typosquatting phishing domain
2. **Zero-Day Exploitation** using CVE-2024-35250 for kernel-level access
3. **Credential Theft** through SSP injection into LSASS
4. **Operational Technology Manipulation** via Modbus protocol abuse

This attack chain demonstrates the critical importance of defense-in-depth strategies, particularly in ICS/SCADA environments where IT-OT convergence creates expanded attack surfaces. The attacker's ability to pivot from a single phished workstation to complete turbine control highlights the need for robust network segmentation and protocol-aware monitoring.

---

**Date:** November 26, 2025  
**Investigator:** MR. Umair  
**Case:** OffSec Echo Response - Week 8: Last Ascent

---

> *"The wind cannot be caught, but it can be understood. In cybersecurity, as in nature, knowledge of the system's flow reveals both its power and its vulnerabilities."*
