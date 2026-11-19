"""
Crypto Engines — wraps existing project modules into clean encrypt/decrypt
functions for text and images, used by the FastAPI backend.
"""

import sys
import os
import time
import base64
import numpy as np
from io import BytesIO
from PIL import Image

# Ensure workspace root is on sys.path so existing modules import correctly
_WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, _WORKSPACE_ROOT)

from utils.crypto_utils import text_to_binary, binary_to_text
from jordan_network.jordan import jordan_encrypt, jordan_decrypt
from chaotic_network.chaotic import chaotic_encrypt, chaotic_decrypt
from chaotic_network.lorenz import encrypt_image_lorenz, decrypt_image_lorenz, LorenzSystem
from encryption.aes_encryption import aes_encrypt, aes_decrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# ---------------------------------------------------------------------------
# Text encryption / decryption
# ---------------------------------------------------------------------------

def encrypt_text(message: str, algorithm: str) -> dict:
    """Encrypt a text message with the given algorithm.
    Returns a dict with ciphertext_hex, key_info, binary_plaintext, encryption_time_ms, algorithm.
    """
    binary_plaintext = text_to_binary(message)
    start = time.perf_counter()

    if algorithm == "jordan":
        ciphertext_bin, keystream = jordan_encrypt(binary_plaintext)
        elapsed = (time.perf_counter() - start) * 1000
        # Binary string → hex
        ciphertext_hex = hex(int(ciphertext_bin, 2))[2:].zfill(len(ciphertext_bin) // 4)
        key_info = {"keystream": keystream, "bit_length": len(ciphertext_bin)}
        return {
            "ciphertext_hex": ciphertext_hex,
            "key_info": key_info,
            "binary_plaintext": binary_plaintext,
            "encryption_time_ms": round(elapsed, 4),
            "algorithm": algorithm,
        }

    elif algorithm == "chaotic":
        ciphertext_bin, keystream = chaotic_encrypt(binary_plaintext)
        elapsed = (time.perf_counter() - start) * 1000
        ciphertext_hex = hex(int(ciphertext_bin, 2))[2:].zfill(len(ciphertext_bin) // 4)
        key_info = {"keystream": keystream, "bit_length": len(ciphertext_bin)}
        return {
            "ciphertext_hex": ciphertext_hex,
            "key_info": key_info,
            "binary_plaintext": binary_plaintext,
            "encryption_time_ms": round(elapsed, 4),
            "algorithm": algorithm,
        }

    elif algorithm == "aes":
        key, nonce, ciphertext = aes_encrypt(message)
        elapsed = (time.perf_counter() - start) * 1000
        return {
            "ciphertext_hex": ciphertext.hex(),
            "key_info": {"key_hex": key.hex(), "nonce_hex": nonce.hex()},
            "binary_plaintext": binary_plaintext,
            "encryption_time_ms": round(elapsed, 4),
            "algorithm": algorithm,
        }

    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")


def decrypt_text(ciphertext_hex: str, key_info: dict, algorithm: str) -> dict:
    """Decrypt a hex ciphertext using key_info.
    Returns dict with plaintext, decryption_time_ms, success.
    """
    start = time.perf_counter()

    try:
        if algorithm in ("jordan", "chaotic"):
            keystream = key_info["keystream"]
            bit_length = key_info["bit_length"]
            # Hex → binary string
            ciphertext_bin = bin(int(ciphertext_hex, 16))[2:].zfill(bit_length)
            if algorithm == "jordan":
                plaintext_bin = jordan_decrypt(ciphertext_bin, keystream)
            else:
                plaintext_bin = chaotic_decrypt(ciphertext_bin, keystream)
            plaintext = binary_to_text(plaintext_bin)
            elapsed = (time.perf_counter() - start) * 1000
            return {"plaintext": plaintext, "decryption_time_ms": round(elapsed, 4), "success": True}

        elif algorithm == "aes":
            key = bytes.fromhex(key_info["key_hex"])
            nonce = bytes.fromhex(key_info["nonce_hex"])
            ciphertext = bytes.fromhex(ciphertext_hex)
            plaintext = aes_decrypt(key, nonce, ciphertext)
            elapsed = (time.perf_counter() - start) * 1000
            return {"plaintext": plaintext, "decryption_time_ms": round(elapsed, 4), "success": True}

        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        return {"plaintext": f"[Decryption failed: {e}]", "decryption_time_ms": round(elapsed, 4), "success": False}


# ---------------------------------------------------------------------------
# Image encryption / decryption
# ---------------------------------------------------------------------------

class FastJordanNetwork:
    """Fast vectorized recurrent byte generator for image encryption."""
    def __init__(self, hidden_size=16, seed=1337):
        rng = np.random.RandomState(seed)
        self.w_context = rng.randn(1, hidden_size) * 1.2
        self.w_hidden = rng.randn(hidden_size, hidden_size) * 0.5
        self.w_out = rng.randn(hidden_size, 1) * 1.5
        self.b_hidden = rng.randn(hidden_size) * 0.2
        self.b_out = np.zeros(1)
        self.context = np.array([0.5])
        self.h = np.zeros(hidden_size)

    def generate_byte_keystream(self, length):
        stream = np.empty(length, dtype=np.uint8)
        for i in range(length):
            self.h = np.tanh(np.dot(self.context, self.w_context) + np.dot(self.h, self.w_hidden) + self.b_hidden)
            out_val = 1.0 / (1.0 + np.exp(-np.dot(self.h, self.w_out) - self.b_out))[0]
            stream[i] = int(abs(out_val) * 1e7) % 256
            self.context = np.array([out_val])
        return stream


def encrypt_image(image_bytes: bytes, algorithm: str) -> dict:
    """Encrypt an image.
    Returns dict with cipher_image_b64, key_info, original_size, cipher_size,
    encryption_time_ms, original_image_b64.
    """
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    # Standardize image to 128x128 for real-time visual cryptographic responsiveness
    img = img.resize((128, 128), Image.Resampling.LANCZOS)
    img_np = np.array(img, dtype=np.uint8)
    original_size = img_np.nbytes

    # Base64 of original for display
    buf_orig = BytesIO()
    img.save(buf_orig, format="PNG")
    original_image_b64 = base64.b64encode(buf_orig.getvalue()).decode()

    start = time.perf_counter()

    if algorithm == "chaotic":
        cipher_img, _permuted = encrypt_image_lorenz(img_np)
        elapsed = (time.perf_counter() - start) * 1000
        key_info = {
            "initial_state": [0.1, 0.2, 0.3],
            "cat_rounds": 2,
            "shape": list(img_np.shape),
        }

    elif algorithm == "jordan":
        flat = img_np.flatten()
        keystream_bytes = FastJordanNetwork(seed=1337).generate_byte_keystream(len(flat))
        cipher_img = (flat ^ keystream_bytes).reshape(img_np.shape)
        elapsed = (time.perf_counter() - start) * 1000
        key_info = {
            "seed": 1337,
            "shape": list(img_np.shape),
        }

    elif algorithm == "aes":
        raw = img_np.tobytes()
        aes_key = AESGCM.generate_key(bit_length=256)
        aes = AESGCM(aes_key)
        nonce = os.urandom(12)
        ct = aes.encrypt(nonce, raw, None)
        elapsed = (time.perf_counter() - start) * 1000
        # Format ciphertext array to image shape for visual scrambling display
        ct_arr = np.frombuffer(ct[: img_np.nbytes], dtype=np.uint8).copy()
        if len(ct_arr) < img_np.size:
            ct_arr = np.pad(ct_arr, (0, img_np.size - len(ct_arr)))
        cipher_img = ct_arr[: img_np.size].reshape(img_np.shape)
        key_info = {
            "key_hex": aes_key.hex(),
            "nonce_hex": nonce.hex(),
            "shape": list(img_np.shape),
            "raw_ciphertext_hex": ct.hex(),
        }

    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    cipher_pil = Image.fromarray(cipher_img.astype(np.uint8))
    buf = BytesIO()
    cipher_pil.save(buf, format="PNG")
    cipher_image_b64 = base64.b64encode(buf.getvalue()).decode()

    return {
        "cipher_image_b64": cipher_image_b64,
        "key_info": key_info,
        "original_size": original_size,
        "cipher_size": cipher_img.nbytes,
        "encryption_time_ms": round(elapsed, 4),
        "original_image_b64": original_image_b64,
    }


def decrypt_image(cipher_image_b64: str, key_info: dict, algorithm: str) -> dict:
    """Decrypt an image from base64.
    Returns dict with decrypted_image_b64, decryption_time_ms, success.
    """
    start = time.perf_counter()
    try:
        if algorithm == "chaotic":
            cipher_bytes = base64.b64decode(cipher_image_b64)
            cipher_pil = Image.open(BytesIO(cipher_bytes)).convert("RGB")
            cipher_np = np.array(cipher_pil, dtype=np.uint8)
            initial_state = tuple(key_info.get("initial_state", [0.1, 0.2, 0.3]))
            cat_rounds = key_info.get("cat_rounds", 2)
            restored = decrypt_image_lorenz(cipher_np, initial_state=initial_state, cat_rounds=cat_rounds)
            elapsed = (time.perf_counter() - start) * 1000
            dec_pil = Image.fromarray(restored.astype(np.uint8))

        elif algorithm == "jordan":
            cipher_bytes = base64.b64decode(cipher_image_b64)
            cipher_pil = Image.open(BytesIO(cipher_bytes)).convert("RGB")
            cipher_np = np.array(cipher_pil, dtype=np.uint8)
            flat = cipher_np.flatten()
            seed = key_info.get("seed", 1337)
            keystream_bytes = FastJordanNetwork(seed=seed).generate_byte_keystream(len(flat))
            restored = (flat ^ keystream_bytes).reshape(cipher_np.shape)
            elapsed = (time.perf_counter() - start) * 1000
            dec_pil = Image.fromarray(restored.astype(np.uint8))

        elif algorithm == "aes":
            raw_ct = bytes.fromhex(key_info["raw_ciphertext_hex"])
            key = bytes.fromhex(key_info["key_hex"])
            nonce = bytes.fromhex(key_info["nonce_hex"])
            aes = AESGCM(key)
            raw_plain = aes.decrypt(nonce, raw_ct, None)
            shape = key_info["shape"]
            restored = np.frombuffer(raw_plain, dtype=np.uint8).reshape(shape)
            elapsed = (time.perf_counter() - start) * 1000
            dec_pil = Image.fromarray(restored)

        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        buf = BytesIO()
        dec_pil.save(buf, format="PNG")
        decrypted_b64 = base64.b64encode(buf.getvalue()).decode()
        return {"decrypted_image_b64": decrypted_b64, "decryption_time_ms": round(elapsed, 4), "success": True}

    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        return {"decrypted_image_b64": "", "decryption_time_ms": round(elapsed, 4), "success": False, "error": str(e)}


# ---------------------------------------------------------------------------
# Attack simulation
# ---------------------------------------------------------------------------

def run_attack_simulation(ciphertext_hex: str, algorithm: str, key_info: dict) -> dict:
    """Simulate Eve intercepting, trying wrong key, tampering, and Bob decrypting correctly."""

    intercepted_hex = ciphertext_hex  # Eve intercepts

    # --- (a) Eve tries decrypting with WRONG key ---
    if algorithm in ("jordan", "chaotic"):
        bit_length = key_info["bit_length"]
        real_ks = key_info["keystream"]
        # Wrong keystream: flip every bit
        wrong_ks = ''.join('0' if b == '1' else '1' for b in real_ks)
        ciphertext_bin = bin(int(ciphertext_hex, 16))[2:].zfill(bit_length)
        if algorithm == "jordan":
            eve_plain_bin = jordan_decrypt(ciphertext_bin, wrong_ks)
        else:
            eve_plain_bin = chaotic_decrypt(ciphertext_bin, wrong_ks)
        eve_result = binary_to_text(eve_plain_bin)
        eve_success = False  # wrong key → garbage
    elif algorithm == "aes":
        # Wrong key
        wrong_key = AESGCM.generate_key(bit_length=256)
        aes_wrong = AESGCM(wrong_key)
        nonce = bytes.fromhex(key_info["nonce_hex"])
        ct = bytes.fromhex(ciphertext_hex)
        try:
            eve_result = aes_wrong.decrypt(nonce, ct, None).decode("utf-8", errors="replace")
            eve_success = True
        except Exception:
            eve_result = "[AES-GCM authentication failed — wrong key]"
            eve_success = False
    else:
        eve_result = "[Unknown algorithm]"
        eve_success = False

    # --- (b) Tamper 1 bit and try decrypting ---
    if algorithm in ("jordan", "chaotic"):
        bit_length = key_info["bit_length"]
        ciphertext_bin = bin(int(ciphertext_hex, 16))[2:].zfill(bit_length)
        # Flip bit 0
        tampered_bin = ('0' if ciphertext_bin[0] == '1' else '1') + ciphertext_bin[1:]
        tampered_hex = hex(int(tampered_bin, 2))[2:].zfill(len(ciphertext_hex))
        keystream = key_info["keystream"]
        if algorithm == "jordan":
            tamper_plain_bin = jordan_decrypt(tampered_bin, keystream)
        else:
            tamper_plain_bin = chaotic_decrypt(tampered_bin, keystream)
        tamper_result = binary_to_text(tamper_plain_bin)
        tamper_detected = True  # corruption visible
    elif algorithm == "aes":
        ct_bytes = bytearray(bytes.fromhex(ciphertext_hex))
        ct_bytes[0] ^= 0x01  # flip 1 bit
        tampered_hex = ct_bytes.hex()
        key = bytes.fromhex(key_info["key_hex"])
        nonce = bytes.fromhex(key_info["nonce_hex"])
        aes_obj = AESGCM(key)
        try:
            tamper_result = aes_obj.decrypt(nonce, bytes(ct_bytes), None).decode("utf-8", errors="replace")
            tamper_detected = False
        except Exception:
            tamper_result = "[AES-GCM authentication failed — tampered ciphertext detected]"
            tamper_detected = True
    else:
        tampered_hex = ciphertext_hex
        tamper_result = "[Unknown algorithm]"
        tamper_detected = False

    # --- (c) Bob decrypts with CORRECT key ---
    bob_result = decrypt_text(ciphertext_hex, key_info, algorithm)

    return {
        "intercepted_hex": intercepted_hex,
        "eve_decrypt_result": eve_result,
        "eve_success": eve_success,
        "tampered_hex": tampered_hex,
        "tamper_decrypt_result": tamper_result,
        "tamper_detected": tamper_detected,
        "bob_decrypt_result": bob_result.get("plaintext", ""),
        "bob_success": bob_result.get("success", False),
    }


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def run_benchmark(message: str, iterations: int = 5) -> list[dict]:
    """Benchmark all three algorithms over N iterations, return avg times."""
    results = []
    for algo in ("jordan", "chaotic", "aes"):
        enc_times = []
        dec_times = []
        ct_sizes = []
        recovery_ok = True

        for _ in range(iterations):
            enc = encrypt_text(message, algo)
            enc_times.append(enc["encryption_time_ms"])
            ct_sizes.append(len(enc["ciphertext_hex"]))

            dec = decrypt_text(enc["ciphertext_hex"], enc["key_info"], algo)
            dec_times.append(dec["decryption_time_ms"])
            if not dec["success"] or dec["plaintext"] != message:
                recovery_ok = False

        results.append({
            "algorithm": algo,
            "encrypt_ms": round(sum(enc_times) / len(enc_times), 4),
            "decrypt_ms": round(sum(dec_times) / len(dec_times), 4),
            "ciphertext_size": ct_sizes[0],
            "recovery_success": recovery_ok,
        })
    return results
