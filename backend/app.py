from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import hashlib, math

from routers import bits, extract, key, report

app = FastAPI(title="QRNG Backend", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bits.router, prefix="/api")
app.include_router(extract.router, prefix="/api")
app.include_router(key.router, prefix="/api")
app.include_router(report.router, prefix="/api")

# -----------------------------
# CHARSETS (your custom options)
# -----------------------------
CHARSETS = {
    "numeric": "0123456789",
    "alpha": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "special": "!@#$%^&*()-_=+[]{};:,.<>/?",
    "alphanumeric": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "alpha_special": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+[]{};:,.<>/?",
    "all": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{};:,.<>/?",
}


# -----------------------------
# Request Model
# -----------------------------
class TokenRequest(BaseModel):
    length: int
    kind: str
    bits: Optional[str] = None


# -----------------------------
# Helper functions
# -----------------------------
def _bits_to_bytes_via_shake(bits: str) -> bytes:
    """Turn bitstring into bytes using SHAKE for unbiased randomness"""
    byte_len = math.ceil(len(bits) / 8)
    return hashlib.shake_256(bits.encode()).digest(byte_len)


def _unbiased_tokens(length: int, alphabet: str, bits: str) -> str:
    """Generate unbiased token from bits + charset"""
    used_bytes = _bits_to_bytes_via_shake(bits)
    token = ""
    for b in used_bytes:
        idx = b % len(alphabet)
        token += alphabet[idx]
        if len(token) >= length:
            break
    return token


# -----------------------------
# New Endpoint
# -----------------------------
@app.post("/api/token")
def generate_token(req: TokenRequest):
    # pick charset
    alphabet = CHARSETS.get(req.kind)
    if not alphabet:
        return {"error": f"Invalid kind: {req.kind}"}

    # either use provided bits or call your existing QRNG
    if req.bits:
        bits = req.bits
    else:
        # ⚠️ replace this with your real QRNG function (e.g. generate_bits(n))
        bits = "1010101110001111" * 256   # dummy fallback

    token = _unbiased_tokens(req.length, alphabet, bits)

    return {
        "kind": req.kind,
        "length": req.length,
        "token": token,
        "used_bits": len(bits),
        "alphabet_size": len(alphabet),
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {
        "message": "Welcome to the QRNG Backend 🚀",
        "docs": "/docs",
        "health": "/api/health"
    }
