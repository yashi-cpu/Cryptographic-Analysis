import React from 'react'
import { 
  ShieldCheck, 
  Brain, 
  Waves, 
  AlertTriangle, 
  Layers, 
  GraduationCap, 
  CheckCircle2, 
  Cpu, 
  Binary,
  ArrowRight
} from 'lucide-react'

export default function About() {
  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-12">
      {/* Hero Banner */}
      <div className="bg-gradient-to-br from-gray-900 via-gray-900 to-emerald-950/40 border border-emerald-500/30 rounded-3xl p-8 shadow-2xl relative overflow-hidden">
        <div className="relative z-10 space-y-3">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 text-xs font-mono">
            <GraduationCap className="w-4 h-4" />
            <span>MSc Artificial Intelligence & Machine Learning Project</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            CipherChat: Neural & Chaotic Cryptographic Communications
          </h1>
          <p className="text-gray-300 text-sm max-w-2xl leading-relaxed">
            An academic research laboratory and messaging testbed simulating WhatsApp-style secure communication, demonstrating recurrent neural keystream generation, chaotic dynamical mapping, and standard authenticated encryption.
          </p>
        </div>
      </div>

      {/* Mandatory Academic Disclaimer */}
      <div className="p-5 bg-yellow-500/10 border border-yellow-500/30 rounded-2xl flex items-start space-x-3.5 text-yellow-300 text-xs leading-relaxed">
        <AlertTriangle className="w-5 h-5 shrink-0 mt-0.5 text-yellow-400" />
        <div>
          <h4 className="font-bold text-sm text-yellow-400 mb-1">Academic & Experimental Cryptography Disclaimer</h4>
          <p>
            The <strong>Jordan Neural Network</strong> and <strong>Chaotic Logistic Map</strong> implementations featured in CipherChat are <em>experimental academic demonstrations</em> designed for comparative analysis in an MSc curriculum. They are <strong>NOT</strong> certified, production-grade encryption algorithms. Standard <strong>AES-256-GCM</strong> is provided as the verified authenticated cryptographic baseline.
          </p>
        </div>
      </div>

      {/* 3 Algorithm Explanations */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Jordan Network */}
        <div className="bg-gray-900/70 border border-purple-500/30 rounded-2xl p-5 space-y-3 flex flex-col justify-between">
          <div>
            <div className="w-10 h-10 rounded-xl bg-purple-500/15 border border-purple-500/30 flex items-center justify-center text-purple-400 mb-3">
              <Brain className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-white text-base">Jordan Neural Network</h3>
            <span className="text-[10px] font-mono uppercase text-purple-400 font-semibold block mb-2">Experimental Model</span>
            <p className="text-xs text-gray-400 leading-relaxed">
              A recurrent neural network where the previous output unit is fed back into the context layer. Generates a dynamic keystream conditioned on plaintext bits and internal state recurrence.
            </p>
          </div>
          <div className="pt-3 border-t border-gray-800 text-[11px] font-mono text-purple-300/80">
            Activation: Tanh + Sigmoid • XOR Stream
          </div>
        </div>

        {/* Chaotic Network */}
        <div className="bg-gray-900/70 border border-pink-500/30 rounded-2xl p-5 space-y-3 flex flex-col justify-between">
          <div>
            <div className="w-10 h-10 rounded-xl bg-pink-500/15 border border-pink-500/30 flex items-center justify-center text-pink-400 mb-3">
              <Waves className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-white text-base">Chaotic Logistic Map</h3>
            <span className="text-[10px] font-mono uppercase text-pink-400 font-semibold block mb-2">Nonlinear Dynamical Map</span>
            <p className="text-xs text-gray-400 leading-relaxed">
              Uses the non-linear recursion <span className="font-mono text-white">x(n+1) = r · x(n) · (1 - x(n))</span> with <span className="font-mono text-white">r = 3.99</span> to produce deterministic, non-periodic chaotic sequences for keystream generation.
            </p>
          </div>
          <div className="pt-3 border-t border-gray-800 text-[11px] font-mono text-pink-300/80">
            Param: r = 3.99 • Arnold Cat Map (Images)
          </div>
        </div>

        {/* AES-GCM */}
        <div className="bg-gray-900/70 border border-emerald-500/30 rounded-2xl p-5 space-y-3 flex flex-col justify-between">
          <div>
            <div className="w-10 h-10 rounded-xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-400 mb-3">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-white text-base">AES-256-GCM</h3>
            <span className="text-[10px] font-mono uppercase text-emerald-400 font-semibold block mb-2">Authenticated Standard (AEAD)</span>
            <p className="text-xs text-gray-400 leading-relaxed">
              Industry gold-standard authenticated encryption. Utilizes counter mode (CTR) for confidentiality and Galois multiplication for a 128-bit authentication tag ensuring message integrity.
            </p>
          </div>
          <div className="pt-3 border-t border-gray-800 text-[11px] font-mono text-emerald-300/80">
            256-bit Key • 96-bit Nonce • Tamper-proof
          </div>
        </div>
      </div>

      {/* System Architecture Diagram */}
      <div className="bg-gray-900/70 border border-gray-800 rounded-2xl p-6 shadow-lg space-y-4">
        <h3 className="font-bold text-sm text-white flex items-center space-x-2">
          <Layers className="w-4 h-4 text-emerald-400" />
          <span>Full-Stack System Architecture</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs font-mono text-center">
          <div className="p-4 bg-gray-950 rounded-xl border border-gray-800">
            <span className="text-emerald-400 font-bold block mb-1">FRONTEND LAYER</span>
            <span className="text-gray-400 text-[11px]">React 19 • Vite • Tailwind v4 • Framer Motion • Recharts</span>
          </div>

          <div className="p-4 bg-gray-950 rounded-xl border border-gray-800">
            <span className="text-purple-400 font-bold block mb-1">API GATEWAY</span>
            <span className="text-gray-400 text-[11px]">FastAPI (Python) • Uvicorn • REST Endpoints • CORS</span>
          </div>

          <div className="p-4 bg-gray-950 rounded-xl border border-gray-800">
            <span className="text-pink-400 font-bold block mb-1">CRYPTOGRAPHIC ENGINES</span>
            <span className="text-gray-400 text-[11px]">Jordan RNN • 3D Lorenz RK4 • NumPy • Cryptography.io AESGCM</span>
          </div>
        </div>
      </div>
    </div>
  )
}
