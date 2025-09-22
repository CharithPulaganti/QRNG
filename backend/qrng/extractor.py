from hashlib import sha256

def von_neumann(bits: str) -> str:
    # pairs: 01 -> 0, 10 -> 1, 00/11 discarded
    out = []
    it = iter(bits)
    for a in it:
        try:
            b = next(it)
        except StopIteration:
            break
        if a == '0' and b == '1':
            out.append('0')
        elif a == '1' and b == '0':
            out.append('1')
        # else drop
    return ''.join(out)

def sha256_extractor(bits: str) -> str:
    # Hash blocks of 4096 bits → 256-bit digest, concatenated
    out = []
    blk = 4096
    for i in range(0, len(bits), blk):
        chunk = bits[i:i+blk]
        # Convert bitstring to bytes
        if not chunk:
            continue
        by = int(chunk, 2).to_bytes((len(chunk)+7)//8, byteorder="big")
        digest = sha256(by).digest()  # 256 bits
        # Convert digest to bits
        out.append(''.join(f'{b:08b}' for b in digest))
    return ''.join(out)
