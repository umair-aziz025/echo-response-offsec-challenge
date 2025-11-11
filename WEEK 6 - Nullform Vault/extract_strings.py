import re
import struct

# Read the binary
with open('Obfuscated_Intent.exe', 'rb') as f:
    data = f.read()

print("=" * 80)
print("DETAILED STRING EXTRACTION")
print("=" * 80)

# Extract all printable ASCII strings (minimum 4 chars)
def extract_ascii_strings(binary, min_length=4):
    pattern = b'[\x20-\x7E]{' + str(min_length).encode() + b',}'
    strings = []
    for match in re.finditer(pattern, binary):
        s = match.group().decode('ascii', errors='ignore')
        strings.append((match.start(), s))
    return strings

# Extract Unicode strings
def extract_unicode_strings(binary, min_length=4):
    pattern = b'(?:[\x20-\x7E]\x00){' + str(min_length).encode() + b',}'
    strings = []
    for match in re.finditer(pattern, binary):
        try:
            s = match.group().decode('utf-16le', errors='ignore')
            strings.append((match.start(), s))
        except:
            pass
    return strings

print("\n[+] Extracting ASCII strings...")
ascii_strings = extract_ascii_strings(data, min_length=4)

print("\n[+] Extracting Unicode strings...")
unicode_strings = extract_unicode_strings(data, min_length=4)

all_strings = ascii_strings + unicode_strings
all_strings.sort(key=lambda x: x[0])  # Sort by offset

# Filter interesting strings
print("\n[+] All Interesting Strings (sorted by offset):")
print("-" * 80)

interesting_patterns = [
    (r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', 'IP Address'),
    (r'https?://', 'URL'),
    (r'www\.', 'Domain'),
    (r'\.(txt|doc|pdf|xls|zip|exe|dll|bat|ps1|key|pem|csv)', 'File Extension'),
    (r'[Pp]ower[Ss]hell', 'PowerShell'),
    (r'cmd|CMD', 'Command'),
    (r'[Ww]eb[Cc]lient', 'WebClient'),
    (r'[Uu]pload', 'Upload'),
    (r'[Dd]ownload', 'Download'),
    (r'[Ss]ystem', 'System Call'),
    (r'[Cc]onnect', 'Connection'),
]

for offset, s in all_strings:
    # Check if string matches any interesting pattern
    is_interesting = False
    for pattern, category in interesting_patterns:
        if re.search(pattern, s, re.IGNORECASE):
            is_interesting = True
            break
    
    # Also show strings with certain keywords
    keywords = ['http', 'www', 'upload', 'download', 'powershell', 'cmd', 
                'invoke', 'webclient', 'system', 'exec', 'shell', 'net',
                'socket', 'connect', 'send', 'recv', 'icmp', 'echo']
    
    if any(kw in s.lower() for kw in keywords):
        is_interesting = True
    
    # Show IP addresses
    if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', s):
        is_interesting = True
    
    # Show strings with dots and slashes (potential paths/URLs)
    if ('/' in s or '\\' in s) and len(s) > 8:
        is_interesting = True
    
    if is_interesting and len(s) > 3 and len(s) < 300:
        print(f"[0x{offset:08X}] {s}")

# Look for encoded data
print("\n" + "=" * 80)
print("[+] Looking for potential encoded/obfuscated data...")
print("-" * 80)

# Search for XOR patterns or repeated bytes
for offset, s in all_strings:
    # Look for base64-like patterns
    if re.match(r'^[A-Za-z0-9+/=]{20,}$', s):
        print(f"[0x{offset:08X}] [BASE64?] {s[:100]}")
    
    # Look for hex patterns
    if re.match(r'^[0-9A-Fa-f]{20,}$', s):
        print(f"[0x{offset:08X}] [HEX?] {s[:100]}")

# Manual scan for IP addresses in raw bytes
print("\n" + "=" * 80)
print("[+] Raw byte scan for IP addresses...")
print("-" * 80)

# Look for IP address patterns in raw bytes
for i in range(len(data) - 15):
    # Check for dotted quad pattern in ASCII
    chunk = data[i:i+15]
    try:
        s = chunk.decode('ascii', errors='ignore')
        ip_match = re.match(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})', s)
        if ip_match:
            octets = [int(x) for x in ip_match.groups()]
            if all(0 <= x <= 255 for x in octets):
                ip = '.'.join(map(str, octets))
                print(f"[0x{i:08X}] Found IP: {ip}")
    except:
        pass

print("\n" + "=" * 80)
print("Detailed extraction complete!")
print("=" * 80)
