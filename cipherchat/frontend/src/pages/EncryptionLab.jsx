import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Play, 
  RotateCcw, 
  CheckCircle2, 
  XCircle, 
  Brain, 
  Waves, 
  ShieldCheck, 
  ArrowRight, 
  Binary, 
  Key, 
  Cpu, 
  Lock,
  Unlock,
  Sparkles
} from 'lucide-react'
import AlgorithmBadge from '../components/AlgorithmBadge'
import { API_BASE } from '../api'

export default function EncryptionLab() {
  const [message, setMessage] = useState('Confidential transmission over experimental neural channel.')
  const [algorithm, setAlgorithm] = useState('jordan')
  const [isProcessing, setIsProcessing] = useState(false)
  const [pipelineData, setPipelineData] = useState(null)
  const [animationStep, setAnimationStep] = useState(0)

  const handleRunPipeline = async () => {
    if (!message.trim() || isProcessing) return
    setIsProcessing(true)
    setAnimationStep(1) // Step 1: Plaintext Encoding

    try {
      // 1. Call Encrypt API
      const encRes = await fetch(`${API_BASE}/api/encrypt-text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, algorithm, sender: 'alice' })
      })

      if (!encRes.ok) throw new Error('Encryption failed')
      const encData = await encRes.json()

      // Animate steps
      setAnimationStep(2) // Algorithm transformation
      await new Promise(r => setTimeout(r, 500))

      setAnimationStep(3) // Ciphertext generated
      await new Promise(r => setTimeout(r, 500))

      // 2. Call Decrypt API
      const decRes = await fetch(`${API_BASE}/api/decrypt-text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ciphertext_hex: encData.ciphertext_hex,
          key_info: encData.key_info,
          algorithm
        })
      })

      if (!decRes.ok) throw new Error('Decryption failed')
      const decData = await decRes.json()

      setAnimationStep(4) // Decryption
      await new Promise(r => setTimeout(r, 400))

      setAnimationStep(5) // Complete

      setPipelineData({
        plaintext: message,
        binary: encData.binary_plaintext,
        algorithm,
        ciphertextHex: encData.ciphertext_hex,
        keyInfo: encData.key_info,
        encTime: encData.encryption_time_ms,
        decTime: decData.decryption_time_ms,
        recoveredText: decData.plaintext,
        isMatch: decData.plaintext === message
      })
    } catch (err) {
      console.error(err)
    } finally {
      setIsProcessing(false)
    }
  }

  const handleReplayAnimation = async () => {
    if (!pipelineData || isProcessing) return
    setIsProcessing(true)
    for (let step = 1; step <= 5; step++) {
      setAnimationStep(step)
      await new Promise(r => setTimeout(r, 450))
    }
    setIsProcessing(false)
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-10">
      {/* Page Header */}
      <div>
        <div className="flex items-center space-x-2">
          <h1 className="text-2xl font-extrabold text-white tracking-tight">Live Encryption Lab</h1>
          <span className="text-xs px-2.5 py-0.5 rounded-full bg-purple-500/15 text-purple-400 font-mono border border-purple-500/30">
            Step-by-Step Visualization
          </span>
        </div>
        <p className="text-sm text-gray-400 mt-1">
          Observe how plaintext undergoes binary serialization, non-linear keystream mixing, transmission, and stateful decryption.
        </p>
      </div>

      {/* Input & Control Card */}
      <div className="bg-gray-900/80 border border-gray-800 rounded-2xl p-5 shadow-lg backdrop-blur space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-2 space-y-1.5">
            <label className="text-xs font-mono font-medium text-gray-300">Plaintext Payload:</label>
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Enter text to encrypt..."
              className="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors font-mono"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-mono font-medium text-gray-300">Cryptographic Algorithm:</label>
            <select
              value={algorithm}
              onChange={(e) => setAlgorithm(e.target.value)}
              className="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors font-mono"
            >
              <option value="jordan">Jordan Recurrent Neural Network (Experimental)</option>
              <option value="chaotic">Chaotic Logistic Map (Experimental)</option>
              <option value="aes">AES-256-GCM (Authenticated Standard)</option>
            </select>
          </div>
        </div>

        <div className="flex items-center space-x-3 pt-2">
          <button
            onClick={handleRunPipeline}
            disabled={isProcessing || !message.trim()}
            className="flex items-center space-x-2 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-40 text-black font-semibold px-5 py-2.5 rounded-xl transition-all shadow-md shadow-emerald-500/20 text-sm"
          >
            <Play className="w-4 h-4 fill-current" />
            <span>{isProcessing ? 'Processing Pipeline...' : 'Run Encryption Pipeline'}</span>
          </button>

          {pipelineData && (
            <button
              onClick={handleReplayAnimation}
              disabled={isProcessing}
              className="flex items-center space-x-2 bg-gray-800 hover:bg-gray-700 text-gray-200 font-medium px-4 py-2.5 rounded-xl transition-all border border-gray-700 text-sm"
            >
              <RotateCcw className="w-4 h-4" />
              <span>Show Encryption Process</span>
            </button>
          )}
        </div>
      </div>

      {/* Visual Pipeline Stages */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
        {[
          { step: 1, title: '1. Plaintext Encoding', desc: 'UTF-8 to Binary representation', icon: Binary },
          { step: 2, title: '2. Encryption Engine', desc: 'Keystream & State Evolution', icon: Cpu },
          { step: 3, title: '3. Ciphertext Output', desc: 'Hex serialized payload', icon: Lock },
          { step: 4, title: '4. Receiver Decryption', desc: 'Shared secret state recovery', icon: Unlock },
          { step: 5, title: '5. Plaintext Recovery', desc: 'Bitwise equality verification', icon: CheckCircle2 },
        ].map((item) => {
          const Icon = item.icon
          const isActive = animationStep === item.step
          const isDone = animationStep >= item.step
          return (
            <motion.div
              key={item.step}
              animate={{
                scale: isActive ? 1.03 : 1,
                borderColor: isActive ? '#10b981' : isDone ? '#059669' : '#1f2937'
              }}
              className={`p-4 rounded-2xl border transition-all ${
                isActive
                  ? 'bg-emerald-500/10 shadow-lg shadow-emerald-500/10'
                  : isDone
                  ? 'bg-gray-900/80 border-gray-700'
                  : 'bg-gray-950/40 border-gray-800/80 opacity-60'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${isActive ? 'bg-emerald-500 text-black' : isDone ? 'bg-gray-800 text-emerald-400' : 'bg-gray-900 text-gray-500'}`}>
                  <Icon className="w-4 h-4" />
                </div>
                {isDone && <span className="text-[10px] font-mono text-emerald-400">DONE</span>}
              </div>
              <h4 className="text-xs font-bold text-white tracking-tight">{item.title}</h4>
              <p className="text-[11px] text-gray-400 mt-0.5">{item.desc}</p>
            </motion.div>
          )
        })}
      </div>

      {/* Deep-Dive Inspection Panels */}
      {pipelineData && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {/* Left Panel: Ciphertext & Key details */}
          <div className="bg-gray-900/70 border border-gray-800 rounded-2xl p-5 space-y-4">
            <div className="flex items-center justify-between border-b border-gray-800 pb-3">
              <h3 className="font-bold text-sm text-white flex items-center space-x-2">
                <Lock className="w-4 h-4 text-emerald-400" />
                <span>Cryptographic Output & Key Info</span>
              </h3>
              <AlgorithmBadge algorithm={pipelineData.algorithm} />
            </div>

            <div className="space-y-3 font-mono text-xs">
              <div>
                <p className="text-gray-400 mb-1">Binary Plaintext ({pipelineData.binary.length} bits):</p>
                <div className="p-3 rounded-xl bg-gray-950 border border-gray-800 text-purple-300 break-all max-h-24 overflow-y-auto">
                  {pipelineData.binary}
                </div>
              </div>

              <div>
                <p className="text-gray-400 mb-1">Generated Ciphertext (Hex):</p>
                <div className="p-3 rounded-xl bg-gray-950 border border-gray-800 text-emerald-400 break-all max-h-24 overflow-y-auto font-bold">
                  {pipelineData.ciphertextHex}
                </div>
              </div>

              <div>
                <p className="text-gray-400 mb-1">Shared Secret / Key State:</p>
                <div className="p-3 rounded-xl bg-gray-950 border border-gray-800 text-gray-300 break-all max-h-24 overflow-y-auto text-[11px]">
                  {JSON.stringify(pipelineData.keyInfo, null, 2)}
                </div>
              </div>
            </div>
          </div>

          {/* Right Panel: Verification & Performance */}
          <div className="bg-gray-900/70 border border-gray-800 rounded-2xl p-5 space-y-4">
            <div className="flex items-center justify-between border-b border-gray-800 pb-3">
              <h3 className="font-bold text-sm text-white flex items-center space-x-2">
                <Unlock className="w-4 h-4 text-emerald-400" />
                <span>Decryption Verification & Latency</span>
              </h3>
              <span className={`px-2.5 py-0.5 rounded-full text-xs font-mono font-bold flex items-center space-x-1 ${pipelineData.isMatch ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-red-500/20 text-red-400'}`}>
                {pipelineData.isMatch ? <CheckCircle2 className="w-3.5 h-3.5" /> : <XCircle className="w-3.5 h-3.5" />}
                <span>{pipelineData.isMatch ? 'EXACT MATCH' : 'MISMATCH'}</span>
              </span>
            </div>

            <div className="space-y-4">
              <div>
                <p className="text-xs text-gray-400 mb-1 font-mono">Original Message:</p>
                <div className="p-3 rounded-xl bg-gray-950 border border-gray-800 text-sm text-white">
                  "{pipelineData.plaintext}"
                </div>
              </div>

              <div>
                <p className="text-xs text-gray-400 mb-1 font-mono">Recovered Decrypted Message:</p>
                <div className="p-3 rounded-xl bg-gray-950 border border-gray-800 text-sm text-emerald-300 font-semibold">
                  "{pipelineData.recoveredText}"
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3 pt-2">
                <div className="p-3 bg-gray-950/80 rounded-xl border border-gray-800">
                  <p className="text-[11px] text-gray-500 uppercase font-mono">Encryption Latency</p>
                  <p className="text-lg font-bold text-white font-mono mt-0.5">{pipelineData.encTime} ms</p>
                </div>
                <div className="p-3 bg-gray-950/80 rounded-xl border border-gray-800">
                  <p className="text-[11px] text-gray-500 uppercase font-mono">Decryption Latency</p>
                  <p className="text-lg font-bold text-white font-mono mt-0.5">{pipelineData.decTime} ms</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
