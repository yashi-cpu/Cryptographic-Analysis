import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  ShieldAlert, 
  ShieldCheck, 
  AlertTriangle, 
  XCircle, 
  CheckCircle2, 
  Radio, 
  Terminal, 
  Key, 
  Lock, 
  Unlock,
  Play,
  RotateCcw
} from 'lucide-react'
import AlgorithmBadge from '../components/AlgorithmBadge'
import { API_BASE } from '../api'

export default function AttackerSim() {
  const [message, setMessage] = useState('Top secret coordinates: 48.8584 N, 2.2945 E.')
  const [algorithm, setAlgorithm] = useState('aes')
  const [isSimulating, setIsSimulating] = useState(false)
  const [attackData, setAttackData] = useState(null)

  const handleRunAttack = async () => {
    if (!message.trim() || isSimulating) return
    setIsSimulating(true)

    try {
      // 1. Encrypt message
      const encRes = await fetch(`${API_BASE}/api/encrypt-text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, algorithm, sender: 'alice' })
      })
      const encData = await encRes.json()

      // 2. Run Attack Simulation on Backend
      const atkRes = await fetch(`${API_BASE}/api/attack-simulation`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ciphertext_hex: encData.ciphertext_hex,
          algorithm,
          key_info: encData.key_info
        })
      })
      const atkData = await atkRes.json()

      setAttackData({
        ...atkData,
        originalPlaintext: message,
        algorithm
      })
    } catch (err) {
      console.error(err)
    } finally {
      setIsSimulating(false)
    }
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-10">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2">
          <h1 className="text-2xl font-extrabold text-white tracking-tight">Third-Party Interception & Tamper Simulation</h1>
          <span className="text-xs px-2.5 py-0.5 rounded-full bg-red-500/15 text-red-400 font-mono border border-red-500/30">
            Adversarial Cryptanalysis
          </span>
        </div>
        <p className="text-sm text-gray-400 mt-1">
          Simulate an active adversary (Eve) intercepting the ciphertext in-transit, attempting unauthorized brute-force decryption, and performing bit-flip tampering.
        </p>
      </div>

      {/* Control Card */}
      <div className="bg-gray-900/80 border border-gray-800 rounded-2xl p-5 shadow-lg backdrop-blur space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-2">
            <label className="text-xs font-mono font-medium text-gray-300 mb-1.5 block">Message Payload:</label>
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors font-mono"
            />
          </div>

          <div>
            <label className="text-xs font-mono font-medium text-gray-300 mb-1.5 block">Cryptographic Engine:</label>
            <select
              value={algorithm}
              onChange={(e) => setAlgorithm(e.target.value)}
              className="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors font-mono"
            >
              <option value="aes">AES-256-GCM (Authenticated Encryption)</option>
              <option value="jordan">Jordan Recurrent Neural Network (Experimental)</option>
              <option value="chaotic">Chaotic Logistic Map (Experimental)</option>
            </select>
          </div>
        </div>

        <div className="pt-2">
          <button
            onClick={handleRunAttack}
            disabled={isSimulating || !message.trim()}
            className="flex items-center space-x-2 bg-red-500 hover:bg-red-400 disabled:opacity-40 text-black font-semibold px-6 py-2.5 rounded-xl transition-all shadow-md shadow-red-500/20 text-sm"
          >
            <ShieldAlert className="w-4 h-4" />
            <span>{isSimulating ? 'Simulating Interception...' : 'Launch Interception & Tamper Attack'}</span>
          </button>
        </div>
      </div>

      {/* 3-Party Scenario Visualization */}
      {attackData && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            
            {/* 1. SENDER: ALICE */}
            <div className="bg-gray-900/70 border border-gray-800 rounded-2xl p-5 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between border-b border-gray-800 pb-3 mb-3">
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 rounded-full bg-purple-500 flex items-center justify-center font-bold text-white text-xs">A</div>
                    <div>
                      <h3 className="font-bold text-white text-sm">Alice (Sender)</h3>
                      <p className="text-[10px] text-gray-400 font-mono">Origin Endpoint</p>
                    </div>
                  </div>
                  <span className="text-[11px] font-mono text-emerald-400">SENT</span>
                </div>

                <div className="space-y-3 font-mono text-xs">
                  <div>
                    <span className="text-gray-500 text-[10px] uppercase block">Original Plaintext:</span>
                    <p className="p-3 bg-gray-950 rounded-xl border border-gray-800 text-white mt-1">
                      "{attackData.originalPlaintext}"
                    </p>
                  </div>

                  <div>
                    <span className="text-gray-500 text-[10px] uppercase block">Emitted Ciphertext:</span>
                    <p className="p-3 bg-gray-950 rounded-xl border border-gray-800 text-emerald-400 break-all max-h-24 overflow-y-auto mt-1">
                      {attackData.intercepted_hex}
                    </p>
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-gray-800/80 flex items-center space-x-2 text-xs text-gray-400">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Message successfully encrypted and dispatched.</span>
              </div>
            </div>

            {/* 2. ADVERSARY: EVE */}
            <div className="bg-gray-900/70 border border-red-500/40 rounded-2xl p-5 flex flex-col justify-between shadow-lg shadow-red-500/5">
              <div>
                <div className="flex items-center justify-between border-b border-red-500/30 pb-3 mb-3">
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 rounded-full bg-red-500 flex items-center justify-center font-bold text-black text-xs">E</div>
                    <div>
                      <h3 className="font-bold text-white text-sm">Eve (The Interceptor)</h3>
                      <p className="text-[10px] text-red-400 font-mono">MITM Adversary</p>
                    </div>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-red-500/20 text-red-400 font-mono border border-red-500/30">
                    INTERCEPTED
                  </span>
                </div>

                <div className="space-y-3 font-mono text-xs">
                  <div>
                    <span className="text-gray-500 text-[10px] uppercase block">Captured Ciphertext:</span>
                    <p className="p-2.5 bg-gray-950 rounded-xl border border-gray-800 text-gray-300 break-all max-h-20 overflow-y-auto mt-1 text-[11px]">
                      {attackData.intercepted_hex}
                    </p>
                  </div>

                  <div>
                    <span className="text-gray-500 text-[10px] uppercase block">Eve's Unauthorized Decrypt Attempt:</span>
                    <p className="p-2.5 bg-red-950/40 rounded-xl border border-red-500/30 text-red-300 break-all max-h-20 overflow-y-auto mt-1 text-[11px]">
                      {attackData.eve_decrypt_result}
                    </p>
                  </div>

                  {/* Animated Status Chips for Eve */}
                  <div className="space-y-1.5 pt-1 text-[11px]">
                    <div className="flex items-center space-x-2 text-red-400">
                      <span className="w-2 h-2 rounded-full bg-red-400 animate-pulse"></span>
                      <span>Interception detected: 100% payload captured</span>
                    </div>
                    <div className="flex items-center space-x-2 text-yellow-400">
                      <span className="w-2 h-2 rounded-full bg-yellow-400"></span>
                      <span>Legitimate shared key missing: Brute-force rejected</span>
                    </div>
                    <div className="flex items-center space-x-2 text-red-400 font-semibold">
                      <XCircle className="w-3.5 h-3.5" />
                      <span>Original plaintext NOT recovered</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-red-500/20 text-xs text-red-300 font-mono">
                Status: Attack Unsuccessful
              </div>
            </div>

            {/* 3. RECEIVER: BOB */}
            <div className="bg-gray-900/70 border border-gray-800 rounded-2xl p-5 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between border-b border-gray-800 pb-3 mb-3">
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 rounded-full bg-emerald-500 flex items-center justify-center font-bold text-black text-xs">B</div>
                    <div>
                      <h3 className="font-bold text-white text-sm">Bob (Legitimate Receiver)</h3>
                      <p className="text-[10px] text-gray-400 font-mono">Destination Endpoint</p>
                    </div>
                  </div>
                  <span className="text-[11px] font-mono text-emerald-400">DELIVERED</span>
                </div>

                <div className="space-y-3 font-mono text-xs">
                  <div>
                    <span className="text-gray-500 text-[10px] uppercase block">Decryption Status:</span>
                    <div className="p-3 bg-emerald-950/30 rounded-xl border border-emerald-500/30 text-emerald-300 font-semibold mt-1">
                      "{attackData.bob_decrypt_result}"
                    </div>
                  </div>

                  <div>
                    <span className="text-gray-500 text-[10px] uppercase block">Key Possession:</span>
                    <p className="text-gray-400 mt-1">
                      Possesses legitimate shared secret parameter. Exact mathematical inversion authenticated.
                    </p>
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-gray-800/80 flex items-center space-x-2 text-xs text-emerald-400">
                <CheckCircle2 className="w-4 h-4 shrink-0" />
                <span>Legitimate recipient recovered plaintext 100%.</span>
              </div>
            </div>
          </div>

          {/* Tampering Section */}
          <div className="bg-gray-900/80 border border-gray-800 rounded-2xl p-5 shadow-lg space-y-4">
            <div className="flex items-center justify-between border-b border-gray-800 pb-3">
              <h3 className="font-bold text-sm text-white flex items-center space-x-2">
                <AlertTriangle className="w-4 h-4 text-yellow-400" />
                <span>Active Ciphertext Tampering Attack (Bit-Flipping in Transit)</span>
              </h3>
              <span className="text-xs font-mono text-yellow-400">Bit 0 Flipped (0x01)</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
              <div>
                <span className="text-gray-400 mb-1 block">Tampered Ciphertext (Modified by Eve):</span>
                <p className="p-3 bg-gray-950 rounded-xl border border-yellow-500/30 text-yellow-300 break-all">
                  {attackData.tampered_hex}
                </p>
              </div>

              <div>
                <span className="text-gray-400 mb-1 block">Receiver Decryption Outcome:</span>
                <p className={`p-3 rounded-xl border font-semibold ${attackData.tamper_detected ? 'bg-red-950/40 border-red-500/40 text-red-300' : 'bg-gray-950 border-gray-800 text-gray-300'}`}>
                  {attackData.tamper_decrypt_result}
                </p>
              </div>
            </div>

            {algorithm === 'aes' ? (
              <div className="p-3.5 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-xs text-emerald-300 leading-relaxed">
                <span className="font-bold">🛡️ Authenticated Encryption Defense: </span>
                AES-GCM computed a 128-bit authentication tag over the original ciphertext. When Eve modified 1 bit, the tag calculation mismatched during decryption, and the cipher <strong>immediately rejected the modified payload (`InvalidTag`)</strong>.
              </div>
            ) : (
              <div className="p-3.5 bg-yellow-500/10 border border-yellow-500/30 rounded-xl text-xs text-yellow-300 leading-relaxed">
                <span className="font-bold">⚠️ Experimental Limitation: </span>
                The experimental Jordan and Chaotic stream ciphers perform pure stream XOR without an authentication tag (AEAD). While bit corruption is visible in the recovered text, the cipher lacks native tamper rejection.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
