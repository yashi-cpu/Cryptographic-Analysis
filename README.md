# 🔐 CipherChat & Deep Learning Cryptography Platform (MSc Project)

An interactive, cybersecurity-themed cryptographic messaging and analysis laboratory featuring:
1. **CipherChat**: A WhatsApp-inspired secure messaging web application built with **React, Vite, Tailwind CSS, Framer Motion, and FastAPI**.
2. **Deep Learning Cryptography Studio**: An exploratory visual research dashboard built with **Streamlit, Plotly, and NumPy**.

---

## 🌟 Key Application: CipherChat (Secure Messaging Laboratory)

**CipherChat** simulates an end-to-end encrypted messaging platform where **Alice** and **Bob** communicate via text and image payloads, visually demonstrating encryption, ciphertext transmission, and decryption at each step.

### Core Modules:
- 💬 **WhatsApp-Style Secure Chat (`/`)**:
  - Dual-panel interface with Alice (Sender A) and Bob (Receiver B).
  - Algorithm switcher: **Jordan RNN**, **Chaotic Logistic Map**, or **AES-256-GCM**.
  - Animated data transmission channel displaying traveling ciphertext packets.
  - Real-time timestamped cryptographic activity log.
- 🧪 **Encryption Lab (`/encryption-lab`)**:
  - Technical 5-stage visualization: *Plaintext $\to$ Binary Encoding $\to$ Encryption Engine $\to$ Ciphertext $\to$ Receiver Decryption $\to$ Plaintext Recovery*.
  - Full inspection of binary arrays, keystream matrices, hex output, and bitwise verification.
  - "Show Encryption Process" animation replay button.
- 🖼️ **Image Cryptography (`/image-crypto`)**:
  - Upload JPG, JPEG, and PNG images.
  - 4-way comparison: *Original Plain-Image $\to$ Arnold Cat Map Permutation $\to$ Chained Lorenz Scrambled Cipher-Image $\to$ Lossless Recovered Image*.
  - Payload footprint, encryption latency, and decryption latency metrics.
- 🛡️ **Attacker Simulation (`/attacker`)**:
  - 3-party adversarial scenario featuring **Alice**, **Bob**, and **Eve (The Interceptor)**.
  - Eve captures ciphertext but lacks the legitimate key $\to$ unauthorized decryption fails.
  - **Ciphertext Bit-Flipping Tampering Attack**: Modifies bit 0 in transit. Demonstrates that **AES-256-GCM immediately raises an authentication error (`InvalidTag`)** while unauthenticated stream ciphers suffer bit corruption.
- 📊 **Performance Analytics (`/analytics`)**:
  - Real empirical timing benchmarks with configurable payload and iteration counts.
  - Interactive Recharts bar graphs comparing **Encryption Latency (ms)**, **Decryption Latency (ms)**, and **Ciphertext Length**.
  - Automated summary cards (Fastest Encryption, Fastest Decryption, Smallest Footprint).
- 📖 **About & Viva Notes (`/about`)**:
  - Architecture breakdown and academic disclaimers.

---

## 🚀 How to Run CipherChat

### One-Click Command (Recommended)
Run the launcher script to start both the **FastAPI Backend (Port 8000)** and the **Vite React Frontend (Port 5173)**:

```bash
./run_cipherchat.sh
```

Then open your browser at:
👉 **[http://localhost:5173](http://localhost:5173)**

API documentation (Swagger UI) is available at:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 🛠️ Manual Step-by-Step Launch

If you prefer running the servers in separate terminals:

### Terminal 1: FastAPI Backend
```bash
source venv/bin/activate
python cipherchat/backend/main.py
```
*(Runs on `http://127.0.0.1:8000`)*

### Terminal 2: React / Vite Frontend
```bash
cd cipherchat/frontend
npm run dev
```
*(Runs on `http://localhost:5173`)*

---

## 🔬 Streamlit Research Studio (Secondary App)
The Streamlit application remains available for academic theoretical analysis and NIST SP 800-22 testing:

```bash
./run_app.sh
```
*(Runs on `http://localhost:8501`)*

---

## 📁 Project Architecture

```
DeepLearningCryptography/
├── run_cipherchat.sh           # One-click launcher for CipherChat
├── run_app.sh                  # One-click launcher for Streamlit Studio
├── cipherchat/
│   ├── backend/
│   │   ├── main.py             # FastAPI REST API with CORS
│   │   ├── crypto_engines.py   # Unified cryptographic wrappers
│   │   └── requirements.txt
│   └── frontend/
│       ├── src/
│       │   ├── pages/
│       │   │   ├── SecureChat.jsx      # WhatsApp dual-panel chat
│       │   │   ├── EncryptionLab.jsx   # 5-stage technical pipeline
│       │   │   ├── ImageCrypto.jsx     # Visual image encryption
│       │   │   ├── AttackerSim.jsx     # Eve interception & tampering
│       │   │   ├── Analytics.jsx       # Recharts benchmark dashboard
│       │   │   └── About.jsx           # Viva notes & architecture
│       │   ├── components/
│       │   │   ├── Sidebar.jsx
│       │   │   └── AlgorithmBadge.jsx
│       │   ├── App.jsx
│       │   └── main.jsx
│       ├── index.html
│       ├── vite.config.js
│       └── package.json
├── jordan_network/             # Recurrent neural network engine
├── chaotic_network/            # Logistic map & 3D Lorenz attractor
├── neural_cryptography/        # Tree Parity Machine key exchange
├── evaluation/                 # NIST SP 800-22 tests & benchmarks
└── encryption/                 # AES-256-GCM authenticated cipher
```
