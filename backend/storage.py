# backend/storage.py
import os
from datetime import datetime

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_txt(bits: str) -> str:
    filename = f"qrng_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w") as f:
        f.write(bits)
    return path

def save_bin(bits: str) -> str:
    filename = f"qrng_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.bin"
    path = os.path.join(OUTPUT_DIR, filename)
    byte_data = int(bits, 2).to_bytes((len(bits) + 7)//8, byteorder="big")
    with open(path, "wb") as f:
        f.write(byte_data)
    return path
