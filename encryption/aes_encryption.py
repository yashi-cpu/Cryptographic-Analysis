
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def aes_encrypt(message):

    key = AESGCM.generate_key(bit_length=256)
    aes = AESGCM(key)

    nonce = os.urandom(12)

    ciphertext = aes.encrypt(
        nonce,
        message.encode("utf-8"),
        None
    )

    return key, nonce, ciphertext


def aes_decrypt(key, nonce, ciphertext):

    aes = AESGCM(key)

    decrypted = aes.decrypt(
        nonce,
        ciphertext,
        None
    )

    return decrypted.decode("utf-8")
