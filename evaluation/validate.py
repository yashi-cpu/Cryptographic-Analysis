
from jordan_network.jordan import jordan_encrypt, jordan_decrypt
from chaotic_network.chaotic import chaotic_encrypt, chaotic_decrypt
from encryption.aes_encryption import aes_encrypt, aes_decrypt

from cryptography.exceptions import InvalidTag


# Different messages to test
test_messages = [
    "Hello",
    "Deep Learning in Cryptography",
    "i love you",
    "Encryption Testing 123!",
    "こんにちは"
]


print("\n========== BACKEND VALIDATION ==========")

# Test Jordan Network
print("\n--- JORDAN NETWORK ---")

for message in test_messages:
    binary_message = ''.join(
        format(byte, '08b') for byte in message.encode("utf-8")
    )

    ciphertext, key = jordan_encrypt(binary_message)
    recovered_binary = jordan_decrypt(ciphertext, key)

    recovered_message = bytes(
        int(recovered_binary[i:i+8], 2)
        for i in range(0, len(recovered_binary), 8)
    ).decode("utf-8")

    print(f"Message: {message}")
    print(f"Recovery: {recovered_message == message}")


# Test Chaotic Network
print("\n--- CHAOTIC NETWORK ---")

for message in test_messages:
    binary_message = ''.join(
        format(byte, '08b') for byte in message.encode("utf-8")
    )

    ciphertext, key = chaotic_encrypt(binary_message)
    recovered_binary = chaotic_decrypt(ciphertext, key)

    recovered_message = bytes(
        int(recovered_binary[i:i+8], 2)
        for i in range(0, len(recovered_binary), 8)
    ).decode("utf-8")

    print(f"Message: {message}")
    print(f"Recovery: {recovered_message == message}")


# Test AES-GCM
print("\n--- AES-GCM ---")

for message in test_messages:
    key, nonce, ciphertext = aes_encrypt(message)
    recovered_message = aes_decrypt(key, nonce, ciphertext)

    print(f"Message: {message}")
    print(f"Recovery: {recovered_message == message}")


# Test AES-GCM tampering detection
print("\n--- AES-GCM TAMPERING TEST ---")

message = "Confidential information"

key, nonce, ciphertext = aes_encrypt(message)

# Change one bit in the ciphertext
tampered_ciphertext = bytearray(ciphertext)
tampered_ciphertext[0] ^= 1

try:
    aes_decrypt(key, nonce, bytes(tampered_ciphertext))
    print("Tampering detected: False")

except InvalidTag:
    print("Tampering detected: True")
    print("AES-GCM rejected the modified ciphertext.")

print("\n========== VALIDATION COMPLETED ==========")
