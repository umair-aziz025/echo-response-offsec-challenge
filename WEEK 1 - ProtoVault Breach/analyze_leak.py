#!/usr/bin/env python3
import requests
import codecs

# Download the leaked database from S3
url = "https://protoguard-asset-management.s3.us-east-2.amazonaws.com/db_backup.xyz"
print(f"[*] Downloading from: {url}")

try:
    response = requests.get(url)
    response.raise_for_status()
    
    # Save the encoded file
    with open("leaked_db_encoded.xyz", "wb") as f:
        f.write(response.content)
    print("[+] Downloaded successfully")
    
    # Decode from ROT13
    encoded_text = response.content.decode('utf-8', errors='ignore')
    decoded_text = codecs.decode(encoded_text, 'rot_13')
    
    # Save the decoded file
    with open("leaked_db_decoded.sql", "w", encoding='utf-8') as f:
        f.write(decoded_text)
    print("[+] Decoded using ROT13")
    
    # Search for Naomi Adler
    print("\n[*] Searching for Naomi Adler...")
    lines = decoded_text.split('\n')
    for i, line in enumerate(lines):
        if 'naomi' in line.lower() and 'adler' in line.lower():
            print(f"\n[!] Found at line {i}:")
            print(line)
            # Print surrounding lines for context
            for j in range(max(0, i-2), min(len(lines), i+3)):
                print(f"  {j}: {lines[j]}")
    
except Exception as e:
    print(f"[!] Error: {e}")
