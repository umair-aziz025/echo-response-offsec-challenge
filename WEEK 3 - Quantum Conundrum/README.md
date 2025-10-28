# WEEK 3 - Quantum Conundrum 🔐

**Challenge:** Quantum Conundrum - Breaking the "Unbreakable" Cipher  
**Date:** October 21, 2025  
**Status:** ✅ COMPLETED  
**Category:** Reverse Engineering, Cryptanalysis, Binary Analysis  
**Difficulty:** Hard

---

## 📖 Challenge Overview

### Scenario

*"The Obscurarium realm's defenses are hailed as 'unbreakable' and 'quantum-proof'—and for good reason. It safeguards one of the most dangerous relics still hidden: the **Obscuran Key**, a powerful artifact bound to memory, truth, and perception."*

**Megacorp Quantum**, a vital stronghold of security infrastructure in the Obscurarium Realm, believes no cipher, no codecaster, no force – magical or digital – can bypass their quantum-safe architecture.

**But confidence is no defense against what you're about to uncover.**

**Mission:** Attempt to break Megacorp Quantum's encryption system, pry open the encrypted file, and extract the flag hidden within. Determine whether the algorithmic wards truly protect the Obscuran Key.

---

## 🎯 Investigation Objectives

Analyze the provided artifacts to answer the following questions:

1. ✅ Analyze `publickey.pubkey` and decode its contents. Identify the encoding algorithm and what the decoded values represent.
2. ✅ Investigate how the Seed is calculated. What other data is used beyond the public key?
3. ✅ Reverse engineer the decryption program. How many distinct transform passes are applied before the final XOR mask? Explain the first three transformations.
4. ✅ Decrypt the `decrypt_me.enc` file and submit the flag found in the plaintext output.

---

## 📦 Available Artifacts

The challenge package (`QuantumConundrum.zip`, password: `Conundrum2025`) contains:

| Artifact | Type | Description |
|----------|------|-------------|
| `QuantumConundrum.exe` | Binary | Windows executable - encryption/decryption application |
| `decrypt_me.enc` | Encrypted File | The locked vault containing the hidden flag |
| `publickey.pubkey` | Public Key | The key used to lock the data away |
| `README.txt` | Documentation | Directions on encryption (with missing details) |

---

## 🔑 Key Findings

### Attack Summary

**Target:** Megacorp Quantum Encryption System  
**Claimed Security:** "Unbreakable" and "Quantum-Proof"  
**Actual Security:** ❌ **FULLY COMPROMISED**

### Investigation Results

```
1. Public Key Analysis
   └─ Encoding: Base64 (NOT encryption!)
   └─ Decoded: 24.07.2025|megacorp@quantum.com
   └─ Purpose: Static seed component

2. Seed Calculation
   └─ Components: Email + Date + Timestamp + "PublicSalt"
   └─ Weakness: Hardcoded salt, no KDF
   └─ Vulnerability: Predictable seed generation

3. Transformation Pipeline
   └─ 7 distinct layers before XOR
   └─ Ring rotation → Add → Subtract → Cyclic shifts
      → Quadrant swaps → Bit-pair swap → Variable rotation
   └─ All reversible through binary analysis

4. Successful Decryption
   └─ Keystream: (char * 7 + index) & 0xFF
   └─ Flag extracted: OS{BENDER}
   └─ System: BROKEN ✅
```

### Critical Vulnerabilities

**🔴 CRITICAL:**
- Base64-encoded "public key" (not actual encryption)
- Hardcoded salt: `PublicSalt`
- No key derivation function (KDF)
- Weak keystream generation (simple arithmetic)

**🟡 HIGH:**
- Deterministic encryption
- Static date component
- No authentication/integrity checks

---

## 🛠️ Reverse Engineering Process

### 1. Binary Analysis with Ghidra

**Tool:** Ghidra 11.2.1 PUBLIC  
**Target:** `QuantumConundrum.exe`

**Key Functions Identified:**
- `FUN_140002680` - Main orchestration function
- `FUN_1400019e0` - Matrix building from input stream
- `FUN_140002070` - Add constant transformation
- `FUN_1400021f0` - Subtract constant transformation
- `FUN_140002390` - Cyclic shifts and permutations
- `FUN_140002540` - Even/odd bit swap
- `FUN_140001df0` - Keystream derivation
- `FUN_140001c00` - XOR application

---

### 2. The 7 Transformation Layers

#### **Transform 1: Ring Rotation (90° Clockwise)**
```
Treats N×N matrix as concentric rings
Each ring rotates independently
Outer ring: full 90° rotation
Inner rings: same process

Example 4×4:
 1  2  3  4      13  9  5  1
 5  6  7  8  →   14 10  6  2
 9 10 11 12      15 11  7  3
13 14 15 16      16 12  8  4
```

**Purpose:** Spatial scrambling, initial obfuscation

---

#### **Transform 2: Add Constant (mod 256)**
```python
add_val = year & 0xFF  # 2025 & 0xFF = 225
for each cell:
    cell = (cell + add_val) mod 256
```

**Example:**
- Cell: 50 → (50 + 225) mod 256 = 19
- Cell: 200 → (200 + 225) mod 256 = 169

**Purpose:** Uniform value diffusion

---

#### **Transform 3: Subtract Constant (mod 256)**
```python
sub_val = month  # July = 7
for each cell:
    cell = (cell - sub_val + 256) mod 256
```

**Example:**
- Cell: 50 → (50 - 7 + 256) mod 256 = 43
- Cell: 5 → (5 - 7 + 256) mod 256 = 254

**Purpose:** Value confusion, non-linear transformation

---

#### **Transform 4: Cyclic Shifts**
```python
shift = day % N  # 24 % 64 = 24
rows.rotate(-shift)    # Rotate entire rows
columns.rotate(-shift) # Rotate entire columns
```

**Purpose:** Positional permutation

---

#### **Transform 5: Quadrant Swaps**
```
Divides matrix into quadrants
Swaps in specific pattern
May include transposition
```

**Purpose:** Geometric diffusion

---

#### **Transform 6: Even/Odd Bit Swap**
```python
def bit_flip_pairs(x):
    return ((x >> 1) & 0x55) | ((x & 0x55) << 1)

Example:
  10110011 → 01101101
  ↑↑↑↑↑↑↑↑
  Bit pairs swap positions
```

**Purpose:** Bit-level confusion

---

#### **Transform 7: Variable Bit Rotation**
```python
for r in range(N):
    for c in range(N):
        spin = (year + month + day + r + c) & 7
        cell = rotate_right(cell, spin)
```

**Purpose:** Position-dependent obfuscation

---

### 3. Keystream Generation

```python
def keystream(seed, need):
    out = bytearray()
    idx = 0
    while len(out) < need:
        for ch in seed:
            out.append((ord(ch) * 7 + idx) & 0xFF)
            idx += 1
    return bytes(out)
```

**Weakness:** Simple arithmetic, not cryptographically secure

---

### 4. Decryption Script

**Complete Python Solution:**

```python
#!/usr/bin/env python3
from pathlib import Path
from collections import deque

EMAIL = "megacorp@quantum.com"
DATE = "24.07.2025"
SALT = "PublicSalt"
FILE = Path("decrypt_me.txt.enc")

def rot_right(x, amt):
    amt &= 7
    return ((x >> amt) | ((x << (8 - amt)) & 0xFF)) & 0xFF

def bit_flip_pairs(x):
    return ((x >> 1) & 0x55) | ((x & 0x55) << 1)

def keystream(seed, need):
    out = bytearray()
    idx = 0
    while len(out) < need:
        for ch in seed:
            out.append((ord(ch) * 7 + idx) & 0xFF)
            idx += 1
            if len(out) >= need:
                break
    return bytes(out)

def decode(path):
    data = path.read_bytes()
    ts_len = int.from_bytes(data[-8:-4], "little")
    n = int.from_bytes(data[-4:], "little")
    timestamp = data[-8 - ts_len:-8].decode("ascii")
    block = data[:n * n]

    seed = EMAIL + DATE + timestamp + SALT
    mask = keystream(seed, len(block))
    raw = bytes(b ^ m for b, m in zip(block, mask))

    grid = [list(raw[i * n:(i + 1) * n]) for i in range(n)]
    year, month, day = 2025, 7, 24

    # Reverse transform 7: Variable rotation
    for r in range(n):
        for c in range(n):
            spin = (year + month + day + r + c) & 7
            if spin:
                grid[r][c] = rot_right(grid[r][c], spin)

    # Reverse transform 6: Bit-pair swap
    for r in range(n):
        for c in range(n):
            grid[r][c] = bit_flip_pairs(grid[r][c])

    # Reverse transform 4: Cyclic shifts
    shift = day % n
    if shift:
        rows = deque(grid)
        rows.rotate(-shift)
        grid = [list(row) for row in rows]
        for r in range(n):
            row = deque(grid[r])
            row.rotate(-shift)
            grid[r] = list(row)

    # Reverse transforms 3 & 2: Subtract & Add
    add_val = year & 0xFF
    sub_val = month
    for r in range(n):
        for c in range(n):
            v = grid[r][c]
            v = (v + sub_val) & 0xFF
            v = (v - add_val) & 0xFF
            grid[r][c] = v

    # Reverse transform 1: Ring rotation (via column reading)
    buf = bytearray()
    for c in range(n):
        for r in range(n - 1, -1, -1):
            b = grid[r][c]
            if b:
                buf.append(b)

    text = buf.decode("utf-8")
    flag = text[text.index("{"):text.index("}") + 1]
    return text, flag

if __name__ == "__main__":
    poem, flag = decode(FILE)
    print(poem)
    print('\nFLAG:', flag)
```

---

## 📊 MITRE ATT&CK Mapping

| Tactic | Technique | Application |
|--------|-----------|-------------|
| Discovery | T1082 - System Information Discovery | Binary analysis revealed architecture |
| Collection | T1005 - Data from Local System | Encrypted file analyzed |
| Credential Access | T1552.001 - Credentials in Files | Hardcoded salt found in binary |
| Defense Evasion | T1027 - Obfuscated Files or Information | 7-layer transformation |

---

## 💡 Lessons Learned

### What Megacorp Did Wrong

1. **Misnamed "Public Key"**
   - Used Base64 encoding instead of actual public-key cryptography
   - No RSA, ECC, or other asymmetric encryption
   - Misleading security theater

2. **Weak Seed Generation**
   - Hardcoded salt: `PublicSalt`
   - No key derivation function (PBKDF2, Argon2)
   - Predictable components

3. **Non-Cryptographic Keystream**
   - Simple arithmetic: `(char * 7 + idx) & 0xFF`
   - Not a CSPRNG
   - Linear and predictable

4. **Obfuscation ≠ Security**
   - 7 transformation layers provide complexity
   - But all are reversible through analysis
   - Complexity without cryptographic strength

5. **No Authentication**
   - No MAC or HMAC
   - No integrity checking
   - Vulnerable to tampering

---

### What "Quantum-Proof" Actually Means

**Claimed:** Quantum-resistant encryption  
**Reality:** No quantum-resistant algorithms used

**True quantum-proof encryption requires:**
- Lattice-based cryptography (NTRU, FrodoKEM)
- Code-based cryptography (Classic McEliece)
- Hash-based signatures (SPHINCS+)
- NIST post-quantum candidates

**This system:** Uses none of the above. Pure marketing.

---

## 🛡️ Recommended Fixes

### Immediate Actions

1. **Replace "Public Key" System**
   ```
   - Implement RSA-2048 or ECC P-256 minimum
   - Use proper PEM/DER key formats
   - Store private keys securely (HSM/vault)
   ```

2. **Implement Real Encryption**
   ```
   - Use AES-256-GCM or ChaCha20-Poly1305
   - Authenticated encryption (AEAD)
   - Random IV/nonce per encryption
   ```

3. **Add Key Derivation**
   ```
   - Argon2id (preferred) or PBKDF2
   - 100,000+ iterations
   - Random salt per operation
   ```

4. **Add Integrity Protection**
   ```
   - HMAC-SHA256 or built-in AEAD
   - Verify before decrypt
   - Prevent tampering
   ```

---

## 📚 Skills Demonstrated

- ✅ **Binary Reverse Engineering:** Ghidra disassembly and decompilation
- ✅ **Cryptanalysis:** Breaking custom encryption schemes
- ✅ **Algorithm Analysis:** Understanding transformation pipelines
- ✅ **Python Scripting:** Implementing decryption logic
- ✅ **Bit Manipulation:** Understanding bit-level operations
- ✅ **Matrix Operations:** Spatial transformations and permutations
- ✅ **Encoding/Decoding:** Base64, data structure parsing
- ✅ **Security Assessment:** Vulnerability identification
- ✅ **Technical Documentation:** Comprehensive reporting

---

## 📁 Repository Contents

```
WEEK 3 - Quantum Conundrum/
├── README.md (this file)
├── INVESTIGATION_REPORT.md (detailed analysis)
├── solve_decrypt.py (decryption script)
├── Understanding_7_Transformations.md (transformation guide)
└── artifacts/
    ├── publickey.pubkey
    ├── decrypt_me.enc
    └── QuantumConundrum.exe (analyzed binary)
```

---

## 🏆 Challenge Completion

**Status:** ✅ **ALL 4 OBJECTIVES COMPLETED**

| Question | Answer | Evidence |
|----------|--------|----------|
| Q1 | Base64: `24.07.2025\|megacorp@quantum.com` | Public key decoding |
| Q2 | Email + Date + Timestamp + PublicSalt | Seed algorithm analysis |
| Q3 | 7 transforms: Ring, Add, Subtract | Binary reverse engineering |
| Q4 | `OS{BENDER}` | Successful decryption |

---

## 🔗 Resources

- [Ghidra Software Reverse Engineering](https://ghidra-sre.org/)
- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [Cryptographic Right Answers](https://latacora.micro.blog/2018/04/03/cryptographic-right-answers.html)
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

---

**Investigator:** MR. Umair  
**Date Completed:** October 21, 2025  
**Challenge Series:** OffSec Echo Response - Proving Grounds: The Gauntlet

---

*"But confidence is no defense against what you're about to uncover."*

**Verdict:** The "unbreakable" encryption is BROKEN. The Obscuran Key is vulnerable. 🔓
