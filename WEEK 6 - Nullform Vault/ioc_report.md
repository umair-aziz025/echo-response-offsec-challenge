Nullform Vault - Indicators of Compromise (IOCs)
Generated: 2025-11-11 21:16:07

Network IOCs
============
IP: 203.0.113.42 (C2 server)
URL: http://203.0.113.42:8000/ (exfiltration endpoint)
Port: 8000/TCP (HTTP)

File IOCs
=========
File: Obfuscated_Intent.exe (packed, 18432 bytes)
File: unpacked.exe (39424 bytes)
Packer: UPX

Target Extensions (XOR key 0x7a):
.pdf .doc .docx .xls .msg

Process IOCs
============
Process: Obfuscated_Intent.exe
Process: powershell.exe (spawned for exfiltration)

API Calls:
IsDebuggerPresent (anti-debugging)
CheckRemoteDebuggerPresent (anti-debugging)
IcmpSendEcho (ICMP with w00t payload)
FindFirstFileW, FindNextFileW (filesystem scan)
_wsystem (PowerShell execution)

DLLs: WS2_32.dll, IPHLPAPI.DLL

MITRE ATT&CK:
T1027 (Packing), T1622 (Anti-debug), T1140 (Decode)
T1083 (File Discovery), T1005 (Data Collection)
T1041 (Exfiltration), T1059.001 (PowerShell)
T1071.001 (HTTP), T1095 (ICMP)

Investigation Status: COMPLETE

