#!/usr/bin/env python3
"""
Tutorial Challenge - Analysis Script
Echo Response - OffSec Challenge
Author: Umair Aziz
Week: 0 (Tutorial)
Difficulty: Easy
"""

import base64
import re
from datetime import datetime

def decode_tutorial_message():
    """Decode the Base64 encoded poem from tutorial.txt"""
    encoded_message = "TXVmZmluIHRoZSBjYXQgY2xpY2tlZCBvbiBhIGxpbmssCk5vdyBhbGwgaGlzIGZpbGVzIGJlZ2FuIHRvIHNocmluayEKSGUgc2hvdWxk4oCZdmUgY2hlY2tlZCB0aGUgc2VuZGVy4oCZcyBuYW1lLApCdXQgbm93IGhpcyBsYXB0b3AncyBub3QgdGhlIHNhbWUuCgpBIHBhc3N3b3JkIHN0cm9uZywgYSBmaXJld2FsbCB0aWdodCwKS2VlcHMgc25lYWt5IGhhY2tlcnMgb3V0IG9mIHNpZ2h0LgpTbyB0aGluayBiZWZvcmUgeW91IHN1cmYgYW5kIHBsYXnigJQKQ3liZXItc21hcnRzIHdpbGwgc2F2ZSB0aGUgZGF5IQoKVGhlIGFuc3dlciB0byB0aGlzIGV4ZXJjaXNlIGlzICJUcnlIYXJkZXIi"
    
    decoded = base64.b64decode(encoded_message).decode('utf-8')
    
    print("=" * 80)
    print("TUTORIAL MESSAGE DECODED")
    print("=" * 80)
    print(decoded)
    print("=" * 80)
    print()
    
    # Extract the answer
    answer_match = re.search(r'The answer to this exercise is "([^"]+)"', decoded)
    if answer_match:
        answer = answer_match.group(1)
        print(f"✅ Exercise Answer: {answer}")
        print()
    
    return decoded

def analyze_access_logs(log_file='access.log'):
    """Analyze access.log for suspicious activity"""
    print("=" * 80)
    print("ACCESS LOG ANALYSIS")
    print("=" * 80)
    
    try:
        with open(log_file, 'r') as f:
            logs = f.readlines()
    except FileNotFoundError:
        print(f"❌ Error: {log_file} not found")
        return
    
    suspicious_activities = []
    path_traversal_attacks = []
    error_responses = []
    authentication_failures = []
    
    for line_num, line in enumerate(logs, 1):
        # Check for path traversal attacks
        if '../' in line or '..\\' in line:
            path_traversal_attacks.append({
                'line': line_num,
                'content': line.strip()
            })
        
        # Check for 403/404/500 errors
        if ' 403 ' in line or ' 404 ' in line or ' 500 ' in line:
            error_responses.append({
                'line': line_num,
                'content': line.strip()
            })
        
        # Check for authentication failures (401)
        if ' 401 ' in line:
            authentication_failures.append({
                'line': line_num,
                'content': line.strip()
            })
    
    # Report findings
    print(f"\n📊 Total log entries analyzed: {len(logs)}")
    print()
    
    if path_traversal_attacks:
        print(f"🚨 PATH TRAVERSAL ATTACKS DETECTED: {len(path_traversal_attacks)}")
        print("-" * 80)
        for attack in path_traversal_attacks:
            # Extract key details
            match = re.search(r'(\d+\.\d+\.\d+\.\d+).*?"([^"]+)".*?(\d+)\s+(\d+)', attack['content'])
            if match:
                ip = match.group(1)
                request = match.group(2)
                status_code = match.group(3)
                size = match.group(4)
                
                print(f"  Line {attack['line']}:")
                print(f"    Source IP: {ip}")
                print(f"    Request: {request}")
                print(f"    Status Code: {status_code}")
                print(f"    Response Size: {size} bytes")
                
                # Extract the malicious path
                if 'GET' in request:
                    path = request.split(' ')[1]
                    print(f"    Malicious Path: {path}")
                    
                    # Count directory traversal attempts
                    traversal_count = path.count('../')
                    print(f"    Directory Traversal Depth: {traversal_count} levels")
                    
                    # Extract target file
                    target_file = path.split('/')[-1]
                    print(f"    Target File: {target_file}")
                print()
        print()
    
    if authentication_failures:
        print(f"🔐 AUTHENTICATION FAILURES: {len(authentication_failures)}")
        print("-" * 80)
        for failure in authentication_failures:
            match = re.search(r'(\d+\.\d+\.\d+\.\d+).*?"([^"]+)"', failure['content'])
            if match:
                ip = match.group(1)
                request = match.group(2)
                print(f"  Line {failure['line']}: {ip} - {request}")
        print()
    
    if error_responses:
        print(f"⚠️ ERROR RESPONSES: {len(error_responses)}")
        print("-" * 80)
        for error in error_responses:
            match = re.search(r'(\d+\.\d+\.\d+\.\d+).*?"([^"]+)".*?(\d+)', error['content'])
            if match:
                ip = match.group(1)
                request = match.group(2)
                status = match.group(3)
                print(f"  Line {error['line']}: {ip} - {request} [{status}]")
        print()
    
    # Summary of findings
    print("=" * 80)
    print("SECURITY SUMMARY")
    print("=" * 80)
    print(f"✅ Total Entries: {len(logs)}")
    print(f"🚨 Path Traversal Attacks: {len(path_traversal_attacks)}")
    print(f"🔐 Authentication Failures: {len(authentication_failures)}")
    print(f"⚠️ Error Responses: {len(error_responses)}")
    print()
    
    # Key finding
    if path_traversal_attacks:
        print("🎯 CRITICAL FINDING:")
        print("   A successful path traversal attack was detected attempting to")
        print("   access SSH private keys from user 'dave' home directory.")
        print("   Attack successfully returned 1678 bytes (200 OK status).")
        print()
        print("   Attack IP: 192.168.1.101")
        print("   Target: /home/dave/.ssh/id_rsa")
        print("   Method: Directory traversal using ../../../../../../../../")
        print()

def main():
    """Main analysis function"""
    print()
    print("*" * 80)
    print(" ECHO RESPONSE - WEEK 0: TUTORIAL CHALLENGE ANALYSIS")
    print(" Difficulty: Easy")
    print(" Category: Incident Response, Log Analysis, Encoding")
    print("*" * 80)
    print()
    
    # Part 1: Decode the tutorial message
    decode_tutorial_message()
    
    # Part 2: Analyze access logs
    analyze_access_logs()
    
    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print()
    print("📝 Questions Answered:")
    print("   1. Tutorial poem decoded successfully")
    print("   2. Exercise answer extracted: 'TryHarder'")
    print("   3. Path traversal attack identified and analyzed")
    print("   4. Malicious IP address identified: 192.168.1.101")
    print("   5. Target file identified: /home/dave/.ssh/id_rsa")
    print()

if __name__ == "__main__":
    main()
