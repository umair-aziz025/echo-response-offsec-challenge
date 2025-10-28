#!/usr/bin/env python3
from pathlib import Path
from collections import deque

EMAIL = "megacorp@quantum.com"
DATE = "24.07.2025"
SALT = "PublicSalt"
FILE = Path("QuantumConundrum_Project/decrypt_me.txt.enc")

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

    for r in range(n):
        for c in range(n):
            spin = (year + month + day + r + c) & 7
            if spin:
                grid[r][c] = rot_right(grid[r][c], spin)

    for r in range(n):
        for c in range(n):
            grid[r][c] = bit_flip_pairs(grid[r][c])

    shift = day % n
    if shift:
        rows = deque(grid)
        rows.rotate(-shift)
        grid = [list(row) for row in rows]
        for r in range(n):
            row = deque(grid[r])
            row.rotate(-shift)
            grid[r] = list(row)

    add_val = year & 0xFF
    sub_val = month
    for r in range(n):
        for c in range(n):
            v = grid[r][c]
            v = (v + sub_val) & 0xFF
            v = (v - add_val) & 0xFF
            grid[r][c] = v

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
