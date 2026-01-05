from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import FileResponse

from qrng.generator import generate_bits
from qrng.extractor import von_neumann, sha256_extractor
from storage import save_txt, save_bin

router = APIRouter(
    prefix="/download",
    tags=["Download"]
)


def _normalize_bits(bits):
    """
    Ensure bits is a string.
    Handles cases where generator returns tuples.
    """
    if isinstance(bits, tuple):
        return bits[0]
    return bits


@router.get("/raw/txt")
def download_raw_txt(
    n: int = Query(1024, gt=0, le=100000)
):
    raw_bits = generate_bits(n)
    raw_bits = _normalize_bits(raw_bits)

    if not raw_bits:
        raise HTTPException(status_code=500, detail="No bits generated")

    file_path = save_txt(raw_bits)

    return FileResponse(
        path=file_path,
        media_type="text/plain",
        filename="qrng_raw_bits.txt"
    )


@router.get("/final/txt")
def download_final_txt(
    n: int = Query(1024, gt=0, le=100000),
    method: str = Query("sha256", enum=["vn", "sha256"])
):
    raw_bits = _normalize_bits(generate_bits(n))

    if method == "vn":
        final_bits = von_neumann(raw_bits)
    else:
        final_bits = sha256_extractor(von_neumann(raw_bits))

    if not final_bits:
        raise HTTPException(
            status_code=500,
            detail="Extraction produced empty output. Increase n."
        )

    file_path = save_txt(final_bits)

    return FileResponse(
        path=file_path,
        media_type="text/plain",
        filename="qrng_extracted_bits.txt"
    )


@router.get("/final/bin")
def download_final_bin(
    n: int = Query(1024, gt=0, le=100000),
    method: str = Query("sha256", enum=["vn", "sha256"])
):
    raw_bits = _normalize_bits(generate_bits(n))

    if method == "vn":
        final_bits = von_neumann(raw_bits)
    else:
        final_bits = sha256_extractor(von_neumann(raw_bits))

    if not final_bits:
        raise HTTPException(
            status_code=500,
            detail="Extraction produced empty output. Increase n."
        )

    file_path = save_bin(final_bits)

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename="qrng_extracted_bits.bin"
    )
