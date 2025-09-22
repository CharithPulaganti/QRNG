from fastapi import APIRouter
from pydantic import BaseModel, Field
from qrng.extractor import von_neumann, sha256_extractor

class ExtractBody(BaseModel):
    bits: str = Field(..., description="Raw bitstring")
    method: str = Field("sha256", description="von_neumann | sha256")

router = APIRouter()

@router.post("/extract")
def post_extract(body: ExtractBody):
    if body.method == "von_neumann":
        out = von_neumann(body.bits)
        method = "von_neumann"
    else:
        out = sha256_extractor(body.bits)
        method = "sha256"
    return {"method": method, "input_len": len(body.bits), "output_len": len(out), "bits": out}
