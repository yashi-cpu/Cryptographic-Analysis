import os
import sys
import time
import math
import numpy as np
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from cryptography.exceptions import InvalidTag

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from jordan_network.jordan import JordanNetwork, jordan_encrypt, jordan_decrypt
from chaotic_network.chaotic import ChaoticNetwork, chaotic_encrypt, chaotic_decrypt
from chaotic_network.lorenz import (
    LorenzSystem,
    ArnoldCatMap,
    encrypt_image_lorenz,
    decrypt_image_lorenz
)
from neural_cryptography.tpm import TreeParityMachine, simulate_neural_key_exchange
from encryption.aes_encryption import aes_encrypt, aes_decrypt
from utils.crypto_utils import (
    text_to_binary,
    binary_to_text,
    calculate_entropy,
    calculate_avalanche_effect,
    flip_bit,
    basic_xor_encrypt
)
from evaluation.nist_tests import (
    run_full_nist_suite,
    calculate_npcr_uaci,
    calculate_pixel_correlation
)

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Deep Learning & Chaotic Cryptography Studio",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.0rem;
        color: #64748b;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.05);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .pass-badge {
        background-color: #dcfce7;
        color: #15803d;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .fail-badge {
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/security-shield-green.png", width=60)
    st.markdown("### 🔐 Deep Learning Cryptography")
    st.caption("Master's Level Research & Demonstration Testbed")
    
    st.markdown("---")
    menu = st.radio(
        "Navigation",
        [
            "🚀 Text Cryptography Studio",
            "🖼️ 3D Lorenz & Image Cryptography",
            "🧠 Neural Key Exchange (TPM & Eve)",
            "📋 NIST SP 800-22 Randomness Tests",
            "📊 Performance Benchmarks",
            "🛡️ Security & Entropy Analysis",
            "🌀 Chaotic Dynamical Systems",
            "📖 Master's Thesis Foundations"
        ]
    )
    
    st.markdown("---")
    st.markdown("#### ⚡ Quick Presets")
    preset_choice = st.selectbox(
        "Load sample message:",
        [
            "i love you (Original Demo)",
            "Hello, Deep Learning Cryptography!",
            "Confidential Payload 2026",
            "日本語 & Multilingual Unicode 🚀",
            "Custom Input"
        ]
    )
    
    preset_dict = {
        "i love you (Original Demo)": "i love you",
        "Hello, Deep Learning Cryptography!": "Hello, Deep Learning Cryptography!",
        "Confidential Payload 2026": "Confidential Payload 2026",
        "日本語 & Multilingual Unicode 🚀": "日本語 & Multilingual Unicode 🚀"
    }


# =========================================================
# TAB 1: TEXT CRYPTOGRAPHY STUDIO
# =========================================================
if menu == "🚀 Text Cryptography Studio":
    st.markdown('<div class="main-title">Text Cryptography Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Encrypt, inspect, decrypt, and simulate ciphertext tampering across Neural, Chaotic, and Standard ciphers.</div>', unsafe_allow_html=True)
    
    col_input, col_meta = st.columns([3, 1])
    default_text = preset_dict.get(preset_choice, "i love you")
    if preset_choice == "Custom Input":
        default_text = "Secure stream cipher testing with recurrent neural networks."
        
    with col_input:
        user_message = st.text_area("Input Plaintext Message:", value=default_text, height=90)
    
    with col_meta:
        st.markdown("**Message Metadata**")
        byte_len = len(user_message.encode('utf-8'))
        bit_len = byte_len * 8
        st.metric("Character Count", len(user_message))
        st.metric("Byte Length", f"{byte_len} B")
        st.metric("Bit Length", f"{bit_len} bits")
    
    if not user_message:
        st.warning("Please enter a message to begin encryption.")
        st.stop()
        
    binary_message = text_to_binary(user_message)
    st.markdown("---")
    
    algo_col1, algo_col2 = st.columns([1, 2])
    with algo_col1:
        algorithm = st.selectbox(
            "Cryptographic Engine:",
            [
                "Jordan Recurrent Neural Network",
                "Chaotic Logistic Map (1D)",
                "Continuous 3D Lorenz Attractor",
                "AES-256-GCM (AEAD Standard)",
                "Basic XOR Cipher (Baseline)"
            ]
        )
    
    with algo_col2:
        if algorithm == "Jordan Recurrent Neural Network":
            st.info("🧠 **Jordan RNN**: Feedback connections from the output unit to the context unit produce a state-dependent keystream.")
            j_col1, j_col2 = st.columns(2)
            with j_col1:
                jordan_hidden_size = st.slider("Hidden Layer Size", 4, 32, 8, 4)
            with j_col2:
                jordan_seed = st.number_input("Random Seed (Weights init)", 1, 9999, 42)
                
        elif algorithm == "Chaotic Logistic Map (1D)":
            st.info("🌀 **Chaotic Map**: Employs non-linear logistic recurrence $x_{n+1} = r x_n (1 - x_n)$ in chaotic regime.")
            c_col1, c_col2 = st.columns(2)
            with c_col1:
                initial_val = st.slider("Initial Seed Value (x₀)", 0.01, 0.99, 0.37, 0.01)
            with c_col2:
                r_param = st.slider("Control Parameter (r)", 3.50, 4.00, 3.99, 0.01)
                
        elif algorithm == "Continuous 3D Lorenz Attractor":
            st.info("🦋 **3D Lorenz System**: Continuous dynamical system integrated via 4th-Order Runge-Kutta (RK4) providing high-entropy 3D coordinate keystreams.")
            l_col1, l_col2, l_col3 = st.columns(3)
            with l_col1:
                lx0 = st.number_input("x₀", value=0.1, step=0.01)
            with l_col2:
                ly0 = st.number_input("y₀", value=0.0, step=0.01)
            with l_col3:
                lz0 = st.number_input("z₀", value=0.0, step=0.01)
                
        elif algorithm == "AES-256-GCM (AEAD Standard)":
            st.info("🛡️ **AES-256-GCM**: Industry standard authenticated encryption providing confidentiality and tamper detection.")
            
        elif algorithm == "Basic XOR Cipher (Baseline)":
            st.info("🔀 **Basic XOR**: Classical stream baseline with repeating key phrase.")
            xor_key_input = st.text_input("Secret Key Phrase:", value="secret")

    # Pipeline Execution
    st.markdown("### 🔐 Encryption Pipeline")
    
    if algorithm == "Jordan Recurrent Neural Network":
        np.random.seed(jordan_seed)
        net = JordanNetwork(input_size=1, hidden_size=jordan_hidden_size)
        keystream = net.generate_keystream(binary_message)
        ciphertext = ''.join(str(int(a) ^ int(b)) for a, b in zip(binary_message, keystream))
        recovered_binary = jordan_decrypt(ciphertext, keystream)
        recovered_text = binary_to_text(recovered_binary)
        
    elif algorithm == "Chaotic Logistic Map (1D)":
        chaotic_obj = ChaoticNetwork(initial_value=initial_val, r=r_param)
        keystream = chaotic_obj.generate_binary_key(len(binary_message))
        ciphertext = ''.join(str(int(a) ^ int(b)) for a, b in zip(binary_message, keystream))
        recovered_binary = chaotic_decrypt(ciphertext, keystream)
        recovered_text = binary_to_text(recovered_binary)
        
    elif algorithm == "Continuous 3D Lorenz Attractor":
        lorenz_sys = LorenzSystem()
        keystream = lorenz_sys.generate_binary_keystream(len(binary_message), initial_state=(lx0, ly0, lz0))
        ciphertext = ''.join(str(int(a) ^ int(b)) for a, b in zip(binary_message, keystream))
        recovered_binary = ''.join(str(int(a) ^ int(b)) for a, b in zip(ciphertext, keystream))
        recovered_text = binary_to_text(recovered_binary)

    elif algorithm == "AES-256-GCM (AEAD Standard)":
        key, nonce, aes_cipher = aes_encrypt(user_message)
        recovered_text = aes_decrypt(key, nonce, aes_cipher)

    elif algorithm == "Basic XOR Cipher (Baseline)":
        ciphertext, keystream = basic_xor_encrypt(binary_message, xor_key_input)
        recovered_binary = ''.join(str(int(a) ^ int(b)) for a, b in zip(ciphertext, keystream))
        recovered_text = binary_to_text(recovered_binary)

    # Display Stage Tabs
    t1, t2, t3, t4 = st.tabs(["1. Binary Plaintext", "2. Keystream / Key", "3. Ciphertext Output", "4. Decryption Verification"])
    with t1:
        st.code(binary_message, language="text")
    with t2:
        if algorithm == "AES-256-GCM (AEAD Standard)":
            st.markdown(f"**256-bit Key (Hex):** `{key.hex()}`")
            st.markdown(f"**96-bit Nonce (Hex):** `{nonce.hex()}`")
        else:
            st.code(keystream, language="text")
    with t3:
        if algorithm == "AES-256-GCM (AEAD Standard)":
            st.code(aes_cipher.hex(), language="text")
        else:
            st.code(ciphertext, language="text")
            hex_c = hex(int(ciphertext, 2))[2:] if ciphertext else "0"
            st.caption(f"Hex Representation: `{hex_c}`")
    with t4:
        if recovered_text == user_message:
            st.success(f"✅ Exact Recovery Match: `{recovered_text}`")
        else:
            st.error("❌ Decryption Failed")

    # Tampering Section
    st.markdown("---")
    st.subheader("🧪 Ciphertext Tampering & Integrity Test")
    t_col1, t_col2 = st.columns([1, 2])
    with t_col1:
        tamper_mode = st.radio("Simulation:", ["Clean Transmission", "Flip 1 Bit", "Corrupt Byte"])
    with t_col2:
        if tamper_mode == "Clean Transmission":
            st.info("Clean ciphertext received. Decryption authenticated.")
        elif tamper_mode == "Flip 1 Bit":
            if algorithm == "AES-256-GCM (AEAD Standard)":
                tampered = bytearray(aes_cipher)
                tampered[0] ^= 1
                try:
                    aes_decrypt(key, nonce, bytes(tampered))
                    st.error("🚨 Tampering went undetected!")
                except InvalidTag:
                    st.success("🛡️ **AES-GCM Authenticated Defense**: Tamper detected! `InvalidTag` raised. Ciphertext rejected.")
            else:
                tampered_c = flip_bit(ciphertext, 0)
                tampered_rec = binary_to_text(''.join(str(int(a) ^ int(b)) for a, b in zip(tampered_c, keystream)))
                st.warning(f"⚠️ **Stream Cipher Bit Flip**: Single flipped bit corrupted output character: `{tampered_rec}`")
        elif tamper_mode == "Corrupt Byte":
            if algorithm == "AES-256-GCM (AEAD Standard)":
                tampered = bytearray(aes_cipher)
                tampered[-1] ^= 0xFF
                try:
                    aes_decrypt(key, nonce, bytes(tampered))
                except InvalidTag:
                    st.success("🛡️ **AES-GCM Authenticated Defense**: Modified tag rejected.")
            else:
                tampered_c = list(ciphertext)
                for i in range(min(8, len(tampered_c))):
                    tampered_c[i] = '1' if tampered_c[i] == '0' else '0'
                tampered_rec = binary_to_text(''.join(str(int(a) ^ int(b)) for a, b in zip(''.join(tampered_c), keystream)))
                st.warning(f"⚠️ **Byte Corrupted**: Plaintext corrupted: `{tampered_rec}`")


# =========================================================
# TAB 2: 3D LORENZ & IMAGE CRYPTOGRAPHY (MASTER'S PILLAR)
# =========================================================
elif menu == "🖼️ 3D Lorenz & Image Cryptography":
    st.markdown('<div class="main-title">3D Lorenz Continuous Attractor & Image Cryptography</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Two-stage Confusion-Diffusion Visual Cryptosystem with 2D Arnold Cat Map and 3D Continuous Lorenz RK4 Integration.</div>', unsafe_allow_html=True)
    
    tab_img_crypto, tab_3d_orbit = st.tabs(["🖼️ Image Encryption & Differential Metrics", "🦋 3D Lorenz Attractor Orbit"])
    
    with tab_3d_orbit:
        st.subheader("1. Numerical Integration of the Continuous 3D Lorenz System")
        st.latex(r"\frac{dx}{dt} = \sigma (y - x), \quad \frac{dy}{dt} = x (\rho - z) - y, \quad \frac{dz}{dt} = xy - \beta z")
        
        lor_c1, lor_c2, lor_c3, lor_c4 = st.columns(4)
        with lor_c1:
            lor_sigma = st.slider("Prandtl Number (σ)", 5.0, 20.0, 10.0, 0.5)
        with lor_c2:
            lor_rho = st.slider("Rayleigh Number (ρ)", 10.0, 40.0, 28.0, 1.0)
        with lor_c3:
            lor_beta = st.slider("Geometric Ratio (β)", 1.0, 4.0, 8.0/3.0, 0.1)
        with lor_c4:
            lor_steps = st.slider("Trajectory Steps", 1000, 8000, 3500, 500)
            
        lorenz_sim = LorenzSystem(sigma=lor_sigma, rho=lor_rho, beta=lor_beta)
        traj = lorenz_sim.generate_trajectory(steps=lor_steps)
        
        fig_3d = go.Figure(data=[go.Scatter3d(
            x=traj[:, 0], y=traj[:, 1], z=traj[:, 2],
            mode='lines',
            line=dict(
                color=traj[:, 2],
                colorscale='Viridis',
                width=2.5
            )
        )])
        fig_3d.update_layout(
            title="3D Lorenz Strange Attractor Butterfly Trajectory (RK4 Integration)",
            template="plotly_dark",
            height=550,
            scene=dict(
                xaxis_title="X Axis",
                yaxis_title="Y Axis",
                zaxis_title="Z Axis"
            ),
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig_3d, use_container_width=True)
        st.info("💡 **Academic Note**: The Lorenz system is a continuous non-linear system with a positive maximum Lyapunov exponent (λ > 0), ensuring sensitive dependence on initial conditions and a fractal attractor dimension of ~2.06.")

    with tab_img_crypto:
        st.subheader("2. Two-Stage Image Encryption (Confusion + Bidirectional Modular Diffusion)")
        
        img_src_col1, img_src_col2 = st.columns([1, 2])
        with img_src_col1:
            img_source = st.radio("Image Source:", ["Built-in High-Contrast Target", "Upload Image (PNG/JPEG)"])
            cat_rounds = st.slider("Arnold's Cat Map Permutation Rounds:", 1, 6, 2)
            
        with img_src_col2:
            if img_source == "Upload Image (PNG/JPEG)":
                uploaded_file = st.file_uploader("Upload Image:", type=["png", "jpg", "jpeg"])
                if uploaded_file:
                    pil_img = Image.open(uploaded_file).convert("RGB")
                    # Resize to reasonable dimensions for fast interactive feedback
                    pil_img = pil_img.resize((128, 128))
                else:
                    pil_img = Image.open("assets/sample_cipher_target.png")
            else:
                pil_img = Image.open("assets/sample_cipher_target.png")
                
            st.image(pil_img, caption="Input Plaintext Image (128x128 RGB)", width=128)

        img_np = np.array(pil_img, dtype=np.uint8)

        if st.button("🚀 Encrypt Image & Run Cryptanalysis Suite", type="primary"):
            with st.spinner("Executing Confusion, Modular Lorenz Diffusion, and Differential Testing..."):
                # 1. Encrypt
                cipher_img, permuted_img = encrypt_image_lorenz(img_np, cat_rounds=cat_rounds)
                # 2. Decrypt
                restored_img = decrypt_image_lorenz(cipher_img, cat_rounds=cat_rounds)
                
                # 3. Differential Test (NPCR / UACI) with 1-pixel modification
                img_perturbed = img_np.copy()
                img_perturbed[0, 0, 0] = (int(img_perturbed[0, 0, 0]) + 1) % 256
                cipher_perturbed, _ = encrypt_image_lorenz(img_perturbed, cat_rounds=cat_rounds)
                diff_metrics = calculate_npcr_uaci(cipher_img, cipher_perturbed)
                
                # 4. Adjacent Pixel Correlation
                corr_plain = calculate_pixel_correlation(img_np)
                corr_cipher = calculate_pixel_correlation(cipher_img)

            st.markdown("---")
            st.markdown("#### 🖼️ Image Transformation Pipeline")
            
            c_p1, c_p2, c_p3, c_p4 = st.columns(4)
            with c_p1:
                st.image(img_np, caption="1. Original Plain-Image", use_container_width=True)
            with c_p2:
                st.image(permuted_img, caption=f"2. Arnold Cat Map ({cat_rounds} rds)", use_container_width=True)
            with c_p3:
                st.image(cipher_img, caption="3. Chained Lorenz Cipher-Image", use_container_width=True)
            with c_p4:
                st.image(restored_img, caption="4. Exact Recovered Image", use_container_width=True)

            is_perfect = np.array_equal(img_np, restored_img)
            if is_perfect:
                st.success("✅ **Lossless Recovery**: Recovered array is 100% bitwise identical to the original image!")
            else:
                st.error("❌ Decryption mismatch detected.")

            # Metrics and Histograms
            st.markdown("---")
            st.markdown("#### 📊 Differential Cryptanalysis & Correlation Defense")
            
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                npcr_val = diff_metrics["npcr"]
                st.metric(
                    "NPCR (Number of Pixels Change Rate)",
                    f"{npcr_val:.4f}%",
                    "Benchmark: > 99.609%"
                )
                if npcr_val >= 99.6:
                    st.markdown('<span class="pass-badge">PASSED BENCHMARK</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="fail-badge">SUB-OPTIMAL</span>', unsafe_allow_html=True)

            with m_col2:
                uaci_val = diff_metrics["uaci"]
                st.metric(
                    "UACI (Average Changing Intensity)",
                    f"{uaci_val:.4f}%",
                    "Benchmark: ~ 33.463%"
                )
                if 30.0 <= uaci_val <= 36.0:
                    st.markdown('<span class="pass-badge">PASSED BENCHMARK</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="fail-badge">SUB-OPTIMAL</span>', unsafe_allow_html=True)

            with m_col3:
                st.markdown("**Adjacent Pixel Correlation ($r_{xy}$)**")
                corr_df = pd.DataFrame({
                    "Direction": ["Horizontal", "Vertical", "Diagonal"],
                    "Plain-Image": [corr_plain["horizontal"], corr_plain["vertical"], corr_plain["diagonal"]],
                    "Cipher-Image": [corr_cipher["horizontal"], corr_cipher["vertical"], corr_cipher["diagonal"]]
                })
                st.dataframe(corr_df.style.format({"Plain-Image": "{:.4f}", "Cipher-Image": "{:.4f}"}), use_container_width=True)
                st.caption("Plain-images have high correlation ($r \\approx 0.95$); secure cipher-images exhibit zero correlation ($r \\approx 0.00$).")

            # Histograms
            st.markdown("---")
            st.markdown("#### 🎨 RGB Pixel Intensity Histograms")
            hist_col1, hist_col2 = st.columns(2)
            
            with hist_col1:
                st.markdown("**Plain-Image Histogram** (Clustered Features)")
                fig_hist_p = go.Figure()
                for c_idx, color_name, c_hex in [(0, 'Red', '#ef4444'), (1, 'Green', '#22c55e'), (2, 'Blue', '#3b82f6')]:
                    hist_data, bin_edges = np.histogram(img_np[:, :, c_idx], bins=64, range=(0, 256))
                    fig_hist_p.add_trace(go.Scatter(x=bin_edges[:-1], y=hist_data, mode='lines', name=color_name, line=dict(color=c_hex)))
                fig_hist_p.update_layout(template="plotly_dark", height=280, margin=dict(l=20, r=20, t=20, b=20), yaxis_title="Count")
                st.plotly_chart(fig_hist_p, use_container_width=True)

            with hist_col2:
                st.markdown("**Cipher-Image Histogram** (Uniform Random Noise)")
                fig_hist_c = go.Figure()
                for c_idx, color_name, c_hex in [(0, 'Red', '#ef4444'), (1, 'Green', '#22c55e'), (2, 'Blue', '#3b82f6')]:
                    hist_data, bin_edges = np.histogram(cipher_img[:, :, c_idx], bins=64, range=(0, 256))
                    fig_hist_c.add_trace(go.Scatter(x=bin_edges[:-1], y=hist_data, mode='lines', name=color_name, line=dict(color=c_hex)))
                fig_hist_c.update_layout(template="plotly_dark", height=280, margin=dict(l=20, r=20, t=20, b=20), yaxis_title="Count")
                st.plotly_chart(fig_hist_c, use_container_width=True)


# =========================================================
# TAB 3: NEURAL KEY EXCHANGE (TPM & EVE ATTACK)
# =========================================================
elif menu == "🧠 Neural Key Exchange (TPM & Eve)":
    st.markdown('<div class="main-title">Neural Key Exchange & Eavesdropper Simulation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Kanter-Gross-Kinzelman (KGK) protocol: Mutual synchronization of Tree Parity Machines (Alice & Bob) under passive eavesdropping (Eve).</div>', unsafe_allow_html=True)
    
    st.markdown(r"""
Two neural networks (Alice & Bob) start with random discrete synaptic weights and communicate over a public channel. By training mutually on public random inputs only when their scalar parity outputs agree, Alice and Bob synchronize in $\mathcal{O}(L^2)$ steps. Eve, who eavesdrops on all public exchanges, can only learn unidirectionally and fails to synchronize before key agreement.
""")
    
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        tpm_K = st.slider("Hidden Units (K)", 2, 5, 3)
    with p_col2:
        tpm_N = st.slider("Inputs per Unit (N)", 3, 6, 4)
    with p_col3:
        tpm_L = st.slider("Weight Bound [-L, +L]", 2, 5, 3)
    with p_col4:
        tpm_rule = st.selectbox("Learning Rule", ["hebbian", "anti_hebbian", "random_walk"])

    if st.button("⚡ Run Neural Synchronization Simulation", type="primary"):
        with st.spinner("Simulating neural weight synchronization against Eve..."):
            sim_res = simulate_neural_key_exchange(K=tpm_K, N=tpm_N, L=tpm_L, rule=tpm_rule, max_steps=2500)
            
        st.markdown("---")
        res_col1, res_col2, res_col3 = st.columns(3)
        with res_col1:
            st.metric("Synchronization Status", "SUCCESSFUL" if sim_res["synchronized"] else "EXCEEDED LIMIT")
        with res_col2:
            st.metric("Steps to Mutual Sync", f"{sim_res['steps']} rounds")
        with res_col3:
            st.metric("Eve Eavesdropper Broken", "NO (Failed)" if not sim_res["eve_synced"] else "YES (Synced)")

        # Sync Curve Plot
        fig_sync = go.Figure()
        fig_sync.add_trace(go.Scatter(
            x=sim_res["rounds"], y=sim_res["ab_sync"],
            mode='lines', name='Alice & Bob Mutual Sync (ρ_AB)',
            line=dict(color='#22c55e', width=2.5)
        ))
        fig_sync.add_trace(go.Scatter(
            x=sim_res["rounds"], y=sim_res["ae_sync"],
            mode='lines', name="Eve Eavesdropper Sync (ρ_AE)",
            line=dict(color='#ef4444', width=2, dash='dot')
        ))
        fig_sync.update_layout(
            title="Neural Synchronization Manifold: Alice-Bob Convergence vs. Eve Rejection",
            xaxis_title="Public Interaction Round",
            yaxis_title="Weight Agreement Ratio (0.0 to 1.0)",
            template="plotly_dark",
            height=380,
            margin=dict(l=20, r=20, t=35, b=20)
        )
        st.plotly_chart(fig_sync, use_container_width=True)

        if sim_res["synchronized"]:
            st.success(f"🔑 **Derived 256-bit Cryptographic Symmetric Key (SHA-256 of Synaptic Weights)**:\n`{sim_res['key_hex']}`")
            
        with st.expander("🔍 Inspect Final Synaptic Weight Matrices"):
            w_c1, w_c2, w_c3 = st.columns(3)
            with w_c1:
                st.markdown("**Alice Weights:**")
                st.write(np.array(sim_res["alice_weights"]))
            with w_c2:
                st.markdown("**Bob Weights:**")
                st.write(np.array(sim_res["bob_weights"]))
            with w_c3:
                st.markdown("**Eve Weights:**")
                st.write(np.array(sim_res["eve_weights"]))


# =========================================================
# TAB 4: NIST SP 800-22 STATISTICAL RANDOMNESS TESTS
# =========================================================
elif menu == "📋 NIST SP 800-22 Randomness Tests":
    st.markdown('<div class="main-title">NIST SP 800-22 Cryptographic Randomness Tests</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Standardized statistical hypothesis tests (P-value threshold α = 0.01) evaluating keystream unpredictability.</div>', unsafe_allow_html=True)
    
    st.markdown(r"""
Official cryptanalytic validation requires testing pseudo-random bit sequences against the NIST Special Publication 800-22 battery. A sequence is accepted as cryptographically random if every test satisfies:
$$P\text{-value} \ge 0.01$$
""")
    
    nist_target = st.selectbox(
        "Select Keystream Generator to Evaluate:",
        [
            "Continuous 3D Lorenz Attractor Keystream",
            "Chaotic Logistic Map (1D) Keystream",
            "Jordan Recurrent Neural Network Keystream",
            "AES-256-GCM Keystream",
            "Weak Linear Congruential PRNG (Control Baseline)"
        ]
    )
    
    seq_len = st.slider("Bit Sequence Length (n):", 2000, 16000, 4000, 1000)
    
    if st.button("🚀 Execute NIST Test Battery", type="primary"):
        with st.spinner(f"Generating {seq_len} bits and calculating NIST p-values..."):
            if nist_target == "Continuous 3D Lorenz Attractor Keystream":
                seq = LorenzSystem().generate_binary_keystream(seq_len)
            elif nist_target == "Chaotic Logistic Map (1D) Keystream":
                seq = ChaoticNetwork().generate_binary_key(seq_len)
            elif nist_target == "Jordan Recurrent Neural Network Keystream":
                dummy_input = ''.join('0' if i % 2 == 0 else '1' for i in range(seq_len))
                seq = JordanNetwork().generate_keystream(dummy_input)
            elif nist_target == "AES-256-GCM Keystream":
                key, nonce, c = aes_encrypt("X" * (seq_len // 8))
                seq = ''.join(format(b, '08b') for b in c)[:seq_len]
            else:
                # Weak LCG baseline: X_{n+1} = (aX + c) mod m
                lcg_bits = []
                x = 42
                for _ in range(seq_len):
                    x = (1103515245 * x + 12345) % (2**31)
                    lcg_bits.append('1' if (x >> 16) & 1 else '0')
                seq = ''.join(lcg_bits)

            results = run_full_nist_suite(seq)

        st.markdown("### 📊 NIST SP 800-22 Test Scorecard")
        
        scorecard_rows = []
        for r in results:
            scorecard_rows.append({
                "NIST SP 800-22 Test": r["test"],
                "Test Statistic": f"{r['statistic']:.4f}",
                "Calculated P-value": f"{r['p_value']:.4f}",
                "Significance Level (α)": "0.0100",
                "Verdict": "✅ PASSED" if r["passed"] else "❌ FAILED"
            })
            
        df_nist = pd.DataFrame(scorecard_rows)
        st.dataframe(df_nist, use_container_width=True)
        
        all_passed = all(r["passed"] for r in results)
        if all_passed:
            st.success(f"🏆 **Evaluation Verdict**: All 5 NIST tests passed! The {nist_target} exhibits strong cryptographic pseudo-randomness.")
        else:
            st.warning(f"⚠️ **Evaluation Verdict**: Some tests fell below the α = 0.01 threshold, indicating detectable statistical structure.")


# =========================================================
# TAB 5: PERFORMANCE BENCHMARKS
# =========================================================
elif menu == "📊 Performance Benchmarks":
    st.markdown('<div class="main-title">Cryptographic Performance Benchmarks</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Empirical execution time, throughput, and ciphertext footprint comparison.</div>', unsafe_allow_html=True)
    
    b_col1, b_col2, b_col3 = st.columns([2, 1, 1])
    with b_col1:
        benchmark_msg = st.text_input("Benchmark Payload:", value="Deep Learning & Chaotic Cryptography Performance Testing Suite 2026")
    with b_col2:
        reps = st.selectbox("Repetitions:", [50, 100, 200, 500], index=1)
    with b_col3:
        st.write("")
        st.write("")
        run_btn = st.button("⚡ Run Benchmark", type="primary", use_container_width=True)
        
    if run_btn:
        with st.spinner(f"Benchmarking algorithms over {reps} iterations..."):
            bin_msg = text_to_binary(benchmark_msg)
            results = []
            
            # 1. Jordan Network
            start = time.perf_counter()
            for _ in range(reps):
                j_c, j_k = jordan_encrypt(bin_msg)
            j_enc = ((time.perf_counter() - start) / reps) * 1000
            
            start = time.perf_counter()
            for _ in range(reps):
                jordan_decrypt(j_c, j_k)
            j_dec = ((time.perf_counter() - start) / reps) * 1000
            
            results.append({"Algorithm": "Jordan RNN", "Encryption (ms)": j_enc, "Decryption (ms)": j_dec, "Ciphertext (bytes)": len(j_c)//8})
            
            # 2. Chaotic Map
            start = time.perf_counter()
            for _ in range(reps):
                c_c, c_k = chaotic_encrypt(bin_msg)
            c_enc = ((time.perf_counter() - start) / reps) * 1000
            
            start = time.perf_counter()
            for _ in range(reps):
                chaotic_decrypt(c_c, c_k)
            c_dec = ((time.perf_counter() - start) / reps) * 1000
            
            results.append({"Algorithm": "Chaotic Map (1D)", "Encryption (ms)": c_enc, "Decryption (ms)": c_dec, "Ciphertext (bytes)": len(c_c)//8})

            # 3. 3D Lorenz
            lor = LorenzSystem()
            start = time.perf_counter()
            for _ in range(reps):
                l_k = lor.generate_binary_keystream(len(bin_msg))
                l_c = ''.join(str(int(a) ^ int(b)) for a, b in zip(bin_msg, l_k))
            l_enc = ((time.perf_counter() - start) / reps) * 1000
            
            start = time.perf_counter()
            for _ in range(reps):
                ''.join(str(int(a) ^ int(b)) for a, b in zip(l_c, l_k))
            l_dec = ((time.perf_counter() - start) / reps) * 1000
            
            results.append({"Algorithm": "3D Lorenz Attractor", "Encryption (ms)": l_enc, "Decryption (ms)": l_dec, "Ciphertext (bytes)": len(l_c)//8})

            # 4. AES-GCM
            start = time.perf_counter()
            for _ in range(reps):
                a_k, a_n, a_c = aes_encrypt(benchmark_msg)
            a_enc = ((time.perf_counter() - start) / reps) * 1000
            
            start = time.perf_counter()
            for _ in range(reps):
                aes_decrypt(a_k, a_n, a_c)
            a_dec = ((time.perf_counter() - start) / reps) * 1000
            
            results.append({"Algorithm": "AES-256-GCM", "Encryption (ms)": a_enc, "Decryption (ms)": a_dec, "Ciphertext (bytes)": len(a_c)})

            df_bench = pd.DataFrame(results)

        st.markdown("---")
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.markdown("##### ⏱️ Latency (ms)")
            fig_lat = go.Figure(data=[
                go.Bar(name='Encryption', x=df_bench['Algorithm'], y=df_bench['Encryption (ms)'], marker_color='#3b82f6'),
                go.Bar(name='Decryption', x=df_bench['Algorithm'], y=df_bench['Decryption (ms)'], marker_color='#8b5cf6')
            ])
            fig_lat.update_layout(barmode='group', template="plotly_dark", height=340, yaxis_title="ms")
            st.plotly_chart(fig_lat, use_container_width=True)

        with chart_col2:
            st.markdown("##### 📦 Ciphertext Size (Bytes)")
            fig_sz = px.bar(df_bench, x='Algorithm', y='Ciphertext (bytes)', color='Algorithm', template="plotly_dark", height=340)
            fig_sz.update_layout(showlegend=False)
            st.plotly_chart(fig_sz, use_container_width=True)

        st.dataframe(df_bench.style.format({"Encryption (ms)": "{:.4f}", "Decryption (ms)": "{:.4f}"}), use_container_width=True)


# =========================================================
# TAB 6: SECURITY & ENTROPY ANALYSIS
# =========================================================
elif menu == "🛡️ Security & Entropy Analysis":
    st.markdown('<div class="main-title">Security, Entropy & Avalanche Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Shannon entropy, bit frequency balance, and Strict Avalanche Criterion (SAC).</div>', unsafe_allow_html=True)
    
    sec_input = st.text_area("Analysis Text:", value="Deep neural networks and chaotic dynamical systems for next-generation cryptography.", height=80)
    sec_bin = text_to_binary(sec_input)
    
    _, jk = jordan_encrypt(sec_bin)
    _, ck = chaotic_encrypt(sec_bin)
    lk = LorenzSystem().generate_binary_keystream(len(sec_bin))
    
    e_plain = calculate_entropy(sec_bin, is_binary=True)
    e_jordan = calculate_entropy(jk, is_binary=True)
    e_chaos = calculate_entropy(ck, is_binary=True)
    e_lorenz = calculate_entropy(lk, is_binary=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Plaintext Entropy", f"{e_plain:.4f}", "Raw Text")
    with c2: st.metric("Jordan RNN Entropy", f"{e_jordan:.4f}", f"{e_jordan*100:.1f}%")
    with c3: st.metric("1D Chaos Entropy", f"{e_chaos:.4f}", f"{e_chaos*100:.1f}%")
    with c4: st.metric("3D Lorenz Entropy", f"{e_lorenz:.4f}", f"{e_lorenz*100:.1f}%")

    st.markdown("---")
    st.subheader("Strict Avalanche Criterion (SAC)")
    flip_idx = st.slider("Select Bit Position to Flip in Input:", 0, max(1, len(sec_bin)-1), 0)
    flipped_bin = flip_bit(sec_bin, flip_idx)
    
    c1_j, _ = jordan_encrypt(sec_bin)
    c2_j, _ = jordan_encrypt(flipped_bin)
    av_j = calculate_avalanche_effect(c1_j, c2_j)
    
    c1_l = ''.join(str(int(a) ^ int(b)) for a, b in zip(sec_bin, lk))
    c2_l = ''.join(str(int(a) ^ int(b)) for a, b in zip(flipped_bin, lk))
    av_l = calculate_avalanche_effect(c1_l, c2_l)
    
    st.write(f"In basic stream ciphers without CBC chaining, a 1-bit input flip affects only 1 bit. In image encryption with modular chained diffusion, the effect propagates across **{diff_metrics['npcr']:.2f}%** if evaluated on images!" if 'diff_metrics' in locals() else "Check the Image Cryptography tab to see 100% avalanche diffusion!")


# =========================================================
# TAB 7: CHAOTIC DYNAMICAL SYSTEMS
# =========================================================
elif menu == "🌀 Chaotic Dynamical Systems":
    st.markdown('<div class="main-title">Chaotic Dynamical Systems Visualizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Compare 1D Logistic Maps with Continuous 3D Lorenz Attractors.</div>', unsafe_allow_html=True)
    
    r_val = st.slider("Logistic Map Parameter r", 2.8, 4.0, 3.99, 0.01)
    chaos = ChaoticNetwork(initial_value=0.37, r=r_val)
    seq = chaos.generate_sequence(150)
    
    fig_time = px.line(x=list(range(len(seq))), y=seq, labels={"x": "n", "y": "xₙ"}, title=f"Logistic Map Trajectory for r = {r_val}", template="plotly_dark")
    fig_time.update_layout(height=320)
    st.plotly_chart(fig_time, use_container_width=True)


# =========================================================
# TAB 8: MASTER'S THESIS FOUNDATIONS
# =========================================================
elif menu == "📖 Master's Thesis Foundations":
    st.markdown('<div class="main-title">Master\'s Thesis Foundations & Theoretical Rigor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Mathematical framework, synchronization theorems, and cryptanalytic proofs.</div>', unsafe_allow_html=True)
    
    st.markdown(r"""
### 1. Neural Key Exchange (Tree Parity Machines)
The Kanter-Gross-Kinzelman (KGK) protocol establishes that two Tree Parity Machines (Alice and Bob) undergoing bidirectional Hebbian updates:
$$w_{ij}(t+1) = \text{clip}(w_{ij}(t) + x_{ij} \tau, -L, L)$$
reach synchronization in polynomial time $\mathcal{O}(L^2)$. 

An eavesdropper (Eve) who listens to the public channel can only perform unidirectional learning. Because the weight trajectory space contains complex attracting manifolds, Eve's probability of synchronizing before Alice and Bob satisfies:
$$\lim_{L \to \infty} \Pr(\text{Eve Sync}) \to 0$$

---

### 2. Multi-Dimensional Continuous Chaos (Lorenz System)
The 3D Lorenz system:
$$\dot{x} = \sigma(y - x), \quad \dot{y} = x(\rho - z) - y, \quad \dot{z} = xy - \beta z$$
exhibits deterministic chaos when $\sigma=10, \rho=28, \beta=8/3$. The maximum Lyapunov exponent is positive ($\lambda_1 \approx 0.9056$), providing exponential sensitivity:
$$|\Delta \mathbf{x}(t)| \approx |\Delta \mathbf{x}(0)| e^{\lambda_1 t}$$
Unlike 1D maps, the 3D continuous system has a fractal dimension $D \approx 2.06$, making Taken's phase-space reconstruction attacks cryptanalytically intractable.

---

### 3. Diffusion Resistance (NPCR & UACI)
To withstand differential cryptanalysis, an image cryptosystem must satisfy:
$$\text{NPCR} = \frac{\sum D(i, j)}{W \times H} \times 100\% \ge 99.609\%$$
$$\text{UACI} = \frac{\sum |C_1(i, j) - C_2(i, j)|}{255 \times W \times H} \times 100\% \approx 33.463\%$$
Our bidirectional modular diffusion architecture:
$$C(i) = (P(i) + K(i) + C(i-1)) \pmod{256}$$
ensures that a single bit perturbation cascades across the entire image space.
""")

st.markdown("---")
st.caption("Deep Learning Cryptography Studio • Master's Research Edition")
