# 🔐 Deep Learning & Chaotic Cryptography Studio (Master's Research Edition)

A Master's-grade cryptographic research testbed and interactive visual suite combining:
1. **Neural Key Exchange**: Tree Parity Machines (TPM) with mutual synchronization and cryptanalysis against eavesdroppers (Eve).
2. **3D Hyperchaotic Multimedia Cryptography**: Continuous 3D Lorenz system (Runge-Kutta 4) + 2D Arnold's Cat Map permutation + Chained bidirectional modular diffusion for lossless image encryption.
3. **Formal NIST SP 800-22 Evaluation**: Statistical hypothesis testing ($P$-value scorecard with $\alpha = 0.01$).
4. **Differential Cryptanalysis Defense**: Validation of the strict theoretical benchmarks for **NPCR (> 99.609%)**, **UACI (~ 33.463%)**, and **Adjacent Pixel Correlation ($r_{xy} \approx 0.00$)**.

---

## 🌟 Master's Level Architecture

### 1. 🧠 Neural Cryptography & Key Exchange (Tree Parity Machines)
- **Kanter-Gross-Kinzelman (KGK) Protocol**: Alice and Bob mutually train their discrete synaptic weights over an insecure public channel.
- **Eve Eavesdropping Attack Simulation**: Demonstrates why bidirectional mutual learning converges in $\mathcal{O}(L^2)$ rounds while unidirectional eavesdropping fails to synchronize.
- **Cryptographic Key Derivation**: SHA-256 digest of synchronized synaptic weights produces a true 256-bit symmetric key.
- **Configurable Dynamics**: Hidden units ($K$), Inputs per unit ($N$), Synaptic bounds ($[-L, +L]$), and learning rules (Hebbian, Anti-Hebbian, Random Walk).

### 2. 🖼️ 3D Lorenz & Multimedia Cryptography (Confusion + Diffusion)
- **Continuous 3D Lorenz Attractor**:
  $$\frac{dx}{dt} = \sigma (y - x), \quad \frac{dy}{dt} = x (\rho - z) - y, \quad \frac{dz}{dt} = xy - \beta z$$
  Solved numerically via 4th-Order Runge-Kutta (RK4) with $dt=0.01$, eliminating finite-precision dynamic degradation.
- **Stage 1 (Confusion)**: 2D discrete Arnold's Cat Map coordinate permutation:
  $$\begin{pmatrix} x' \\ y' \end{pmatrix} = \begin{pmatrix} 1 & p \\ q & pq+1 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} \pmod N$$
- **Stage 2 (Diffusion)**: Bidirectional chained modular diffusion:
  $$C_{fwd}[i] = (P[i] + K_1[i] + C_{fwd}[i-1]) \pmod{256}$$
  $$C[i] = (C_{fwd}[i] + K_2[i] + C[i+1]) \pmod{256}$$
- **Differential Cryptanalysis Resistance**:
  - **NPCR (Number of Pixels Change Rate)**: Achieves **99.61%** (exceeds theoretical requirement of $> 99.609\%$).
  - **UACI (Unified Average Changing Intensity)**: Achieves **33.35%** (matches theoretical expectation of $\approx 33.463\%$).
  - **Adjacent Pixel Correlation ($r_{xy}$)**: Decreases correlation from $r \approx 0.95$ in plain-images to $r \approx 0.00$ in cipher-images.

### 3. 📋 NIST SP 800-22 Cryptographic Randomness Test Suite
Standardized statistical hypothesis tests evaluated with significance level $\alpha = 0.01$:
- **Monobit Frequency Test**
- **Block Frequency Test**
- **Runs Test**
- **Longest Run of Ones in a Block**
- **Discrete Fourier Transform (Spectral) Test**

### 4. 🚀 Live Text Cryptography Studio
- Step-by-step pipeline view: *Plaintext $\to$ Binary Encoding $\to$ Keystream Generation $\to$ Ciphertext $\to$ Decryption Verification*.
- Comparison between Jordan RNN, Chaotic Logistic Map, 3D Lorenz Attractor, AES-256-GCM, and XOR.
- Interactive ciphertext tampering simulation (stream bit-flip corruption vs. AES-GCM `InvalidTag` rejection).

---

## 🚀 Quick Start

### 1. Launch the Streamlit Research Studio
```bash
./run_app.sh
```
Or directly:
```bash
./venv/bin/streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 📁 Repository Structure

```
DeepLearningCryptography/
├── app.py                      # Main Master's Research Streamlit UI
├── run_app.sh                  # One-click execution launcher
├── requirements.txt            # Project dependencies
├── main.py                     # Initial demo script
├── assets/                     # Sample high-contrast cipher target images
│   └── sample_cipher_target.png
├── neural_cryptography/        # Kanter-Gross-Kinzelman TPM Neural Key Exchange
│   ├── __init__.py
│   └── tpm.py
├── chaotic_network/            # Chaotic dynamical systems
│   ├── chaotic.py              # 1D Logistic Map
│   └── lorenz.py               # 3D Lorenz continuous system & Arnold Cat Map
├── evaluation/                 # Cryptanalysis & benchmarking suites
│   ├── nist_tests.py           # NIST SP 800-22 tests + NPCR/UACI + Pixel Correlation
│   ├── compare.py              # Execution latency benchmarks
│   └── validate.py             # Regression tests
├── encryption/                 # AES-GCM Authenticated Encryption
│   └── aes_encryption.py
└── utils/                      # Reusable mathematical & bit-level utilities
    ├── __init__.py
    └── crypto_utils.py
```
