from fastapi import APIRouter
from pydantic import BaseModel, Field
from qrng.tests import run_all_tests

class ReportBody(BaseModel):
    bits: str = Field(..., description="Bitstring to test")
    block_size: int = 128

router = APIRouter()

@router.post("/report")
def post_report(body: ReportBody):
    res = run_all_tests(body.bits, block_size=body.block_size)
    return res
