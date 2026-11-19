import math
import numpy as np


def _gammaincc(a: float, x: float) -> float:
    """
    Regularized upper incomplete gamma function Q(a, x) = Gamma(a, x) / Gamma(a).
    Standard numerical recipes implementation for NIST chi-square p-value calculations.
    """
    if x < 0.0 or a <= 0.0:
        return 0.0
    if x == 0.0:
        return 1.0

    gln = math.lgamma(a)
    if x < a + 1.0:
        # Series expansion for lower incomplete gamma P(a, x)
        ap = a
        sum_val = 1.0 / a
        del_val = sum_val
        for _ in range(120):
            ap += 1.0
            del_val *= x / ap
            sum_val += del_val
            if abs(del_val) < abs(sum_val) * 1e-15:
                break
        P = sum_val * math.exp(-x + a * math.log(x) - gln)
        return max(0.0, min(1.0, 1.0 - P))
    else:
        # Continued fraction for upper incomplete gamma Q(a, x)
        b = x + 1.0 - a
        c = 1.0 / 1e-30
        d = 1.0 / b
        h = d
        for i in range(1, 121):
            an = -i * (i - a)
            b += 2.0
            d = an * d + b
            if abs(d) < 1e-30:
                d = 1e-30
            c = b + an / c
            if abs(c) < 1e-30:
                c = 1e-30
            d = 1.0 / d
            del_val = d * c
            h *= del_val
            if abs(del_val - 1.0) < 1e-15:
                break
        Q = math.exp(-x + a * math.log(x) - gln) * h
        return max(0.0, min(1.0, Q))


# -------------------------------------------------------------
# NIST SP 800-22 Cryptographic Randomness Tests
# -------------------------------------------------------------

def nist_monobit_frequency_test(bin_sequence: str) -> dict:
    """
    NIST Test 1: Frequency (Monobit) Test.
    Tests whether the ratio of 0s and 1s is approximately 0.5.
    """
    n = len(bin_sequence)
    if n < 10:
        return {"test": "Monobit Frequency", "statistic": 0.0, "p_value": 0.0, "passed": False}
    
    # Map '1' -> +1, '0' -> -1
    sn = sum(1 if b == '1' else -1 for b in bin_sequence)
    s_obs = abs(sn) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    
    return {
        "test": "Monobit Frequency",
        "statistic": float(s_obs),
        "p_value": float(p_value),
        "passed": bool(p_value >= 0.01)
    }


def nist_block_frequency_test(bin_sequence: str, block_size: int = 128) -> dict:
    """
    NIST Test 2: Frequency Test within a Block.
    Evaluates proportion of ones within M-bit blocks.
    """
    n = len(bin_sequence)
    if n < block_size:
        block_size = max(16, n // 4)
    if block_size <= 0:
        return {"test": "Block Frequency", "statistic": 0.0, "p_value": 0.0, "passed": False}

    num_blocks = n // block_size
    if num_blocks == 0:
        return {"test": "Block Frequency", "statistic": 0.0, "p_value": 0.0, "passed": False}

    proportions = []
    for i in range(num_blocks):
        block = bin_sequence[i * block_size : (i + 1) * block_size]
        proportions.append(block.count('1') / block_size)

    chi_squared = 4.0 * block_size * sum((pi - 0.5) ** 2 for pi in proportions)
    p_value = _gammaincc(num_blocks / 2.0, chi_squared / 2.0)

    return {
        "test": "Block Frequency",
        "statistic": float(chi_squared),
        "p_value": float(p_value),
        "passed": bool(p_value >= 0.01)
    }


def nist_runs_test(bin_sequence: str) -> dict:
    """
    NIST Test 3: Runs Test.
    Tests whether the number of runs of consecutive identical bits is as expected.
    """
    n = len(bin_sequence)
    if n < 10:
        return {"test": "Runs Test", "statistic": 0.0, "p_value": 0.0, "passed": False}

    pi = bin_sequence.count('1') / n
    # Pre-test requirement
    if abs(pi - 0.5) >= (2.0 / math.sqrt(n)):
        return {"test": "Runs Test", "statistic": 0.0, "p_value": 0.0, "passed": False}

    v_obs = 1 + sum(1 for i in range(n - 1) if bin_sequence[i] != bin_sequence[i + 1])
    numerator = abs(v_obs - 2.0 * n * pi * (1.0 - pi))
    denominator = 2.0 * math.sqrt(2.0 * n) * pi * (1.0 - pi)
    
    if denominator == 0:
        return {"test": "Runs Test", "statistic": float(v_obs), "p_value": 0.0, "passed": False}

    p_value = math.erfc(numerator / denominator)
    return {
        "test": "Runs Test",
        "statistic": float(v_obs),
        "p_value": float(p_value),
        "passed": bool(p_value >= 0.01)
    }


def nist_longest_run_of_ones_test(bin_sequence: str) -> dict:
    """
    NIST Test 4: Longest Run of Ones in a Block.
    For small/medium sequences (M=8 blocks).
    """
    n = len(bin_sequence)
    M = 8  # block size
    K = 3  # degrees of freedom - 1
    N = n // M
    if N < 16:
        return {"test": "Longest Run of Ones", "statistic": 0.0, "p_value": 0.0, "passed": False}

    # Precomputed NIST probabilities for M=8, K=3
    # Classes: <=1, 2, 3, >=4
    pi_table = [0.2148, 0.3672, 0.2305, 0.1875]
    counts = [0, 0, 0, 0]

    for i in range(N):
        block = bin_sequence[i * M : (i + 1) * M]
        max_run = 0
        cur_run = 0
        for bit in block:
            if bit == '1':
                cur_run += 1
                if cur_run > max_run:
                    max_run = cur_run
            else:
                cur_run = 0
                
        if max_run <= 1:
            counts[0] += 1
        elif max_run == 2:
            counts[1] += 1
        elif max_run == 3:
            counts[2] += 1
        else:
            counts[3] += 1

    chi_sq = sum(((counts[k] - N * pi_table[k]) ** 2) / (N * pi_table[k]) for k in range(4))
    p_value = _gammaincc(K / 2.0, chi_sq / 2.0)

    return {
        "test": "Longest Run of Ones",
        "statistic": float(chi_sq),
        "p_value": float(p_value),
        "passed": bool(p_value >= 0.01)
    }


def nist_dft_spectral_test(bin_sequence: str) -> dict:
    """
    NIST Test 5: Discrete Fourier Transform (Spectral) Test.
    Detects periodic features (repetitive patterns) in the sequence.
    """
    n = len(bin_sequence)
    if n < 10:
        return {"test": "DFT Spectral", "statistic": 0.0, "p_value": 0.0, "passed": False}

    # Convert '0'/'1' to -1, +1
    x = np.array([1 if b == '1' else -1 for b in bin_sequence], dtype=float)
    # Fast Fourier Transform
    fft_vals = np.fft.fft(x)
    mags = np.abs(fft_vals[: n // 2])
    
    # 95% peak threshold
    t_threshold = math.sqrt(2.995732274 * n)
    n0 = 0.95 * (n / 2.0)
    n1 = float(np.sum(mags < t_threshold))
    
    d = (n1 - n0) / math.sqrt(n * 0.95 * 0.05 * 0.25)
    p_value = math.erfc(abs(d) / math.sqrt(2.0))

    return {
        "test": "DFT Spectral Test",
        "statistic": float(abs(d)),
        "p_value": float(p_value),
        "passed": bool(p_value >= 0.01)
    }


def run_full_nist_suite(bin_sequence: str) -> list[dict]:
    """
    Runs the comprehensive NIST SP 800-22 test battery.
    Returns list of dicts with test name, statistic, p-value, and pass status.
    """
    return [
        nist_monobit_frequency_test(bin_sequence),
        nist_block_frequency_test(bin_sequence),
        nist_runs_test(bin_sequence),
        nist_longest_run_of_ones_test(bin_sequence),
        nist_dft_spectral_test(bin_sequence)
    ]


# -------------------------------------------------------------
# Differential Image Cryptanalysis & Correlation Metrics
# -------------------------------------------------------------

def calculate_npcr_uaci(image1: np.ndarray, image2: np.ndarray) -> dict:
    """
    Calculate NPCR (Number of Pixels Change Rate) and UACI (Unified Average Changing Intensity).
    Theoretical expectations for robust visual cryptography:
    - NPCR: > 99.609%
    - UACI: ~ 33.463%
    """
    assert image1.shape == image2.shape, "Images must have identical dimensions"
    
    diff = (image1 != image2).astype(np.float64)
    total_elements = float(image1.size)
    
    # NPCR: Percentage of differing pixels
    npcr = (np.sum(diff) / total_elements) * 100.0
    
    # UACI: Normalized absolute intensity difference
    abs_diff = np.abs(image1.astype(np.float64) - image2.astype(np.float64))
    uaci = (np.sum(abs_diff) / (total_elements * 255.0)) * 100.0
    
    return {
        "npcr": float(npcr),
        "uaci": float(uaci),
        "npcr_benchmark_met": bool(npcr >= 99.5),
        "uaci_benchmark_met": bool(30.0 <= uaci <= 36.0)
    }


def calculate_pixel_correlation(image: np.ndarray, num_samples: int = 3000) -> dict:
    """
    Calculate Pearson Adjacent Pixel Correlation Coefficient (r_xy) in:
    - Horizontal direction
    - Vertical direction
    - Diagonal direction
    Plaintext images: r_xy ~ 0.90 to 0.99 (high redundancy)
    Ciphertext images: r_xy ~ 0.00 (uncorrelated, secure)
    """
    # Convert to grayscale if 3D
    if image.ndim == 3:
        gray = 0.2989 * image[:, :, 0] + 0.5870 * image[:, :, 1] + 0.1140 * image[:, :, 2]
    else:
        gray = image.astype(np.float64)

    H, W = gray.shape
    num_samples = min(num_samples, (H - 1) * (W - 1))
    
    np.random.seed(42)
    y_coords = np.random.randint(0, H - 1, size=num_samples)
    x_coords = np.random.randint(0, W - 1, size=num_samples)

    # 1. Horizontal
    x_h = gray[y_coords, x_coords]
    y_h = gray[y_coords, x_coords + 1]
    r_h = float(np.corrcoef(x_h, y_h)[0, 1])

    # 2. Vertical
    x_v = gray[y_coords, x_coords]
    y_v = gray[y_coords + 1, x_coords]
    r_v = float(np.corrcoef(x_v, y_v)[0, 1])

    # 3. Diagonal
    x_d = gray[y_coords, x_coords]
    y_d = gray[y_coords + 1, x_coords + 1]
    r_d = float(np.corrcoef(x_d, y_d)[0, 1])

    return {
        "horizontal": r_h if not np.isnan(r_h) else 0.0,
        "vertical": r_v if not np.isnan(r_v) else 0.0,
        "diagonal": r_d if not np.isnan(r_d) else 0.0
    }
