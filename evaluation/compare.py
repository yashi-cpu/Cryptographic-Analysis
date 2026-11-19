
import time

from jordan_network.jordan import jordan_encrypt, jordan_decrypt
from chaotic_network.chaotic import chaotic_encrypt, chaotic_decrypt
from encryption.aes_encryption import aes_encrypt, aes_decrypt


def benchmark(message, repetitions=100):

    binary_message = ''.join(
        format(byte, '08b')
        for byte in message.encode('utf-8')
    )

    results = []

    # 1. JORDAN NETWORK
    start = time.perf_counter()

    for _ in range(repetitions):
        jordan_ciphertext, jordan_key = jordan_encrypt(binary_message)

    jordan_encrypt_time = (
        time.perf_counter() - start
    ) / repetitions

    start = time.perf_counter()

    for _ in range(repetitions):
        jordan_recovered = jordan_decrypt(
            jordan_ciphertext, jordan_key
        )

    jordan_decrypt_time = (
        time.perf_counter() - start
    ) / repetitions

    results.append({
        "Algorithm": "Jordan Network",
        "Encryption (ms)": jordan_encrypt_time * 1000,
        "Decryption (ms)": jordan_decrypt_time * 1000,
        "Ciphertext (bytes)": len(jordan_ciphertext) // 8,
        "Recovery": jordan_recovered == binary_message
    })

    # 2. CHAOTIC NETWORK
    start = time.perf_counter()

    for _ in range(repetitions):
        chaotic_ciphertext, chaotic_key = chaotic_encrypt(binary_message)

    chaotic_encrypt_time = (
        time.perf_counter() - start
    ) / repetitions

    start = time.perf_counter()

    for _ in range(repetitions):
        chaotic_recovered = chaotic_decrypt(
            chaotic_ciphertext, chaotic_key
        )

    chaotic_decrypt_time = (
        time.perf_counter() - start
    ) / repetitions

    results.append({
        "Algorithm": "Chaotic Network",
        "Encryption (ms)": chaotic_encrypt_time * 1000,
        "Decryption (ms)": chaotic_decrypt_time * 1000,
        "Ciphertext (bytes)": len(chaotic_ciphertext) // 8,
        "Recovery": chaotic_recovered == binary_message
    })

    # 3. AES-GCM
    start = time.perf_counter()

    for _ in range(repetitions):
        aes_key, nonce, aes_ciphertext = aes_encrypt(message)

    aes_encrypt_time = (
        time.perf_counter() - start
    ) / repetitions

    start = time.perf_counter()

    for _ in range(repetitions):
        aes_recovered = aes_decrypt(
            aes_key, nonce, aes_ciphertext
        )

    aes_decrypt_time = (
        time.perf_counter() - start
    ) / repetitions

    results.append({
        "Algorithm": "AES-GCM",
        "Encryption (ms)": aes_encrypt_time * 1000,
        "Decryption (ms)": aes_decrypt_time * 1000,
        "Ciphertext (bytes)": len(aes_ciphertext),
        "Recovery": aes_recovered == message
    })

    return results


if __name__ == "__main__":

    test_message = "i love you"

    comparison = benchmark(test_message)

    print("\n========== ALGORITHM COMPARISON ==========")

    for result in comparison:
        print("\nAlgorithm:", result["Algorithm"])
        print("Encryption Time:", round(result["Encryption (ms)"], 4), "ms")
        print("Decryption Time:", round(result["Decryption (ms)"], 4), "ms")
        print("Ciphertext Size:", result["Ciphertext (bytes)"], "bytes")
        print("Successful Recovery:", result["Recovery"])
