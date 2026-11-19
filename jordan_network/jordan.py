import numpy as np


class JordanNetwork:
    """
    Jordan Recurrent Neural Network for keystream generation.
    Incorporates non-linear output-to-context recurrent feedback and hidden recurrence
    to produce balanced, pseudo-random keystreams avoiding degenerate bit inversion.
    """
    def __init__(self, input_size=1, hidden_size=16, seed=1337):
        rng = np.random.RandomState(seed)
        self.hidden_size = hidden_size
        self.w_input = rng.randn(input_size, hidden_size) * 0.8
        self.w_context = rng.randn(1, hidden_size) * 1.2
        self.w_hidden = rng.randn(hidden_size, hidden_size) * 0.5
        self.w_out = rng.randn(hidden_size, 1) * 1.5
        self.b_hidden = rng.randn(hidden_size) * 0.2
        self.b_out = np.zeros(1)

        self.context = np.array([0.5])
        self.h = np.zeros(hidden_size)

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-np.clip(x, -30.0, 30.0)))

    def generate_keystream(self, binary_data):
        keystream = []
        for bit in binary_data:
            x = np.array([int(bit)])
            # Context and hidden state recurrent mixing
            self.h = np.tanh(
                np.dot(x, self.w_input)
                + np.dot(self.context, self.w_context)
                + np.dot(self.h, self.w_hidden)
                + self.b_hidden
            )
            out_val = self.sigmoid(np.dot(self.h, self.w_out) + self.b_out)[0]
            key_bit = '1' if out_val >= 0.5 else '0'
            keystream.append(key_bit)
            # Output unit feeds back to context unit (Jordan recurrence)
            self.context = np.array([out_val])

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
