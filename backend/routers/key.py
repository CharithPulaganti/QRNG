from fastapi import APIRouter, Query
from qrng.generator import generate_bits
from qrng.extractor import sha256_extractor
import hashlib

router = APIRouter()

@router.get("/key")
def get_key(length: int = Query(256, ge=64, le=4096), method: str = "sha256"):
    # generate raw bits >= length*2, then extract via SHA256 until enough bits
    need = length * 2
    raw, meta = generate_bits(need)
    refined = sha256_extractor(raw)
    # Ensure we have enough bits
    while len(refined) < length:
        extra_raw, _ = generate_bits(need)
        refined += sha256_extractor(extra_raw)
    key_bits = refined[:length]
    # present as hex
    # chunk bits into bytes
    by = int(key_bits, 2).to_bytes(length // 8, byteorder="big")
    hexkey = by.hex()
    checksum = hashlib.sha256(by).hexdigest()[:16]
    return {"length": length, "hex": hexkey, "checksum": checksum, **meta}
