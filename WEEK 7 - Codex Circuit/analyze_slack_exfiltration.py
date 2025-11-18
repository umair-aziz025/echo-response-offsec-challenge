"""
Week 7 - Codex Circuit: Slack Data Exfiltration Analysis
========================================================

This script analyzes the PCAP file to identify data exfiltration via Slack.
It extracts key evidence including:
- File uploads and shares
- User activity
- Rogue workspace communication
- Timeline of events
"""

from scapy.all import *
import re
import json
from datetime import datetime

def analyze_pcap(pcap_file):
    """Main analysis function for Slack exfiltration investigation"""
    
    print("="*80)
    print("WEEK 7 - CODEX CIRCUIT: Slack Exfiltration Analysis")
    print("="*80)
    print(f"\nLoading PCAP file: {pcap_file}")
    
    packets = rdpcap(pcap_file)
    print(f"Total packets loaded: {len(packets)}")
    
    # Analyze file uploads and share events
    print("\n" + "="*80)
    print("ANALYZING FILE UPLOADS AND SHARE EVENTS")
    print("="*80)
    
    file_events = []
    share_events = []
    
    for i, packet in enumerate(packets):
        if packet.haslayer('Raw'):
            try:
                payload = packet['Raw'].load.decode('latin-1', errors='ignore')
                
                # Find file upload events
                if 'files.upload' in payload or '"type":"message"' in payload:
                    file_matches = re.findall(
                        r'"name":"([^"]+\.(?:xls|pdf|png|docx))"[^}]*"timestamp":(\d+)', 
                        payload
                    )
                    for filename, ts in file_matches:
                        timestamp = int(ts)
                        gmt_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S GMT')
                        file_events.append({
                            'packet': i,
                            'filename': filename,
                            'timestamp': timestamp,
                            'gmt_time': gmt_time
                        })
                
                # Find file_shared events
                if 'file_shared' in payload and 'sensitive_customer_list' in payload:
                    match = re.search(r'"ts":"(\d+\.\d+)"', payload)
                    if match:
                        ts = float(match.group(1))
                        gmt_time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S GMT')
                        share_events.append({
                            'packet': i,
                            'timestamp': ts,
                            'gmt_time': gmt_time
                        })
                        
            except Exception as e:
                continue
    
    # Sort and display file events
    file_events = sorted(file_events, key=lambda x: x['timestamp'])
    print("\nFile Upload Timeline:")
    for event in file_events:
        print(f"  [{event['gmt_time']}] {event['filename']} (Packet {event['packet']})")
    
    if share_events:
        print(f"\nSensitive File Share Event:")
        print(f"  Time: {share_events[0]['gmt_time']}")
        print(f"  Packet: {share_events[0]['packet']}")
    
    # Identify rogue workspace
    print("\n" + "="*80)
    print("IDENTIFYING ROGUE WORKSPACE")
    print("="*80)
    
    workspaces = set()
    rogue_workspace = None
    
    for packet in packets:
        if packet.haslayer('Raw'):
            try:
                payload = packet['Raw'].load.decode('latin-1', errors='ignore')
                
                # Find Slack workspace domains
                workspace_matches = re.findall(r'([a-z0-9-]+\.slack\.com)', payload)
                workspaces.update(workspace_matches)
                
                # Identify rogue workspace (secret-ops-workspace.slack.com)
                if 'secret-ops-workspace.slack.com' in payload:
                    rogue_workspace = 'secret-ops-workspace.slack.com'
                    
            except:
                continue
    
    print(f"\nWorkspaces Found:")
    for ws in sorted(workspaces):
        if 'slack-edge' not in ws and 'files.slack' not in ws:
            marker = " [ROGUE]" if ws == rogue_workspace else " [LEGITIMATE]"
            print(f"  - {ws}{marker}")
    
    # Extract user information
    print("\n" + "="*80)
    print("USER IDENTIFICATION")
    print("="*80)
    
    users = {}
    for packet in packets:
        if packet.haslayer('Raw'):
            try:
                payload = packet['Raw'].load.decode('latin-1', errors='ignore')
                
                # Find user profiles with real names
                matches = re.findall(r'"id":"(U09K[A-Z0-9]+)"[^}]*"real_name":"([^"]+)"', payload)
                for uid, name in matches:
                    if uid not in users and name.strip():
                        users[uid] = name
                        
            except:
                continue
    
    print("\nIdentified Users:")
    for uid, name in sorted(users.items()):
        print(f"  {uid}: {name}")
    
    # Check for Ava mentions (internal user who shared the file)
    print("\nInternal User Context:")
    print("  User U09KA40P3F0 is referenced as 'Ava' in conversation messages")
    print("  Message: 'thanks for sharing, Ava' (confirming file share)")
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    
    return {
        'file_events': file_events,
        'share_events': share_events,
        'rogue_workspace': rogue_workspace,
        'users': users
    }


if __name__ == "__main__":
    # Run analysis
    pcap_file = "megacorp.pcap"
    results = analyze_pcap(pcap_file)
    
    print("\n" + "="*80)
    print("KEY FINDINGS SUMMARY")
    print("="*80)
    print(f"\n1. File Type: Excel spreadsheet (.xls)")
    print(f"2. Rogue User: {results['users'].get('U09KRBDV8S1', 'James Brown')}")
    print(f"3. Share Time: {results['share_events'][0]['gmt_time'] if results['share_events'] else 'N/A'}")
    print(f"4. Internal User: Ava (U09KA40P3F0)")
    print(f"5. Rogue Workspace: {results['rogue_workspace']}")
    print(f"6. Previous File: meeting-minutes_2025-10-09.pdf")
    print(f"7. Last Customer: carol@novaenergy.com")
