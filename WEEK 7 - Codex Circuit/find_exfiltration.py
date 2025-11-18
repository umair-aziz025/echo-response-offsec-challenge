#!/usr/bin/env python3
"""
Deep dive into conversations.history to find exfiltrated data
"""

import scapy.all as scapy
import re
import json

def find_exfiltration(pcap_file):
    print("=" * 80)
    print(" SEARCHING FOR EXFILTRATED DATA")
    print("=" * 80)
    
    packets = scapy.rdpcap(pcap_file)
    
    # Look for HTTP responses containing conversation data
    conversation_data = []
    file_data = []
    
    print(f"\n[*] Deep scanning {len(packets)} packets...")
    
    for i, pkt in enumerate(packets):
        if not pkt.haslayer(scapy.Raw):
            continue
        
        payload = pkt[scapy.Raw].load
        
        try:
            payload_str = payload.decode('utf-8', errors='ignore')
        except:
            continue
        
        # Look for JSON responses with messages
        if '"messages":[' in payload_str or '"text":' in payload_str:
            # This might be a conversations.history response
            if len(payload_str) > 500:  # Significant response
                conversation_data.append({
                    'packet': i,
                    'size': len(payload_str),
                    'data': payload_str
                })
        
        # Look for file content or file metadata
        if '"file":' in payload_str and '"name"' in payload_str:
            file_data.append({
                'packet': i,
                'size': len(payload_str),
                'data': payload_str
            })
    
    print(f"\n[+] Found {len(conversation_data)} conversation responses")
    print(f"[+] Found {len(file_data)} file-related responses")
    
    # Analyze conversation data
    if conversation_data:
        print("\n" + "=" * 80)
        print(" CONVERSATION DATA ANALYSIS")
        print("=" * 80)
        
        for idx, conv in enumerate(conversation_data):
            print(f"\n[Conversation #{idx+1}] Packet {conv['packet']} - Size: {conv['size']} bytes")
            
            # Try to parse as JSON
            try:
                # Find JSON start
                json_start = conv['data'].find('{')
                if json_start != -1:
                    json_data = conv['data'][json_start:]
                    # Find end of JSON (heuristic)
                    try:
                        parsed = json.loads(json_data)
                        
                        # Extract messages
                        if 'messages' in parsed:
                            print(f"    Messages found: {len(parsed['messages'])}")
                            for msg in parsed['messages'][:5]:  # First 5 messages
                                if 'text' in msg:
                                    print(f"    - {msg['text'][:200]}")
                                if 'files' in msg:
                                    print(f"    - FILES ATTACHED: {len(msg['files'])}")
                                    for file in msg['files']:
                                        if 'name' in file:
                                            print(f"      * {file.get('name', 'unknown')}")
                        
                        # Save full JSON
                        with open(f'conversation_{idx+1}.json', 'w') as f:
                            json.dump(parsed, f, indent=2)
                        print(f"    Saved to conversation_{idx+1}.json")
                    except:
                        # Not valid JSON, just print excerpt
                        print(f"    Excerpt: {conv['data'][:500]}")
            except Exception as e:
                print(f"    Error parsing: {e}")
    
    # Analyze file data
    if file_data:
        print("\n" + "=" * 80)
        print(" FILE DATA ANALYSIS")
        print("=" * 80)
        
        for idx, file_info in enumerate(file_data[:10]):  # First 10
            print(f"\n[File #{idx+1}] Packet {file_info['packet']}")
            
            # Extract file names
            name_matches = re.findall(r'"name":"([^"]+)"', file_info['data'])
            for name in set(name_matches):
                print(f"    Filename: {name}")
            
            # Extract file types
            type_matches = re.findall(r'"mimetype":"([^"]+)"', file_info['data'])
            for ftype in set(type_matches):
                print(f"    Type: {ftype}")
            
            # Extract URLs
            url_matches = re.findall(r'"url_private":"([^"]+)"', file_info['data'])
            for url in set(url_matches):
                print(f"    URL: {url[:100]}...")
            
            # Save to file
            with open(f'file_metadata_{idx+1}.txt', 'w') as f:
                f.write(file_info['data'])
            print(f"    Saved to file_metadata_{idx+1}.txt")
    
    print("\n[+] Analysis complete!")

if __name__ == '__main__':
    find_exfiltration('megacorp.pcap')
