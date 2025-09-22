from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from qrng.tests import run_all_tests
import numpy as np

# ---------------- Request Schema ----------------
class ReportBody(BaseModel):
    bits: str = Field(..., description="Bitstring to test")
    block_size: int = Field(128, description="Block size for block frequency test")


router = APIRouter()


# ---------------- Helper: Convert numpy → Python types ----------------
def to_python_type(val):
    if isinstance(val, (np.bool_, bool)):
        return bool(val)
    if isinstance(val, (np.integer,)):
        return int(val)
    if isinstance(val, (np.floating,)):
        return float(val)
    return val


def clean_dict(d):
    if isinstance(d, dict):
        return {k: clean_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [clean_dict(v) for v in d]
    else:
        return to_python_type(d)


# ---------------- Route ----------------
@router.post("/report")
def post_report(body: ReportBody):
    bits = body.bits.strip()

    if not bits:
        raise HTTPException(status_code=400, detail="Bitstring is empty.")

    # ✅ run all randomness tests
    res = run_all_tests(bits, block_size=body.block_size)

    # ✅ clean numpy / float64 / int64 → Python
    cleaned = clean_dict(res)

    # ✅ Add summary
    summary = {
        "total_bits": len(bits),
        "passed_tests": sum(1 for k, v in cleaned.items() if isinstance(v, dict) and v.get("pass") is True),
        "failed_tests": sum(1 for k, v in cleaned.items() if isinstance(v, dict) and v.get("pass") is False),
        "total_tests": sum(1 for k, v in cleaned.items() if isinstance(v, dict) and "pass" in v),
    }

    return {
        "summary": summary,
        "results": cleaned,
    }
