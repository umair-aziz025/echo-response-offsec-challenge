import pefile
import struct
import re

# Load the PE file
pe = pefile.PE('Obfuscated_Intent.exe')

print("=" * 80)
print("PE ANALYSIS - STATIC ANALYSIS")
print("=" * 80)

# Get entry point
entry_point = pe.OPTIONAL_HEADER.AddressOfEntryPoint
image_base = pe.OPTIONAL_HEADER.ImageBase
print(f"\n[+] Entry Point RVA: 0x{entry_point:X}")
print(f"[+] Image Base: 0x{image_base:X}")

# Get code section
code_section = None
for section in pe.sections:
    name = section.Name.decode().strip('\x00')
    print(f"\n[+] Section: {name}")
    print(f"    Virtual Address: 0x{section.VirtualAddress:X}")
    print(f"    Virtual Size: 0x{section.Misc_VirtualSize:X}")
    print(f"    Raw Size: 0x{section.SizeOfRawData:X}")
    
    if name == '.text':
        code_section = section

# Import Analysis
print("\n" + "=" * 80)
print("[+] IMPORTS ANALYSIS")
print("=" * 80)

networking_dlls = []
if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        dll_name = entry.dll.decode()
        print(f"\n[DLL] {dll_name}")
        
        # Check for networking DLLs
        if any(net in dll_name.upper() for net in ['WS2_32', 'WININET', 'URLMON', 'IPHLPAPI', 'WINHTTP']):
            networking_dlls.append(dll_name)
        
        for imp in entry.imports:
            if imp.name:
                func_name = imp.name.decode()
                print(f"    - {func_name}")
                
                # Highlight important functions
                important_funcs = ['IcmpSendEcho', 'inet_addr', 'socket', 'connect', 
                                 'send', 'recv', 'LoadLibraryA', 'GetProcAddress',
                                 'VirtualProtect', 'CreateProcess', 'WinExec', 'system',
                                 'ShellExecute', 'URLDownloadToFile']
                
                if func_name in important_funcs:
                    print(f"        *** IMPORTANT: {func_name} ***")

print(f"\n[+] Networking DLLs found: {networking_dlls}")

# Search for hardcoded data in the data section
print("\n" + "=" * 80)
print("[+] SEARCHING FOR HARDCODED DATA")
print("=" * 80)

# Get .data or .rdata section
data_sections = [s for s in pe.sections if b'.data' in s.Name or b'.rdata' in s.Name]

for section in data_sections:
    name = section.Name.decode().strip('\x00')
    print(f"\n[Section: {name}]")
    
    # Get section data
    section_data = section.get_data()
    
    # Look for IP addresses
    for i in range(len(section_data) - 15):
        chunk = section_data[i:i+15]
        try:
            s = chunk.decode('ascii', errors='ignore')
            # Match IP pattern
            ip_match = re.match(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})', s)
            if ip_match:
                octets = [int(x) for x in ip_match.groups()]
                if all(0 <= x <= 255 for x in octets):
                    ip = '.'.join(map(str, octets))
                    offset = section.VirtualAddress + i
                    print(f"    [RVA 0x{offset:08X}] IP Address: {ip}")
        except:
            pass
    
    # Look for URLs/strings
    ascii_pattern = b'[\x20-\x7E]{8,}'
    for match in re.finditer(ascii_pattern, section_data):
        s = match.group().decode('ascii', errors='ignore')
        
        # Check if it contains interesting keywords
        if any(kw in s.lower() for kw in ['http', 'www', 'upload', 'download', '.txt', '.pdf', '.doc']):
            offset = section.VirtualAddress + match.start()
            print(f"    [RVA 0x{offset:08X}] String: {s[:80]}")

# Look in all sections for strings
print("\n" + "=" * 80)
print("[+] SCANNING ALL SECTIONS FOR HARDCODED STRINGS")
print("=" * 80)

all_data = bytearray()
for section in pe.sections:
    all_data.extend(section.get_data())

# Look for IP addresses
print("\n[+] IP Addresses:")
for i in range(len(all_data) - 15):
    chunk = all_data[i:i+15]
    try:
        s = chunk.decode('ascii', errors='ignore')
        ip_match = re.match(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\x00', s)
        if ip_match:
            octets = [int(x) for x in ip_match.groups()]
            if all(0 <= x <= 255 for x in octets):
                ip = '.'.join(map(str, octets))
                print(f"    Offset 0x{i:08X}: {ip}")
    except:
        pass

# Look for file extensions
print("\n[+] File Extension Patterns:")
ext_patterns = [b'*.txt', b'*.doc', b'*.pdf', b'*.xls', b'*.zip', b'*.docx', b'*.xlsx']
for pattern in ext_patterns:
    if pattern in all_data:
        idx = all_data.find(pattern)
        print(f"    Found {pattern.decode()} at offset 0x{idx:08X}")

# Look for PowerShell command patterns
print("\n[+] PowerShell/Command Patterns:")
ps_patterns = [b'powershell', b'cmd.exe', b'/c ', b'-c ', b'Invoke-', b'WebClient', 
               b'DownloadString', b'UploadFile', b'UploadData']
for pattern in ps_patterns:
    if pattern in all_data:
        idx = all_data.find(pattern)
        # Get context
        context = all_data[max(0, idx-20):idx+80]
        try:
            context_str = context.decode('ascii', errors='ignore')
            print(f"    Found {pattern.decode()} at offset 0x{idx:08X}")
            print(f"        Context: {context_str}")
        except:
            pass

print("\n" + "=" * 80)
print("PE Analysis Complete!")
print("=" * 80)

pe.close()
