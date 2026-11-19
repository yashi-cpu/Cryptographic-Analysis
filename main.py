
from jordan_network.jordan import jordan_encrypt, jordan_decrypt
from chaotic_network.chaotic import ChaoticNetwork
from chaotic_network.chaotic import chaotic_encrypt, chaotic_decrypt
from encryption.aes_encryption import aes_encrypt, aes_decrypt
# 1. PLAINTEXT
message = "i love you"

# 2. CONVERT TEXT TO BINARY
binary_message = ''.join(
    format(byte, '08b')
    for byte in message.encode('utf-8')
)

print("Original Message:", message)
print("Binary Message:", binary_message)


# 3. BINARY TO TEXT
def binary_to_text(binary_message):

    bytes_list = [
        binary_message[i:i+8]
        for i in range(0, len(binary_message), 8)
    ]

    message = ''.join(
        chr(int(byte, 2))
        for byte in bytes_list
    )

    return message


# 4. BASIC XOR DEMONSTRATION
def xor_encrypt(binary_message, key):

    key_binary = ''.join(
        format(byte, '08b')
        for byte in key.encode('utf-8')
    )

    return ''.join(
        str(int(binary_message[i]) ^ int(key_binary[i % len(key_binary)]))
        for i in range(len(binary_message))
    )


key = "secret"

xor_ciphertext = xor_encrypt(binary_message, key)
xor_decrypted = xor_encrypt(xor_ciphertext, key)

print("\n--- BASIC XOR ---")
print("Ciphertext:", xor_ciphertext)
print("Recovered:", binary_to_text(xor_decrypted))


# 5. JORDAN NETWORK ENCRYPTION
jordan_ciphertext, jordan_key = jordan_encrypt(binary_message)

jordan_recovered = jordan_decrypt(
    jordan_ciphertext,
    jordan_key
)

print("\n--- JORDAN ENCRYPTION ---")
print("Keystream:", jordan_key)
print("Ciphertext:", jordan_ciphertext)
print("Recovered:", binary_to_text(jordan_recovered))
print("Successful Recovery:", jordan_recovered == binary_message)


# 6. CHAOTIC NETWORK
chaotic = ChaoticNetwork()

chaotic_key = chaotic.generate_binary_key(
    len(binary_message)
)

print("\n--- CHAOTIC NETWORK ---")
print("Generated Chaotic Key:", chaotic_key)


# 7. CHAOTIC ENCRYPTION

chaotic_ciphertext, chaotic_key = chaotic_encrypt(binary_message)

chaotic_recovered = chaotic_decrypt(
    chaotic_ciphertext,
    chaotic_key
)

print("\n--- CHAOTIC ENCRYPTION ---")
print("Generated Keystream:", chaotic_key)
print("Ciphertext:", chaotic_ciphertext)
print("Recovered:", binary_to_text(chaotic_recovered))

print(
    "Successful Recovery:",
    chaotic_recovered == binary_message
)

key, nonce, aes_ciphertext = aes_encrypt(message)

aes_recovered = aes_decrypt(
    key,
    nonce,
    aes_ciphertext
)

print("\n--- AES-GCM ENCRYPTION ---")
print("Ciphertext:", aes_ciphertext.hex())
print("Recovered:", aes_recovered)
print("Successful Recovery:", aes_recovered == message)