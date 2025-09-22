from math import erfc, sqrt, log
from collections import Counter
import numpy as np
from scipy.stats import chi2

"""
QRNG Statistical Tests
----------------------
Implements a subset of NIST randomness tests for evaluating bitstreams.
Each test returns:
    - p: probability value
    - pass: whether randomness passes threshold (p >= 0.01)
    - extra metrics (depends on test)
"""

# ---------------- Monobit (Frequency) Test ----------------
def monobit_test(bits: str):
    """
    Tests balance of ones and zeros.
    """
    n = len(bits)
    if n == 0:
        return {"p": 0.0, "pass": False, "ones": 0, "zeros": 0}
    s = sum(1 if b == '1' else -1 for b in bits)
    sobs = abs(s) / sqrt(n)
    p = erfc(sobs / sqrt(2))   # complementary error function
    return {
        "p": float(p),
        "pass": p >= 0.01,
        "ones": bits.count("1"),
        "zeros": bits.count("0"),
    }


# ---------------- Runs Test ----------------
def runs_test(bits: str):
    """
    Tests whether runs of consecutive identical bits are within expected limits.
    """
    n = len(bits)
    if n < 100:
        return {"p": 0.0, "pass": False}
    pi = bits.count('1') / n
    if abs(pi - 0.5) >= 0.5 / sqrt(n):
        return {"p": 0.0, "pass": False}
    v = 1 + sum(1 for i in range(1, n) if bits[i] != bits[i - 1])
    p = erfc(abs(v - 2 * n * pi * (1 - pi)) / (2 * sqrt(2 * n) * pi * (1 - pi)))
    return {"p": float(p), "pass": p >= 0.01}


# ---------------- Block Frequency Test ----------------
def block_frequency_test(bits: str, M=128):
    """
    Splits bitstring into blocks and checks frequency of ones.
    """
    n = len(bits)
    if n < M:
        return {"p": 0.0, "pass": False, "block_means": []}
    N = n // M
    chisq = 0.0
    block_means = []
    for i in range(N):
        block = bits[i * M:(i + 1) * M]
        pi = block.count('1') / M
        block_means.append(pi)
        chisq += 4 * M * ((pi - 0.5) ** 2)
    p = chi2.sf(chisq, df=N)  # survival function = 1 - cdf
    return {
        "p": float(p),
        "pass": p >= 0.01,
        "blocks": N,
        "M": M,
        "block_means": block_means,
    }


# ---------------- Serial Test ----------------
def serial_test(bits: str):
    """
    Tests frequency of 2-bit patterns (00,01,10,11).
    """
    n = len(bits)
    if n < 1000:
        return {"p": 0.0, "pass": False}
    pairs = [bits[i:i + 2] for i in range(0, n - 1)]
    c = Counter(pairs)
    expected = (n - 1) / 4
    chisq = sum((c.get(p, 0) - expected) ** 2 / expected for p in ['00', '01', '10', '11'])
    p = chi2.sf(chisq, df=3)  # df = 4-1 = 3
    return {"p": float(p), "pass": p >= 0.01}


# ---------------- Approximate Entropy Test ----------------
def approximate_entropy(bits: str, m=2):
    """
    Tests unpredictability of patterns of length m and m+1.
    """
    n = len(bits)
    if n < 1000:
        return {"value": 0.0, "p": 0.0, "pass": False, "max": log(2)}

    def _phi(m):
        c = Counter(bits[i:i + m] for i in range(n - m + 1))
        tot = n - m + 1
        return sum((v / tot) * log(v / tot) for v in c.values())

    phi_m = _phi(m)
    phi_m1 = _phi(m + 1)
    ap_en = phi_m - phi_m1
    chisq = 2 * n * (log(2) - ap_en)
    df = (2 ** m) - 1
    p = chi2.sf(chisq, df=df)
    return {
        "value": float(ap_en),
        "p": float(p),
        "pass": p >= 0.01,
        "max": log(2),
    }


# ---------------- Autocorrelation Test ----------------
def autocorrelation(bits: str, lags=(1, 2, 8, 16, 32)):
    """
    Tests correlation between bits separated by lag.
    """
    n = len(bits)
    if n < max(lags) * 2:
        return {"corr": {}, "pass": False, "lags": list(lags)}
    x = np.fromiter((1 if b == '1' else 0 for b in bits), dtype=np.int8, count=n)
    results = {}
    passes = []
    for k in lags:
        a = x[:-k]
        b = x[k:]
        corr = float(np.corrcoef(a, b)[0, 1])
        results[k] = corr
        passes.append(abs(corr) < 0.02)  # heuristic threshold
    return {"corr": results, "pass": all(passes), "lags": list(lags)}


# ---------------- Run All Tests ----------------
def run_all_tests(bits: str, block_size: int = 128):
    """
    Runs all randomness tests and aggregates results.
    """
    return {
        "n": len(bits),
        "frequency_test": monobit_test(bits),              # ones/zeros balance
        "runs_test": runs_test(bits),                      # runs distribution
        "block_frequency": block_frequency_test(bits, M=block_size),  # per-block uniformity
        "serial_test": serial_test(bits),                  # 2-bit pattern distribution
        "entropy": approximate_entropy(bits, m=2),         # entropy measure
        "autocorrelation": autocorrelation(bits),          # lag correlation
    }
