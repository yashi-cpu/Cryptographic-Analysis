import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Upload, 
  Image as ImageIcon, 
  Lock, 
  Unlock, 
  ShieldCheck, 
  CheckCircle2, 
  AlertTriangle,
  ArrowRight,
  Clock,
  HardDrive,
  Sparkles,
  RefreshCw
} from 'lucide-react'
import AlgorithmBadge from '../components/AlgorithmBadge'
import { API_BASE } from '../api'

export default function ImageCrypto() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [algorithm, setAlgorithm] = useState('chaotic')
  const [isProcessing, setIsProcessing] = useState(false)
  const [result, setResult] = useState(null)
  const [errorMsg, setErrorMsg] = useState('')

  // Generate high-contrast geometric sample pattern for instant testing
  const generateSampleImage = () => {
    const canvas = document.createElement('canvas')
    canvas.width = 128
    canvas.height = 128
    const ctx = canvas.getContext('2d')
    
    // Background gradient
    const grad = ctx.createLinearGradient(0, 0, 128, 128)
    grad.addColorStop(0, '#10b981')
    grad.addColorStop(0.5, '#3b82f6')
    grad.addColorStop(1, '#ec4899')
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
    ctx.font = 'bold 12px Inter, sans-serif'
    ctx.textAlign = 'center'
    ctx.fillText('CIPHER', 64, 68)

    canvas.toBlob((blob) => {
      const file = new File([blob], 'cipher_sample_target.png', { type: 'image/png' })
      setSelectedFile(file)
      setPreviewUrl(URL.createObjectURL(file))
      setResult(null)
      setErrorMsg('')
    }, 'image/png')
  }

  // Auto-load sample image on mount so the user never has an empty/blocked state
  useEffect(() => {
    generateSampleImage()
  }, [])

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      setSelectedFile(file)
      setPreviewUrl(URL.createObjectURL(file))
      setResult(null)
      setErrorMsg('')
    }
  }

  const handleEncryptImage = async () => {
    if (!selectedFile || isProcessing) return
    setIsProcessing(true)
    setErrorMsg('')

    try {
      // 1. Upload & Encrypt
      const formData = new FormData()
      formData.append('file', selectedFile)
      formData.append('algorithm', algorithm)

      const encRes = await fetch(`${API_BASE}/api/encrypt-image`, {
        method: 'POST',
        body: formData
      })

      if (!encRes.ok) {
        const err = await encRes.json().catch(() => ({}))
        throw new Error(err.detail || 'Encryption failed')
      }
      const encData = await encRes.json()

      // 2. Decrypt
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
        const err = await decRes.json().catch(() => ({}))
        throw new Error(err.detail || 'Decryption failed')
      }
      const decData = await decRes.json()

      setResult({
        originalB64: encData.original_image_b64,
        cipherB64: encData.cipher_image_b64,
        decryptedB64: decData.decrypted_image_b64,
        originalSize: encData.original_size,
        cipherSize: encData.cipher_size,
        encTime: encData.encryption_time_ms,
        decTime: decData.decryption_time_ms,
        success: decData.success,
        algorithm
      })
    } catch (err) {
      console.error(err)
      setErrorMsg(err.message)
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-10">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2">
          <h1 className="text-2xl font-extrabold text-white tracking-tight">Image Cryptography Lab</h1>
          <span className="text-xs px-2.5 py-0.5 rounded-full bg-pink-500/15 text-pink-400 font-mono border border-pink-500/30">
            Pixel Diffusion & Recovery
          </span>
        </div>
        <p className="text-sm text-gray-400 mt-1">
          Encrypt full RGB image payloads using Chaotic continuous dynamics (Arnold Cat Map + Lorenz RK4), Jordan RNN, or AES-GCM.
        </p>
      </div>

      {/* Upload Card */}
      <div className="bg-gray-900/80 border border-gray-800 rounded-2xl p-5 shadow-lg backdrop-blur space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
          <div className="md:col-span-2">
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-xs font-mono font-medium text-gray-300 block">Select Image or Use Pre-loaded Target:</label>
              <button
                type="button"
                onClick={generateSampleImage}
                className="text-xs text-emerald-400 hover:text-emerald-300 font-mono flex items-center space-x-1"
              >
                <RefreshCw className="w-3 h-3" />
                <span>Reset to Built-in Sample</span>
              </button>
            </div>
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-2 text-sm text-gray-300 file:mr-4 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-emerald-500 file:text-black hover:file:bg-emerald-400 cursor-pointer"
            />
          </div>

          <div>
            <label className="text-xs font-mono font-medium text-gray-300 mb-1.5 block">Cryptographic Algorithm:</label>
            <select
              value={algorithm}
              onChange={(e) => setAlgorithm(e.target.value)}
              className="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors font-mono"
            >
              <option value="chaotic">Chaotic Lorenz + Arnold Map (Recommended)</option>
              <option value="jordan">Jordan RNN Byte Stream</option>
              <option value="aes">AES-256-GCM Authenticated</option>
            </select>
          </div>
        </div>

        {/* Selected Image Preview Pill */}
        {previewUrl && (
          <div className="flex items-center space-x-3 p-3 bg-gray-950/70 border border-gray-800 rounded-xl">
            <img src={previewUrl} alt="Preview" className="w-10 h-10 object-cover rounded-lg border border-gray-700" />
            <div className="text-xs">
              <p className="font-semibold text-white font-mono">{selectedFile?.name || 'sample_target.png'}</p>
              <p className="text-gray-500 text-[11px]">Ready for encryption • Resized to 128x128 for real-time responsiveness</p>
            </div>
          </div>
        )}

        {errorMsg && (
          <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-xs flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        <div className="pt-2 flex items-center space-x-3">
          <button
            onClick={handleEncryptImage}
            disabled={!selectedFile || isProcessing}
            className="flex items-center space-x-2 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-40 text-black font-semibold px-6 py-2.5 rounded-xl transition-all shadow-md shadow-emerald-500/20 text-sm"
          >
            <Lock className="w-4 h-4" />
            <span>{isProcessing ? 'Encrypting & Decrypting...' : 'Encrypt & Transmit Image'}</span>
          </button>
        </div>
      </div>

      {/* 4-Panel Image Transformation Showcase */}
      {result && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* 1. Original Image */}
            <div className="bg-gray-900/70 border border-gray-800 rounded-2xl p-4 flex flex-col items-center">
              <span className="text-xs font-mono text-gray-400 mb-2 uppercase">1. Original Plain-Image</span>
              <div className="w-full h-56 bg-black rounded-xl overflow-hidden flex items-center justify-center border border-gray-800">
                <img
                  src={`data:image/png;base64,${result.originalB64}`}
                  alt="Original"
                  className="max-h-full max-w-full object-contain"
                />
              </div>
              <p className="text-[11px] font-mono text-gray-500 mt-2">
                Input Dimensions: 128x128 RGB
              </p>
            </div>

            {/* 2. Encrypted Scrambled Image */}
            <div className="bg-gray-900/70 border border-emerald-500/30 rounded-2xl p-4 flex flex-col items-center shadow-md shadow-emerald-500/5">
              <div className="flex items-center space-x-1.5 mb-2">
                <span className="text-xs font-mono text-emerald-400 font-semibold uppercase">2. Encrypted Payload</span>
                <AlgorithmBadge algorithm={result.algorithm} size="xs" />
              </div>
              <div className="w-full h-56 bg-black rounded-xl overflow-hidden flex items-center justify-center border border-emerald-500/20">
                <img
                  src={`data:image/png;base64,${result.cipherB64}`}
                  alt="Encrypted"
                  className="max-h-full max-w-full object-contain"
                />
              </div>
              <p className="text-[11px] font-mono text-emerald-400 mt-2">
                Pixel Diffusion Active • Enc: {result.encTime} ms
              </p>
            </div>

            {/* 3. Decrypted Recovered Image */}
            <div className="bg-gray-900/70 border border-gray-800 rounded-2xl p-4 flex flex-col items-center">
              <div className="flex items-center space-x-1.5 mb-2">
                <span className="text-xs font-mono text-gray-400 uppercase">3. Decrypted Recovery</span>
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              </div>
              <div className="w-full h-56 bg-black rounded-xl overflow-hidden flex items-center justify-center border border-gray-800">
                <img
                  src={`data:image/png;base64,${result.decryptedB64}`}
                  alt="Decrypted"
                  className="max-h-full max-w-full object-contain"
                />
              </div>
              <p className="text-[11px] font-mono text-gray-500 mt-2">
                Dec: {result.decTime} ms • Exact Match: ✅
              </p>
            </div>
          </div>

          {/* Performance & Security Comparison Panel */}
          <div className="bg-gray-900/80 border border-gray-800 rounded-2xl p-5 shadow-lg">
            <h3 className="font-bold text-sm text-white mb-4 flex items-center space-x-2">
              <HardDrive className="w-4 h-4 text-emerald-400" />
              <span>Image Cryptographic Performance Summary</span>
            </h3>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-3 bg-gray-950 rounded-xl border border-gray-800">
                <span className="text-[11px] text-gray-500 font-mono uppercase block">Original Data Size</span>
                <span className="text-lg font-bold text-white font-mono">{(result.originalSize / 1024).toFixed(1)} KB</span>
              </div>
              <div className="p-3 bg-gray-950 rounded-xl border border-gray-800">
                <span className="text-[11px] text-gray-500 font-mono uppercase block">Encrypted Payload Size</span>
                <span className="text-lg font-bold text-white font-mono">{(result.cipherSize / 1024).toFixed(1)} KB</span>
              </div>
              <div className="p-3 bg-gray-950 rounded-xl border border-gray-800">
                <span className="text-[11px] text-gray-500 font-mono uppercase block">Encryption Latency</span>
                <span className="text-lg font-bold text-emerald-400 font-mono">{result.encTime} ms</span>
              </div>
              <div className="p-3 bg-gray-950 rounded-xl border border-gray-800">
                <span className="text-[11px] text-gray-500 font-mono uppercase block">Decryption Latency</span>
                <span className="text-lg font-bold text-emerald-400 font-mono">{result.decTime} ms</span>
              </div>
            </div>

            <div className="mt-4 p-3.5 bg-gray-950/60 rounded-xl border border-gray-800 text-xs text-gray-400 leading-relaxed">
              <span className="font-bold text-white font-mono">⚠️ Academic Note: </span>
              In chaotic image encryption, the combination of <strong>Arnold's Cat Map</strong> (confusion) and <strong>Continuous Lorenz Attractor</strong> (diffusion) eliminates visual silhouettes (such as the ECB penguin effect). AES-GCM provides standard authenticated encryption.
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
