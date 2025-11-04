# Week 5 Emerald Anomaly - Analysis Script
# Decodes CRYPTO_SEED obfuscation from MCP backdoor

Write-Host "`n=== CRYPTO_SEED Decoder ===" -ForegroundColor Cyan
Write-Host "Analyzing backdoor obfuscation from server.py`n" -ForegroundColor Yellow

# CRYPTO_SEED array from line 34 of server.py
$seed = "mah0lptuhsari.!p0s.bCocVhFhxtbOxsvmr+urcsgernynev=bpsUph.h2tarNh1e76itLogptngFfbiikC2ntAosMacEstrgn/um!iY".ToCharArray()

Write-Host "CRYPTO_SEED length: $($seed.Length)" -ForegroundColor Green
Write-Host "CRYPTO_SEED array: $($seed -join '')`n" -ForegroundColor Gray

# Decode protocol (hPalette)
Write-Host "[*] Decoding hPalette (protocol)..." -ForegroundColor Cyan
$protocol_idx = @(2,6,28,5)
$protocol = -join ($protocol_idx | ForEach-Object { $seed[$_] })
Write-Host "    Indices: [$($protocol_idx -join ', ')]" -ForegroundColor Gray
Write-Host "    Result: $protocol" -ForegroundColor Green

# Decode domain (nWidth)
Write-Host "`n[*] Decoding nWidth (domain)..." -ForegroundColor Cyan
$domain_idx = @(1,33,10,59,60,11,17,13,41,12,69,8,7,19,37,32,42,35,22,3,44,74,47,46,86,18,39,21,0)
$domain = -join ($domain_idx | ForEach-Object { $seed[$_] })
Write-Host "    Indices: [$($domain_idx -join ', ')]" -ForegroundColor Gray
Write-Host "    Result: $domain" -ForegroundColor Green

# Construct full URL
$full_url = "${protocol}://${domain}"
Write-Host "`n[+] Full C2 URL: $full_url" -ForegroundColor Yellow

# Typosquatting analysis
Write-Host "`n=== Typosquatting Analysis ===" -ForegroundColor Cyan
$legitimate = "avatars.githubusercontent.com"
$typosquatted = $domain

Write-Host "Legitimate:   $legitimate" -ForegroundColor Green
Write-Host "Typosquatted: $typosquatted" -ForegroundColor Red

# Highlight difference
Write-Host "`nKey difference: 'o' replaced with '0' (zero)" -ForegroundColor Yellow
Write-Host "  githubuserc[o]ntent.com  (legitimate)" -ForegroundColor Green
Write-Host "  githubuserc[0]ntent.com  (typosquatted)" -ForegroundColor Red

# DNS resolution (from Sysmon Event ID 22)
Write-Host "`n=== DNS Resolution ===" -ForegroundColor Cyan
Write-Host "Event: Sysmon Event ID 22 (DNS Query)" -ForegroundColor Gray
Write-Host "Timestamp: 2025-08-26 14:08:22" -ForegroundColor Gray
Write-Host "QueryName: $domain" -ForegroundColor Yellow
Write-Host "QueryResults: ::ffff:100.43.72.21" -ForegroundColor Green
Write-Host "Process: python.exe (ross.martinez)" -ForegroundColor Gray

# SMTP authentication (from PCAP)
Write-Host "`n=== SMTP Authentication ===" -ForegroundColor Cyan
$encoded_creds = "AHJvc3MubWFydGluZXpAbWVnYWNvcnBvbmUuYWkAU3VwZXJTZWN1cmVQNHNzMSE="
$decoded_creds = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($encoded_creds))

Write-Host "Source IP: 79.134.64.179" -ForegroundColor Yellow
Write-Host "Target: mail.megacorpone.ai:25" -ForegroundColor Gray
Write-Host "Method: AUTH PLAIN" -ForegroundColor Gray
Write-Host "`nEncoded: $encoded_creds" -ForegroundColor Gray
Write-Host "Decoded: $decoded_creds" -ForegroundColor Red

# Parse credentials
$cred_parts = $decoded_creds -split "`0"
if ($cred_parts.Length -ge 3) {
    Write-Host "`nParsed credentials:" -ForegroundColor Cyan
    Write-Host "  Username: $($cred_parts[1])" -ForegroundColor Yellow
    Write-Host "  Password: $($cred_parts[2])" -ForegroundColor Red
}

# Summary
Write-Host "`n=== Attack Summary ===" -ForegroundColor Cyan
Write-Host "[+] Attacker IP 1: 100.43.72.21 (C2/Exfiltration)" -ForegroundColor Green
Write-Host "    - Hosts typosquatted domain" -ForegroundColor Gray
Write-Host "    - Receives exfiltrated credentials via HTTP" -ForegroundColor Gray
Write-Host "    - Discovered via Sysmon DNS Event ID 22" -ForegroundColor Gray

Write-Host "`n[+] Attacker IP 2: 79.134.64.179 (SMTP Relay)" -ForegroundColor Green
Write-Host "    - Validates stolen credentials" -ForegroundColor Gray
Write-Host "    - Authenticates to mail server" -ForegroundColor Gray
Write-Host "    - Discovered via PCAP analysis" -ForegroundColor Gray

Write-Host "`n[+] Backdoor triggers:" -ForegroundColor Yellow
Write-Host "    - PowerShell commands containing 'pass'" -ForegroundColor Gray
Write-Host "    - PowerShell commands containing 'securestring'" -ForegroundColor Gray

Write-Host "`n[+] Exfiltration method:" -ForegroundColor Yellow
Write-Host "    - HTTP GET to $full_url" -ForegroundColor Gray
Write-Host "    - Base64-encoded PowerShell command in 'dynamic_icon' parameter" -ForegroundColor Gray

Write-Host "`n[*] Analysis complete!`n" -ForegroundColor Cyan
