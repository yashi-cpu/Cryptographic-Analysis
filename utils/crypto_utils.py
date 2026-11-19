import math
import numpy as np

def text_to_binary(text: str) -> str:
    """Convert a text string to its UTF-8 binary representation (8 bits per byte)."""
    return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))

def binary_to_text(binary_str: str) -> str:
    """Convert binary string back to UTF-8 text safely."""
    if len(binary_str) % 8 != 0:
        binary_str = binary_str[:len(binary_str) - (len(binary_str) % 8)]
    byte_arr = bytearray(
        int(binary_str[i:i+8], 2)
        for i in range(0, len(binary_str), 8)
    )
    return byte_arr.decode('utf-8', errors='replace')

def calculate_entropy(data: str, is_binary: bool = True) -> float:
    """
    Calculate Shannon entropy.
    If is_binary, entropy is per-bit in [0, 1].
    If text/bytes, entropy is per-byte in [0, 8].
    """
    if not data:
        return 0.0
    if is_binary:
        p1 = data.count('1') / len(data)
        p0 = 1.0 - p1
        entropy = 0.0
        if p1 > 0:
            entropy -= p1 * math.log2(p1)
        if p0 > 0:
            entropy -= p0 * math.log2(p0)
        return entropy
    else:
        # byte-level entropy
        byte_counts = {}
        for char in data:
            byte_counts[char] = byte_counts.get(char, 0) + 1
        entropy = 0.0
        n = len(data)
        for count in byte_counts.values():
            p = count / n
            entropy -= p * math.log2(p)
        return entropy

def calculate_avalanche_effect(cipher1: str, cipher2: str) -> dict:
    """
    Calculates bitwise differences between two ciphertexts (binary strings).
    Returns Hamming distance, total bits, and percentage flipped.
    """
    length = min(len(cipher1), len(cipher2))
    if length == 0:
        return {"hamming_distance": 0, "total_bits": 0, "flip_percentage": 0.0, "diff_indices": []}
    
    diff_indices = [i for i in range(length) if cipher1[i] != cipher2[i]]
    hamming_dist = len(diff_indices)
    percentage = (hamming_dist / length) * 100.0
    return {
        "hamming_distance": hamming_dist,
        "total_bits": length,
        "flip_percentage": percentage,
        "diff_indices": diff_indices
    }

def flip_bit(binary_str: str, index: int) -> str:
    """Flip a single bit at the given index."""
    if not binary_str:
        return binary_str
    index = index % len(binary_str)
    flipped = '0' if binary_str[index] == '1' else '1'
    return binary_str[:index] + flipped + binary_str[index+1:]

def basic_xor_encrypt(binary_message: str, key: str) -> tuple[str, str]:
    """Basic XOR stream encryption with a repeating string key."""
    key_binary = text_to_binary(key)
    if not key_binary:
        key_binary = "00000000"
    keystream = ''.join(key_binary[i % len(key_binary)] for i in range(len(binary_message)))
    ciphertext = ''.join(str(int(binary_message[i]) ^ int(keystream[i])) for i in range(len(binary_message)))
    return ciphertext, keystream

