
import numpy as np


class JordanNetwork:

    def __init__(self, input_size=1, hidden_size=8):
        np.random.seed(42)

        self.hidden_weights = np.random.randn(
            input_size + 1, hidden_size
        ) * 0.1

        self.output_weights = np.random.randn(
            hidden_size, 1
        ) * 0.1

        self.hidden_bias = np.zeros(hidden_size)
        self.output_bias = np.zeros(1)

        self.context = np.zeros(1)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def generate_keystream(self, binary_data):

        keystream = []

        for bit in binary_data:

            current_input = np.array([int(bit)])

            combined_input = np.concatenate(
                (current_input, self.context)
            )

            hidden = np.tanh(
                np.dot(combined_input, self.hidden_weights)
                + self.hidden_bias
            )

            output = self.sigmoid(
                np.dot(hidden, self.output_weights)
                + self.output_bias
            )

            key_bit = '1' if output[0] >= 0.5 else '0'

            keystream.append(key_bit)

            self.context = output

        return ''.join(keystream)


def jordan_encrypt(binary_message):

    network = JordanNetwork()

    keystream = network.generate_keystream(binary_message)

    ciphertext = ''.join(
        str(int(a) ^ int(b))
        for a, b in zip(binary_message, keystream)
    )

    return ciphertext, keystream


def jordan_decrypt(ciphertext, keystream):

    plaintext = ''.join(
        str(int(a) ^ int(b))
        for a, b in zip(ciphertext, keystream)
    )

    return plaintext
