from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import hashlib
import math

# Routers
from routers import bits, extract, key, report, download

app = FastAPI(
    title="QRNG Backend",
    version="1.1.0",
    description="Quantum Random Number Generator Backend with Bias Reduction"
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Register Routers
# -----------------------------
app.include_router(bits.router, prefix="/api")
app.include_router(extract.router, prefix="/api")
app.include_router(key.router, prefix="/api")
app.include_router(report.router, prefix="/api")
app.include_router(download.router, prefix="/api")  # 🔥 Download feature

# -----------------------------
# CHARSETS
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
# Helper Functions
# -----------------------------
def _bits_to_bytes_via_shake(bits: str) -> bytes:
    """
    Convert bitstring to bytes using SHAKE-256
    (cryptographic conditioning, unbiased)
    """
    byte_len = math.ceil(len(bits) / 8)
    return hashlib.shake_256(bits.encode()).digest(byte_len)


def _unbiased_tokens(length: int, alphabet: str, bits: str) -> str:
    """
    Generate unbiased token from bitstream + charset
    """
    used_bytes = _bits_to_bytes_via_shake(bits)
    token = ""

    for b in used_bytes:
        idx = b % len(alphabet)
        token += alphabet[idx]
        if len(token) >= length:
            break

    return token

# -----------------------------
# Token Generation Endpoint
# -----------------------------
@app.post("/api/token")
def generate_token(req: TokenRequest):
    alphabet = CHARSETS.get(req.kind)
    if not alphabet:
        return {"error": f"Invalid kind: {req.kind}"}

    # Use provided bits or fallback
    if req.bits:
        bits = req.bits
    else:
        # ⚠️ Replace with real QRNG call if needed
        bits = "1010101110001111" * 256

    token = _unbiased_tokens(req.length, alphabet, bits)

    return {
        "kind": req.kind,
        "length": req.length,
        "token": token,
        "used_bits": len(bits),
        "alphabet_size": len(alphabet),
    }

# -----------------------------
# Health & Root
# -----------------------------
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
