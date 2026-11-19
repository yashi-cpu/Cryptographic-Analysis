import React, { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Send, 
  Lock, 
  CheckCheck, 
  ArrowRight, 
  Terminal, 
  ShieldCheck, 
  ShieldAlert,
  Cpu, 
  Waves, 
  Brain,
  Eye,
  EyeOff,
  Skull,
  Radio,
  XCircle,
  KeyRound,
  AlertTriangle,
  Copy,
  Check,
  Paperclip,
  Image as ImageIcon,
  X,
  Sparkles
} from 'lucide-react'
import AlgorithmBadge from '../components/AlgorithmBadge'
import { API_BASE } from '../api'

export default function SecureChat() {
  const [algorithm, setAlgorithm] = useState('jordan')
  const [aliceInput, setAliceInput] = useState('')
  const [bobInput, setBobInput] = useState('')
  const [aliceImage, setAliceImage] = useState(null) // { file, previewUrl }
  const [bobImage, setBobImage] = useState(null)
  const [showEve, setShowEve] = useState(true) // Toggle 3rd person interceptor view

  const aliceFileRef = useRef(null)
  const bobFileRef = useRef(null)

  // Chat message history with key info for demonstration
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'alice',
      type: 'text',
      plaintext: 'Meet me at 5 PM.',
      ciphertextHex: '0x9102c35682c34047555682d14f5595',
      algorithm: 'jordan',
      timestamp: '10:24 AM',
      keyInfo: { bit_length: 120, keystream: '10010110...' },
      eveDecryptAttempt: null,
      status: 'delivered'
    },
    {
      id: 2,
      sender: 'bob',
      type: 'text',
      plaintext: 'Understood. Is the channel secure?',
      ciphertextHex: '0xc9a4271a16bfaf7144e617d0bd1744',
      algorithm: 'chaotic',
      timestamp: '10:25 AM',
      keyInfo: { bit_length: 272, keystream: '11001010...' },
      eveDecryptAttempt: null,
      status: 'delivered'
    }
  ])

  // Transmission state
  const [isTransmitting, setIsTransmitting] = useState(false)
  const [activeStep, setActiveStep] = useState(0) // 0: idle, 1: Alice Encrypts, 2: Eve Intercepts, 3: Bob Decrypts
  const [currentCiphertext, setCurrentCiphertext] = useState('')
  const [copiedId, setCopiedId] = useState(null)

  const [activityLogs, setActivityLogs] = useState([
    { time: '10:24:00', text: 'Secure session established between Alice and Bob.' },
    { time: '10:24:01', text: 'Alice encrypted: "Meet me at 5 PM." using Jordan RNN.' },
    { time: '10:24:01', text: '⚠️ Eve intercepted ciphertext packet 0x9102c3... on public wire.' },
    { time: '10:24:02', text: 'Bob verified and decrypted message payload.' },
  ])

  const chatEndRef = useRef(null)

  const addLog = (text) => {
    const now = new Date()
    const timeStr = now.toTimeString().split(' ')[0]
    setActivityLogs(prev => [...prev.slice(-30), { time: timeStr, text }])
  }

  const handleCopyCipher = (id, text) => {
    navigator.clipboard.writeText(text)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 1500)
  }

  // Quick generator for a test graphic sample
  const createSampleBlob = (label = 'CIPHER') => {
    const canvas = document.createElement('canvas')
    canvas.width = 128
    canvas.height = 128
    const ctx = canvas.getContext('2d')
    
    // Background gradient
    const grad = ctx.createLinearGradient(0, 0, 128, 128)
    grad.addColorStop(0, '#10b981')
    grad.addColorStop(0.5, '#3b82f6')
    grad.addColorStop(1, '#a855f7')
    ctx.fillStyle = grad
    ctx.fillRect(0, 0, 128, 128)
    
    // Geometric high-contrast target
    ctx.fillStyle = '#facc15'
    ctx.beginPath()
    ctx.arc(64, 64, 38, 0, Math.PI * 2)
    ctx.fill()
    
    ctx.fillStyle = '#0f172a'
    ctx.fillRect(46, 46, 36, 36)

    ctx.fillStyle = '#ffffff'
    ctx.font = 'bold 12px monospace'
    ctx.textAlign = 'center'
    ctx.fillText(label, 64, 68)

    return new Promise(resolve => {
      canvas.toBlob((blob) => {
        const file = new File([blob], `sample_${label.toLowerCase()}.png`, { type: 'image/png' })
        resolve(file)
      }, 'image/png')
    })
  }

  const handleAttachSample = async (sender) => {
    const file = await createSampleBlob(sender === 'alice' ? 'TOP_SECRET' : 'CONFIRMED')
    const previewUrl = URL.createObjectURL(file)
    if (sender === 'alice') {
      setAliceImage({ file, previewUrl })
    } else {
      setBobImage({ file, previewUrl })
    }
  }

  const handleFileInputChange = (e, sender) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      const previewUrl = URL.createObjectURL(file)
      if (sender === 'alice') {
        setAliceImage({ file, previewUrl })
      } else {
        setBobImage({ file, previewUrl })
      }
    }
  }

  // Eve attempts to decrypt an intercepted packet
  const handleEveAttemptDecrypt = async (msgId) => {
    const msg = messages.find(m => m.id === msgId)
    if (!msg) return

    addLog(`🚨 Eve attempting unauthorized decryption of packet #${msgId}...`)

    // If it's an image
    if (msg.type === 'image') {
      if (msg.algorithm === 'aes') {
        addLog(`❌ AES-GCM Authentication Failure: InvalidTag rejected Eve's forged/missing key.`)
        setMessages(prev => prev.map(m => m.id === msgId ? {
          ...m,
          eveDecryptAttempt: '❌ AUTHENTICATION FAILURE (InvalidTag): Eve does not possess the 256-bit AES secret key. Ciphertext authentication tag rejected decryption.'
        } : m))
      } else {
        addLog(`❌ Parameter Mismatch: Decryption without shared RNN weights / Lorenz seed produces pure pseudorandom pixel noise.`)
        setMessages(prev => prev.map(m => m.id === msgId ? {
          ...m,
          eveDecryptAttempt: `❌ MATHEMATICAL FAILURE: Eve used default/unauthorized parameters. Without synchronized internal recurrence state, decrypted matrix is unintelligible noise.`
        } : m))
      }
      return
    }

    // If it's text
    try {
      const res = await fetch(`${API_BASE}/api/attack-simulation`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ciphertext_hex: msg.ciphertextHex,
          algorithm: msg.algorithm,
          key_info: msg.keyInfo || { bit_length: 120, keystream: '0'.repeat(120), key_hex: '0'.repeat(64), nonce_hex: '0'.repeat(24) }
        })
      })

      const data = await res.json()
      addLog(`❌ Eve decryption failed: Unauthorized key / tag mismatch.`)

      setMessages(prev => prev.map(m => {
        if (m.id === msgId) {
          return {
            ...m,
            eveDecryptAttempt: data.eve_decrypt_result || '[Decryption rejected — key not available]'
          }
        }
        return m
      }))
    } catch (e) {
      addLog(`❌ Eve brute-force rejected: ${e.message}`)
    }
  }

  const handleSendMessage = async (sender) => {
    const text = sender === 'alice' ? aliceInput.trim() : bobInput.trim()
    const imageObj = sender === 'alice' ? aliceImage : bobImage
    if ((!text && !imageObj) || isTransmitting) return

    if (sender === 'alice') {
      setAliceInput('')
      setAliceImage(null)
    } else {
      setBobInput('')
      setBobImage(null)
    }

    setIsTransmitting(true)
    setActiveStep(1) // Step 1: Encrypting

    try {
      const now = new Date()
      const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

      // ================= CASE A: IMAGE MESSAGE =================
      if (imageObj) {
        addLog(`${sender === 'alice' ? 'Alice' : 'Bob'} uploading image: ${imageObj.file.name}`)
        addLog(`Encrypting image matrix with ${algorithm.toUpperCase()}...`)

        const formData = new FormData()
        formData.append('file', imageObj.file)
        formData.append('algorithm', algorithm)

        const encRes = await fetch(`${API_BASE}/api/encrypt-image`, {
          method: 'POST',
          body: formData
        })
        if (!encRes.ok) {
          const errData = await encRes.json().catch(() => ({}))
          throw new Error(errData.detail || 'Image encryption failed')
        }
        const encData = await encRes.json()

        setCurrentCiphertext(encData.cipher_image_b64.slice(0, 36) + '...')
        addLog(`Image encrypted in ${encData.encryption_time_ms} ms. Wire packet generated.`)

        // Step 2: On wire -> Eve sniffs
        await new Promise(r => setTimeout(r, 650))
        setActiveStep(2)
        addLog(`⚠️ Eve intercepted image payload on wire! (Scrambled matrix only, private key is protected)`)

        // Step 3: Decrypting at Receiver
        await new Promise(r => setTimeout(r, 700))
        setActiveStep(3)
        addLog(`Receiver verified secret key. Running ${algorithm.toUpperCase()} image decryption...`)

        const decRes = await fetch(`${API_BASE}/api/decrypt-image`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            cipher_image_b64: encData.cipher_image_b64,
            key_info: encData.key_info,
            algorithm
          })
        })
        if (!decRes.ok) {
          const errData = await decRes.json().catch(() => ({}))
          throw new Error(errData.detail || 'Image decryption failed')
        }
        const decData = await decRes.json()

        addLog(`Decryption successful in ${decData.decryption_time_ms} ms. Original image recovered.`)

        setMessages(prev => [
          ...prev,
          {
            id: Date.now(),
            sender,
            type: 'image',
            plaintext: text || '[Secret Image Attachment]',
            ciphertextHex: encData.cipher_image_b64.slice(0, 32) + '...',
            originalImageB64: encData.original_image_b64,
            cipherImageB64: encData.cipher_image_b64,
            decryptedImageB64: decData.decrypted_image_b64,
            algorithm,
            keyInfo: encData.key_info,
            eveDecryptAttempt: null,
            timestamp: timeStr,
            status: 'delivered'
          }
        ])

      // ================= CASE B: TEXT MESSAGE =================
      } else {
        addLog(`${sender === 'alice' ? 'Alice' : 'Bob'} composed: "${text}"`)
        addLog(`Encrypting plaintext with ${algorithm.toUpperCase()}...`)

        const encRes = await fetch(`${API_BASE}/api/encrypt-text`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text, algorithm, sender })
        })

        if (!encRes.ok) throw new Error('Encryption failed')
        const encData = await encRes.json()

        setCurrentCiphertext(encData.ciphertext_hex)
        addLog(`Ciphertext generated: ${encData.ciphertext_hex.slice(0, 24)}... (${encData.encryption_time_ms} ms)`)

        // Step 2: Packet on wire -> Eve intercepts
        await new Promise(r => setTimeout(r, 650))
        setActiveStep(2)
        addLog(`⚠️ Packet intercepted by Eve on public wire! (Ciphertext only, key is protected)`)

        // Step 3: Decrypting at Receiver
        await new Promise(r => setTimeout(r, 700))
        setActiveStep(3)
        addLog(`Receiver verified shared secret. Running ${algorithm.toUpperCase()} decryption...`)

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

        addLog(`Decryption successful in ${decData.decryption_time_ms} ms. Message delivered.`)

        setMessages(prev => [
          ...prev,
          {
            id: Date.now(),
            sender,
            type: 'text',
            plaintext: decData.plaintext,
            ciphertextHex: encData.ciphertext_hex,
            algorithm,
            keyInfo: encData.key_info,
            eveDecryptAttempt: null,
            timestamp: timeStr,
            status: 'delivered'
          }
        ])
      }

      await new Promise(r => setTimeout(r, 350))
    } catch (err) {
      console.error(err)
      addLog(`Error during transmission pipeline: ${err.message}`)
    } finally {
      setIsTransmitting(false)
      setActiveStep(0)
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-2rem)] space-y-4">
      {/* Top Header & Controls */}
      <div className="bg-gray-900/70 border border-gray-800 rounded-2xl p-4 backdrop-blur flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-xl font-bold text-white tracking-tight">CipherChat Secure Messenger</h1>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 font-mono border border-emerald-500/30">
              End-to-End Encrypted
            </span>
          </div>
          <p className="text-xs text-gray-400 mt-0.5">
            Demonstrating legitimate Alice-Bob communication vs. a third-party interceptor (Eve) who can only capture raw ciphertext.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          {/* Eavesdropper Toggle */}
          <button
            onClick={() => setShowEve(!showEve)}
            className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all border ${
              showEve
                ? 'bg-red-500/15 border-red-500/40 text-red-300 shadow-sm shadow-red-500/20'
                : 'bg-gray-900 border-gray-700 text-gray-400 hover:text-white'
            }`}
          >
            {showEve ? <Eye className="w-3.5 h-3.5 text-red-400" /> : <EyeOff className="w-3.5 h-3.5" />}
            <span>{showEve ? 'Third-Party Interceptor (Active)' : 'Show Interceptor (Eve)'}</span>
          </button>

          {/* Algorithm Selector */}
          <div className="flex items-center bg-gray-950 p-1 rounded-xl border border-gray-800">
            {[
              { id: 'jordan', label: 'Jordan RNN', icon: Brain, color: 'text-purple-400' },
              { id: 'chaotic', label: 'Chaotic Map', icon: Waves, color: 'text-pink-400' },
              { id: 'aes', label: 'AES-256-GCM', icon: ShieldCheck, color: 'text-emerald-400' },
            ].map((item) => {
              const Icon = item.icon
              const isSelected = algorithm === item.id
              return (
                <button
                  key={item.id}
                  onClick={() => setAlgorithm(item.id)}
                  className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                    isSelected
                      ? 'bg-gray-800 text-white shadow-sm border border-gray-700'
                      : 'text-gray-400 hover:text-gray-200'
                  }`}
                >
                  <Icon className={`w-3.5 h-3.5 ${item.color}`} />
                  <span>{item.label}</span>
                </button>
              )
            })}
          </div>
        </div>
      </div>

      {/* Main 3-Column Interface: Alice (Left), Eve Interceptor (Center), Bob (Right) */}
      <div className={`grid gap-4 flex-1 min-h-0 ${showEve ? 'grid-cols-1 lg:grid-cols-3' : 'grid-cols-1 lg:grid-cols-2'}`}>
        
        {/* ================= 1. ALICE (USER A) ================= */}
        <div className="bg-gray-900/60 border border-gray-800 rounded-2xl flex flex-col overflow-hidden">
          <div className="bg-gray-900 px-4 py-3 border-b border-gray-800 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-purple-500 to-indigo-600 flex items-center justify-center font-bold text-white shadow-md text-sm">
                A
              </div>
              <div>
                <h3 className="font-semibold text-white text-sm">Alice (Sender A)</h3>
                <p className="text-[11px] text-emerald-400 font-mono">● Online • Authenticated</p>
              </div>
            </div>
            <AlgorithmBadge algorithm={algorithm} size="xs" />
          </div>

          {/* Messages */}
          <div className="flex-1 p-4 overflow-y-auto space-y-3 bg-gray-950/40">
            {messages.map((m) => {
              const isMe = m.sender === 'alice'
              return (
                <div key={m.id} className={`flex flex-col ${isMe ? 'items-end' : 'items-start'}`}>
                  <div
                    className={`max-w-[85%] rounded-2xl p-3.5 shadow-sm text-sm ${
                      isMe
                        ? 'bg-emerald-600/90 text-white rounded-tr-none border border-emerald-500/30'
                        : 'bg-gray-800 text-gray-200 rounded-tl-none border border-gray-700/60'
                    }`}
                  >
                    {/* Render Image if available */}
                    {m.type === 'image' && (
                      <div className="mb-2">
                        <img 
                          src={`data:image/png;base64,${m.originalImageB64 || m.decryptedImageB64}`} 
                          alt="Encrypted attachment" 
                          className="w-36 h-36 object-cover rounded-xl border border-white/20 shadow-md"
                        />
                        <span className="text-[10px] text-emerald-200 block mt-1 font-mono">
                          🔒 Image Payload ({m.algorithm.toUpperCase()})
                        </span>
                      </div>
                    )}
                    
                    {m.plaintext && m.plaintext !== '[Secret Image Attachment]' && (
                      <p className="font-normal leading-relaxed">{m.plaintext}</p>
                    )}

                    <div className="mt-2 pt-1 border-t border-white/10 flex items-center justify-between space-x-2 text-[10px] opacity-75">
                      <span className="font-mono truncate max-w-[140px]">
                        Cipher: {m.ciphertextHex.slice(0, 10)}...
                      </span>
                      <div className="flex items-center space-x-1 font-mono">
                        <span>{m.timestamp}</span>
                        {isMe && <CheckCheck className="w-3.5 h-3.5 text-emerald-200" />}
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
            <div ref={chatEndRef} />
          </div>

          {/* Alice Attachment Preview */}
          {aliceImage && (
            <div className="px-3 py-2 bg-gray-950 border-t border-gray-800 flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <img src={aliceImage.previewUrl} alt="Preview" className="w-10 h-10 object-cover rounded-lg border border-emerald-500" />
                <span className="text-xs text-gray-300 font-mono truncate max-w-[160px]">{aliceImage.file.name}</span>
              </div>
              <button 
                onClick={() => setAliceImage(null)} 
                className="text-gray-400 hover:text-white p-1 rounded-lg"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* Alice Input Bar */}
          <div className="p-3 bg-gray-900/80 border-t border-gray-800">
            <form
              onSubmit={(e) => {
                e.preventDefault()
                handleSendMessage('alice')
              }}
              className="flex items-center space-x-2"
            >
              {/* Hidden file input */}
              <input 
                type="file" 
                ref={aliceFileRef} 
                onChange={(e) => handleFileInputChange(e, 'alice')} 
                accept="image/*" 
                className="hidden" 
              />
              
              <button
                type="button"
                onClick={() => aliceFileRef.current?.click()}
                title="Attach photo/image"
                className="p-2 text-gray-400 hover:text-emerald-400 bg-gray-950 hover:bg-gray-800 border border-gray-800 rounded-xl transition-all"
              >
                <Paperclip className="w-4 h-4" />
              </button>

              <button
                type="button"
                onClick={() => handleAttachSample('alice')}
                title="Attach high-contrast sample image"
                className="px-2 py-1.5 text-[11px] font-mono text-emerald-400 bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/30 rounded-xl transition-all flex items-center space-x-1"
              >
                <Sparkles className="w-3 h-3" />
                <span>Sample</span>
              </button>

              <input
                type="text"
                value={aliceInput}
                onChange={(e) => setAliceInput(e.target.value)}
                placeholder={aliceImage ? "Add image caption..." : "Type message as Alice..."}
                disabled={isTransmitting}
                className="flex-1 bg-gray-950 border border-gray-800 rounded-xl px-4 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-emerald-500 transition-colors"
              />
              <button
                type="submit"
                disabled={isTransmitting || (!aliceInput.trim() && !aliceImage)}
                className="bg-emerald-500 hover:bg-emerald-400 disabled:opacity-40 text-black font-semibold p-2.5 rounded-xl transition-all shadow-md shadow-emerald-500/20"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </div>

        {/* ================= 2. EVE: THE THIRD-PERSON INFILTRATOR (CENTER) ================= */}
        {showEve && (
          <div className="bg-gray-900/70 border border-red-500/40 rounded-2xl flex flex-col overflow-hidden shadow-xl shadow-red-950/20 relative">
            {/* Header */}
            <div className="bg-gradient-to-r from-red-950/80 to-gray-900 px-4 py-3 border-b border-red-500/30 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-9 h-9 rounded-full bg-red-600 flex items-center justify-center font-bold text-black shadow-md text-sm">
                  <Skull className="w-4 h-4 text-black" />
                </div>
                <div>
                  <div className="flex items-center space-x-1.5">
                    <h3 className="font-bold text-white text-sm">Eve (Third-Party Infiltrator)</h3>
                    <span className="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
                  </div>
                  <p className="text-[11px] text-red-400 font-mono">Sniffing Channel • No Shared Key</p>
                </div>
              </div>
              <span className="text-[10px] px-2 py-0.5 rounded bg-red-500/20 text-red-300 font-mono border border-red-500/30 uppercase">
                Wiretap
              </span>
            </div>

            {/* Explanation Banner */}
            <div className="px-3.5 py-2 bg-red-950/30 border-b border-red-500/20 text-[11px] text-red-300/90 leading-tight flex items-center space-x-2">
              <ShieldAlert className="w-4 h-4 shrink-0 text-red-400" />
              <span>
                <strong>Zero Knowledge:</strong> Eve captures all packets on the wire, but only gets <strong>ciphertext</strong>. Plaintext is inaccessible.
              </span>
            </div>

            {/* Intercepted Stream */}
            <div className="flex-1 p-3 overflow-y-auto space-y-3 bg-gray-950/80 font-mono text-xs">
              {messages.map((m) => (
                <div key={m.id} className="p-3 bg-gray-900/90 border border-red-500/25 rounded-xl space-y-2">
                  <div className="flex items-center justify-between text-[11px] text-gray-400 pb-1 border-b border-gray-800">
                    <span className="text-red-400 font-bold flex items-center space-x-1">
                      <Radio className="w-3 h-3 text-red-400" />
                      <span>PACKET #{m.id} ({m.sender.toUpperCase()} ➔ {m.sender === 'alice' ? 'BOB' : 'ALICE'})</span>
                    </span>
                    <span>{m.timestamp}</span>
                  </div>

                  {/* If Intercepted Packet is an IMAGE */}
                  {m.type === 'image' && m.cipherImageB64 && (
                    <div>
                      <span className="text-[10px] text-red-400 uppercase font-semibold block mb-1">
                        Captured Scrambled Image Matrix:
                      </span>
                      <div className="relative group rounded-lg overflow-hidden border border-red-500/30">
                        <img 
                          src={`data:image/png;base64,${m.cipherImageB64}`} 
                          alt="Scrambled Ciphertext Matrix" 
                          className="w-full h-32 object-cover bg-black filter contrast-125"
                        />
                        <div className="absolute inset-0 bg-red-950/40 backdrop-blur-[1px] flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                          <span className="text-[10px] bg-black/80 text-red-400 px-2 py-1 rounded border border-red-500/40">
                            Scrambled Ciphertext (Visual Noise)
                          </span>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Captured Ciphertext */}
                  <div>
                    <span className="text-[10px] text-gray-500 uppercase block">Captured Ciphertext:</span>
                    <div className="flex items-center justify-between bg-black/60 p-2 rounded-lg border border-gray-800 mt-0.5">
                      <span className="text-emerald-400 break-all text-[11px] select-all">
                        {m.ciphertextHex}
                      </span>
                      <button
                        onClick={() => handleCopyCipher(m.id, m.ciphertextHex)}
                        className="ml-2 text-gray-500 hover:text-white p-1 rounded"
                        title="Copy ciphertext"
                      >
                        {copiedId === m.id ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                      </button>
                    </div>
                  </div>

                  {/* Plaintext Status for Eve */}
                  <div className="p-2 bg-red-950/30 border border-red-500/30 rounded-lg flex items-center justify-between">
                    <div className="flex items-center space-x-1.5 text-[11px] text-red-300 font-semibold">
                      <Lock className="w-3.5 h-3.5 text-red-400 shrink-0" />
                      <span>PLAINTEXT: 🔒 ENCRYPTED (BLOCKED)</span>
                    </div>
                    <button
                      onClick={() => handleEveAttemptDecrypt(m.id)}
                      className="px-2 py-1 rounded bg-red-600 hover:bg-red-500 text-black font-bold text-[10px] transition-all flex items-center space-x-1"
                    >
                      <KeyRound className="w-3 h-3" />
                      <span>Attempt Crack</span>
                    </button>
                  </div>

                  {/* Unauthorized Decrypt Attempt Result */}
                  {m.eveDecryptAttempt && (
                    <div className="p-2 bg-black rounded-lg border border-red-500/40 text-[10px] text-red-400 break-all">
                      <span className="font-bold text-white uppercase block mb-0.5">Eve Decrypt Output:</span>
                      {m.eveDecryptAttempt}
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Eve Status Footer */}
            <div className="p-3 bg-gray-900/90 border-t border-red-500/20 flex items-center justify-between text-[11px] font-mono text-gray-400">
              <span className="flex items-center space-x-1.5 text-red-400">
                <XCircle className="w-3.5 h-3.5 text-red-400" />
                <span>Legitimate Key: Not In Memory</span>
              </span>
              <span className="text-gray-500">AES-GCM / RNN Protected</span>
            </div>
          </div>
        )}

        {/* ================= 3. BOB (USER B) ================= */}
        <div className="bg-gray-900/60 border border-gray-800 rounded-2xl flex flex-col overflow-hidden">
          <div className="bg-gray-900 px-4 py-3 border-b border-gray-800 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-emerald-500 to-teal-600 flex items-center justify-center font-bold text-black shadow-md text-sm">
                B
              </div>
              <div>
                <h3 className="font-semibold text-white text-sm">Bob (Receiver B)</h3>
                <p className="text-[11px] text-emerald-400 font-mono">● Online • Shared Key Possessed</p>
              </div>
            </div>
            <AlgorithmBadge algorithm={algorithm} size="xs" />
          </div>

          {/* Messages */}
          <div className="flex-1 p-4 overflow-y-auto space-y-3 bg-gray-950/40">
            {messages.map((m) => {
              const isMe = m.sender === 'bob'
              return (
                <div key={m.id} className={`flex flex-col ${isMe ? 'items-end' : 'items-start'}`}>
                  <div
                    className={`max-w-[85%] rounded-2xl p-3.5 shadow-sm text-sm ${
                      isMe
                        ? 'bg-emerald-600/90 text-white rounded-tr-none border border-emerald-500/30'
                        : 'bg-gray-800 text-gray-200 rounded-tl-none border border-gray-700/60'
                    }`}
                  >
                    {/* Render Image if available */}
                    {m.type === 'image' && (
                      <div className="mb-2">
                        <img 
                          src={`data:image/png;base64,${m.decryptedImageB64 || m.originalImageB64}`} 
                          alt="Decrypted attachment" 
                          className="w-36 h-36 object-cover rounded-xl border border-emerald-400/40 shadow-md"
                        />
                        <span className="text-[10px] text-emerald-300 block mt-1 font-mono">
                          ✓ Decrypted & Verified by Bob
                        </span>
                      </div>
                    )}

                    {m.plaintext && m.plaintext !== '[Secret Image Attachment]' && (
                      <p className="font-normal leading-relaxed">{m.plaintext}</p>
                    )}

                    <div className="mt-2 pt-1 border-t border-white/10 flex items-center justify-between space-x-2 text-[10px] opacity-75">
                      <span className="font-mono truncate max-w-[140px]">
                        Cipher: {m.ciphertextHex.slice(0, 10)}...
                      </span>
                      <div className="flex items-center space-x-1 font-mono">
                        <span>{m.timestamp}</span>
                        {isMe && <CheckCheck className="w-3.5 h-3.5 text-emerald-200" />}
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>

          {/* Bob Attachment Preview */}
          {bobImage && (
            <div className="px-3 py-2 bg-gray-950 border-t border-gray-800 flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <img src={bobImage.previewUrl} alt="Preview" className="w-10 h-10 object-cover rounded-lg border border-emerald-500" />
                <span className="text-xs text-gray-300 font-mono truncate max-w-[160px]">{bobImage.file.name}</span>
              </div>
              <button 
                onClick={() => setBobImage(null)} 
                className="text-gray-400 hover:text-white p-1 rounded-lg"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* Bob Input Bar */}
          <div className="p-3 bg-gray-900/80 border-t border-gray-800">
            <form
              onSubmit={(e) => {
                e.preventDefault()
                handleSendMessage('bob')
              }}
              className="flex items-center space-x-2"
            >
              {/* Hidden file input */}
              <input 
                type="file" 
                ref={bobFileRef} 
                onChange={(e) => handleFileInputChange(e, 'bob')} 
                accept="image/*" 
                className="hidden" 
              />
              
              <button
                type="button"
                onClick={() => bobFileRef.current?.click()}
                title="Attach photo/image"
                className="p-2 text-gray-400 hover:text-emerald-400 bg-gray-950 hover:bg-gray-800 border border-gray-800 rounded-xl transition-all"
              >
                <Paperclip className="w-4 h-4" />
              </button>

              <button
                type="button"
                onClick={() => handleAttachSample('bob')}
                title="Attach high-contrast sample image"
                className="px-2 py-1.5 text-[11px] font-mono text-emerald-400 bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/30 rounded-xl transition-all flex items-center space-x-1"
              >
                <Sparkles className="w-3 h-3" />
                <span>Sample</span>
              </button>

              <input
                type="text"
                value={bobInput}
                onChange={(e) => setBobInput(e.target.value)}
                placeholder={bobImage ? "Add image caption..." : "Reply as Bob..."}
                disabled={isTransmitting}
                className="flex-1 bg-gray-950 border border-gray-800 rounded-xl px-4 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-emerald-500 transition-colors"
              />
              <button
                type="submit"
                disabled={isTransmitting || (!bobInput.trim() && !bobImage)}
                className="bg-emerald-500 hover:bg-emerald-400 disabled:opacity-40 text-black font-semibold p-2.5 rounded-xl transition-all shadow-md shadow-emerald-500/20"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* ================= TRANSMISSION PIPELINE OVERLAY ================= */}
      <AnimatePresence>
        {isTransmitting && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="bg-gray-900/90 border border-emerald-500/40 rounded-2xl p-3 shadow-xl backdrop-blur flex items-center justify-between"
          >
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center animate-spin">
                <Lock className="w-4 h-4 text-emerald-400" />
              </div>
              <div>
                <p className="text-xs font-semibold text-white">
                  {activeStep === 1 && 'Step 1: Alice Encrypting Plaintext → Ciphertext'}
                  {activeStep === 2 && 'Step 2: Packet on Wire — Eve Intercepts Ciphertext (Key Protected)'}
                  {activeStep === 3 && 'Step 3: Bob Decrypting Payload with Shared Secret Key'}
                </p>
                <p className="text-[11px] font-mono text-emerald-400 truncate max-w-md">
                  Payload: {currentCiphertext ? currentCiphertext.slice(0, 36) + '...' : 'Computing...'}
                </p>
              </div>
            </div>

            {/* Step Indicators */}
            <div className="flex items-center space-x-2">
              {['Alice Encrypts', 'Eve Intercepts (Cipher)', 'Bob Decrypts'].map((name, i) => (
                <div key={name} className="flex items-center space-x-1">
                  <div
                    className={`w-2 h-2 rounded-full ${
                      activeStep > i ? 'bg-emerald-400 shadow-sm shadow-emerald-400' : 'bg-gray-700'
                    }`}
                  />
                  <span className={`text-[10px] font-mono ${activeStep > i ? 'text-gray-200' : 'text-gray-500'}`}>
                    {name}
                  </span>
                  {i < 2 && <ArrowRight className="w-3 h-3 text-gray-600" />}
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ================= LIVE ACTIVITY LOG ================= */}
      <div className="bg-gray-900/70 border border-gray-800 rounded-2xl p-3 max-h-32 flex flex-col">
        <div className="flex items-center justify-between pb-1 border-b border-gray-800 mb-2">
          <div className="flex items-center space-x-2 text-xs font-mono font-semibold text-gray-400 uppercase">
            <Terminal className="w-3.5 h-3.5 text-emerald-400" />
            <span>Cryptographic Wire Activity & Interception Log</span>
          </div>
          <span className="text-[10px] text-gray-500 font-mono">Real-time Timestamps</span>
        </div>
        <div className="overflow-y-auto space-y-1 font-mono text-[11px] flex-1">
          {activityLogs.map((log, i) => (
            <div key={i} className="flex items-start space-x-2 text-gray-400">
              <span className="text-emerald-500/80 font-bold shrink-0">{log.time}</span>
              <span className="text-gray-600">❯</span>
              <span className={log.text.includes('Eve') || log.text.includes('intercepted') ? 'text-red-400 font-semibold' : 'text-gray-300'}>
                {log.text}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
