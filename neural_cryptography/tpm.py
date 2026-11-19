import hashlib
import numpy as np


class TreeParityMachine:
    """
    Tree Parity Machine (TPM) for Neural Cryptography (Kanter-Gross-Kinzelman Protocol).
    Parameters:
        K: Number of hidden units (default 3)
        N: Number of inputs per hidden unit (default 4)
        L: Maximum synaptic weight limit, weights in [-L, +L] (default 3)
        seed: Optional random seed for initialization
    """
    def __init__(self, K=3, N=4, L=3, seed=None):
        self.K = K
        self.N = N
        self.L = L
        if seed is not None:
            np.random.seed(seed)
        # Discrete integer synaptic weights in [-L, +L]
        self.weights = np.random.randint(-L, L + 1, size=(K, N))
        self.hidden_states = np.zeros(K, dtype=int)
        self.tau = 0

    def forward(self, X: np.ndarray) -> int:
        """
        Compute output tau in {-1, +1} given input X of shape (K, N) with values in {-1, +1}.
        """
        # Linear sum per hidden unit
        sums = np.sum(self.weights * X, axis=1)
        # sgn function: if 0, resolve to -1 to avoid zero state
        self.hidden_states = np.where(sums > 0, 1, -1)
        self.tau = int(np.prod(self.hidden_states))
        return self.tau

    def update(self, X: np.ndarray, tau_partner: int, rule="hebbian"):
        """
        Update weights based on the partner's output.
        Only updates when self.tau == tau_partner.
        """
        if self.tau != tau_partner:
            return

        for i in range(self.K):
            # Only update hidden units that agreed with overall output tau
            if self.hidden_states[i] == self.tau:
                if rule == "hebbian":
                    # Hebbian: w = w + x * tau
                    delta = X[i] * self.tau
                elif rule == "anti_hebbian":
                    # Anti-Hebbian: w = w - x * tau
                    delta = -X[i] * self.tau
                elif rule == "random_walk":
                    # Random Walk: w = w + x
                    delta = X[i]
                else:
                    delta = X[i] * self.tau

                self.weights[i] = np.clip(self.weights[i] + delta, -self.L, self.L)

    def get_sync_score(self, other_tpm: "TreeParityMachine") -> float:
        """
        Calculate weight agreement ratio in [0.0, 1.0].
        """
        matches = np.sum(self.weights == other_tpm.weights)
        return float(matches) / float(self.K * self.N)

    def extract_key(self) -> bytes:
        """
        Derive a 256-bit cryptographic AES key by hashing the synchronized synaptic weights.
        """
        weight_bytes = self.weights.astype(np.int8).tobytes()
        return hashlib.sha256(weight_bytes).digest()


def simulate_neural_key_exchange(K=3, N=4, L=3, rule="hebbian", max_steps=2500, eve_present=True):
    """
    Simulates the Kanter-Gross-Kinzelman neural key exchange between Alice and Bob,
    with an active eavesdropper (Eve) attempting to synchronize passively.
    Returns:
        history: dict with rounds, alice_bob_sync, alice_eve_sync
        synchronized: bool
        steps_taken: int
        derived_key_hex: str
    """
    alice = TreeParityMachine(K=K, N=N, L=L)
    bob = TreeParityMachine(K=K, N=N, L=L)
    eve = TreeParityMachine(K=K, N=N, L=L) if eve_present else None

    rounds = []
    ab_sync_history = []
    ae_sync_history = []

    for step in range(1, max_steps + 1):
        # Generate random public input X in {-1, +1}
        X = np.random.choice([-1, 1], size=(K, N))

        tau_A = alice.forward(X)
        tau_B = bob.forward(X)
        if eve:
            tau_E = eve.forward(X)

        # Alice and Bob update if their outputs match
        if tau_A == tau_B:
            alice.update(X, tau_B, rule=rule)
            bob.update(X, tau_A, rule=rule)

            # Eve can only update if she predicted the matching output correctly
            if eve and tau_E == tau_A:
                eve.update(X, tau_A, rule=rule)

        ab_score = alice.get_sync_score(bob)
        rounds.append(step)
        ab_sync_history.append(ab_score)

        if eve:
            ae_score = alice.get_sync_score(eve)
            ae_sync_history.append(ae_score)
        else:
            ae_sync_history.append(0.0)

        # Check full synchronization
        if ab_score == 1.0:
            key_hex = alice.extract_key().hex()
            return {
                "synchronized": True,
                "steps": step,
                "rounds": rounds,
                "ab_sync": ab_sync_history,
                "ae_sync": ae_sync_history,
                "eve_synced": (eve.get_sync_score(alice) == 1.0) if eve else False,
                "key_hex": key_hex,
                "alice_weights": alice.weights.tolist(),
                "bob_weights": bob.weights.tolist(),
                "eve_weights": eve.weights.tolist() if eve else None
            }

    # If reached max steps without 100% sync
    return {
        "synchronized": False,
        "steps": max_steps,
        "rounds": rounds,
        "ab_sync": ab_sync_history,
        "ae_sync": ae_sync_history,
        "eve_synced": False,
        "key_hex": None,
        "alice_weights": alice.weights.tolist(),
        "bob_weights": bob.weights.tolist(),
        "eve_weights": eve.weights.tolist() if eve else None
    }
