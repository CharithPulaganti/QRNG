from fastapi import APIRouter, Query
from qrng.generator import generate_bits

router = APIRouter()

@router.get("/bits")
def get_bits(n: int = Query(100000, ge=1, le=5_000_000)):
    bits, meta = generate_bits(n)
    return {"bits": bits, "count": n, **meta}
