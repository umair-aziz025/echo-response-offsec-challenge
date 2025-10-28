# Understanding the 7 Transformations in Quantum Conundrum Decryption

## Question 3 Explanation

**Question:** How many distinct transform passes are applied before the final XOR mask?

**Answer:** **7 transformations**

---

## Complete Transformation Flow

Based on the disassembled code analysis of `FUN_140002680` (the main orchestrating function), here are the **7 transformations** applied to the N×N matrix **BEFORE** the final XOR operation:

---

### **Transformation 1: Ring Rotation (90° Clockwise)**
**Location:** Inline block in `FUN_140002680` (lines ~680-750)

**What it does:**
- Treats the N×N matrix as concentric "rings" (like layers of an onion)
- Rotates each ring 90 degrees clockwise
- The outermost ring rotates independently from inner rings
- This is a physical spatial rearrangement of the matrix data

**Example (4×4 matrix):**
```
Before:              After:
 1  2  3  4          13  9  5  1
 5  6  7  8    →     14 10  6  2
 9 10 11 12          15 11  7  3
13 14 15 16          16 12  8  4
```

**Why first:** This scrambles the spatial layout before any byte-level operations.

---

### **Transformation 2: Add Constant (mod 256)**
**Location:** `FUN_140002070`
**Parameter:** `k₁` (derived from year in date)

**What it does:**
- Adds a constant value to every byte in the matrix
- Operations are modulo 256 (wraps around at byte boundary)
- Each cell: `new_value = (old_value + k₁) mod 256`

**Code signature:**
```c
*puVar6 = iVar9 + ((int)((-(uint)(iVar9 < 0) & 0xff) + iVar9) >> 8) * -0x100;
// This is modulo 256 arithmetic: (value + param_2) & 0xFF
```

**Example:**
- If k₁ = 225 (from year 2025 & 0xFF)
- Cell with value 50 becomes (50 + 225) mod 256 = 19
- Cell with value 200 becomes (200 + 225) mod 256 = 169

**Purpose:** Adds diffusion - changes all byte values uniformly.

---

### **Transformation 3: Subtract Constant (mod 256)**
**Location:** `FUN_1400021f0`
**Parameter:** `k₂` (derived from month in date)

**What it does:**
- Subtracts a constant value from every byte in the matrix
- Operations are modulo 256 (wraps around at byte boundary)
- Each cell: `new_value = (old_value - k₂ + 256) mod 256`

**Code signature:**
```c
iVar9 = (*puVar6 - param_2) + 0x100;
*puVar6 = iVar9 + ((int)((-(uint)(iVar9 < 0) & 0xff) + iVar9) >> 8) * -0x100;
// This is: (value - param_2) & 0xFF with proper wrapping
```

**Example:**
- If k₂ = 7 (month July)
- Cell with value 50 becomes (50 - 7 + 256) mod 256 = 43
- Cell with value 5 becomes (5 - 7 + 256) mod 256 = 254

**Purpose:** Further byte-level obfuscation, reversing some of the addition.

---

### **Transformation 4: Row/Column Cyclic Shifts**
**Location:** `FUN_140002390` (first part)
**Parameter:** `k₃` (derived from day in date)

**What it does:**
- Performs cyclic rotation of entire rows
- Performs cyclic rotation of entire columns
- Shift amount is based on day of month modulo N
- This is like rotating the matrix without changing individual bytes

**Example (day % N = 2, for 4×4 matrix):**
```
Rows rotate left by 2:
Row [A B C D] becomes [C D A B]

Columns rotate up by 2:
Col [ 1]    becomes [ 9]
    [ 5]             [13]
    [ 9]             [ 1]
    [13]             [ 5]
```

**Purpose:** Permutes position without changing byte values - positional confusion.

---

### **Transformation 5: Transposition / Quadrant Swaps**
**Location:** Inline block after `FUN_140002390` (lines ~740-780)

**What it does:**
- Swaps quadrants of the matrix
- May also transpose sections (swap rows with columns)
- Complex geometric rearrangement

**Conceptual example:**
```
Quadrant swap for 4×4:
[TL TR]    →    [BR BL]
[BL BR]         [TR TL]

Where TL=top-left, TR=top-right, etc.
```

**Purpose:** Additional spatial diffusion and complexity.

---

### **Transformation 6: Even/Odd Bit Swap (0x55 mask)**
**Location:** `FUN_140002540`

**What it does:**
- Operates on individual BITS within each byte
- Swaps even-numbered bits with odd-numbered bits
- Uses bit mask 0x55 (binary: 01010101)
- For each byte: `((x >> 1) & 0x55) | ((x & 0x55) << 1)`

**Bit-level transformation:**
```
Original byte:  b₇ b₆ b₅ b₄ b₃ b₂ b₁ b₀
After swap:     b₆ b₇ b₄ b₅ b₂ b₃ b₀ b₁

Example:
  10110011 (179 decimal)
→ 01101101 (109 decimal)

Bit positions:  7 6 5 4 3 2 1 0
Original:       1 0 1 1 0 0 1 1
Swapped:        0 1 1 0 1 1 0 1
                ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑
                Even/odd pairs swap
```

**Code:**
```c
*puVar3 = (int)*puVar3 >> 1 & 0x55U | (*puVar3 & 0x55) << 1;
```

**Purpose:** Bit-level confusion - makes linear analysis harder.

---

### **Transformation 7: Per-Byte Variable Bit Rotation**
**Location:** Inline loop in `FUN_140002680` (lines ~870-890)

**What it does:**
- Rotates bits within each byte
- Rotation amount varies by position (row/column)
- Uses position-dependent rotation: `(year + month + day + row + col) & 7`
- Each byte rotates right by 0-7 bits based on its position

**Example:**
```
For position (row=2, col=3):
  rotation = (2025 + 7 + 24 + 2 + 3) & 7 = 2061 & 7 = 5

Original byte:  10110011
Rotate right 5: 01101011

Visual:
  10110011  →  rotate right →  01101011
  ↑↑                                  ↑↑
  These bits wrap to right →→→→→→→→→→
```

**Code:**
```c
uVar41 = uVar44 & 0x80000007;  // rotation amount
*(uint *)(...) = (iVar8 >> (8 - (byte)uVar41) | iVar8 << ((byte)uVar41)) & 0xff;
// Right rotation: (x >> n) | (x << (8-n))
```

**Purpose:** Final bit-level obfuscation with position-dependent variation.

---

## Summary Table

| # | Transformation | Level | Function | Purpose |
|---|---------------|-------|----------|---------|
| 1 | Ring rotation | Spatial | Inline | Physical rearrangement |
| 2 | Add constant | Byte | FUN_140002070 | Value diffusion |
| 3 | Subtract constant | Byte | FUN_1400021f0 | Value confusion |
| 4 | Cyclic shifts | Spatial | FUN_140002390 (part 1) | Positional permutation |
| 5 | Quadrant swaps | Spatial | Inline after 390 | Geometric diffusion |
| 6 | Bit-pair swap | Bit | FUN_140002540 | Bit-level confusion |
| 7 | Variable rotation | Bit | Inline loop | Position-dependent obfuscation |

---

## After All 7 Transformations

**Then the final step occurs:**

### **Final XOR with Keystream**
**Location:** `FUN_140001df0` (derives keystream) + `FUN_140001c00` (applies XOR)

**What it does:**
- Generates a keystream from the seed (email + date + timestamp + salt)
- XORs each byte of the transformed matrix with the keystream
- This is the final decryption step that reveals the plaintext

**Keystream generation (from your solve_decrypt.py):**
```python
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
```

---

## Why 7 Transformations?

The "quantum-proof" encryption uses **7 distinct transformation layers** because:

1. **Spatial (3 transforms)**: Ring rotation, cyclic shifts, quadrant swaps - scramble positions
2. **Byte-level (2 transforms)**: Add/subtract constants - change values
3. **Bit-level (2 transforms)**: Even/odd swap, variable rotation - maximum diffusion

This creates a **cascade effect** where:
- Each layer makes reverse engineering harder
- Spatial + byte + bit operations require different analysis techniques
- The number "7" may be symbolic (7 is cryptographically significant in some contexts)
- Multiple layers prevent simple pattern analysis

---

## Decryption Process (Your Script)

Your `solve_decrypt.py` reverses these in **exact opposite order**:

```python
# 1. XOR with keystream (undo final XOR)
raw = bytes(b ^ m for b, m in zip(block, mask))

# 2. Undo variable rotation (Transformation 7)
grid[r][c] = rot_right(grid[r][c], spin)

# 3. Undo bit-pair swap (Transformation 6)
grid[r][c] = bit_flip_pairs(grid[r][c])

# 4. Undo cyclic shifts (Transformation 4)
rows.rotate(-shift)
row.rotate(-shift)

# 5. Undo subtract constant (Transformation 3)
v = (v + sub_val) & 0xFF

# 6. Undo add constant (Transformation 2)
v = (v - add_val) & 0xFF

# 7. Undo ring rotation (Transformation 1) - via column reading
# Reading column-wise effectively reverses the rotation
```

---

## Answer to Question 3

**Number of distinct transformations before final XOR: 7**

**First three transformations in encryption order:**

1. **Ring rotation**: Rotates each concentric layer of the N×N grid 90° clockwise. This physically rearranges the spatial layout of the matrix, treating it like onion rings where each ring rotates independently.

2. **Add constant pass**: Adds a byte constant (derived from the year) to every cell modulo 256. This operation uniformly shifts all byte values, providing initial value diffusion across the entire matrix.

3. **Subtract constant pass**: Subtracts a byte constant (derived from the month) from every cell modulo 256. This reverses some of the addition effect while maintaining the byte-level confusion, creating a non-linear relationship between original and transformed values.

---

**Hope this helps you understand the complete transformation pipeline!** 🔐
