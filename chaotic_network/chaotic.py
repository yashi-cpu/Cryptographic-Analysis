
import numpy as np


class ChaoticNetwork:

    def __init__(self, initial_value=0.37, r=3.99):
        self.initial_value = initial_value
        self.r = r

    def generate_sequence(self, length):

        x = self.initial_value
        sequence = []

        for _ in range(length):
            x = self.r * x * (1 - x)
            sequence.append(x)

        return sequence

    def generate_binary_key(self, length):

        sequence = self.generate_sequence(length)

        binary_key = ''.join(
            '1' if value >= 0.5 else '0'
            for value in sequence
        )

        return binary_key


def chaotic_encrypt(binary_message, initial_value=0.37, r=3.99):

    chaotic = ChaoticNetwork(initial_value, r)

    keystream = chaotic.generate_binary_key(
        len(binary_message)
    )

    ciphertext = ''.join(
        str(int(a) ^ int(b))
        for a, b in zip(binary_message, keystream)
    )

    return ciphertext, keystream


def chaotic_decrypt(ciphertext, keystream):

    plaintext = ''.join(
        str(int(a) ^ int(b))
        for a, b in zip(ciphertext, keystream)
    )

    return plaintext
