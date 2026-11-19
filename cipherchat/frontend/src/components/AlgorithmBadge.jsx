import React from 'react'
import { Brain, Waves, ShieldCheck } from 'lucide-react'

export default function AlgorithmBadge({ algorithm, size = 'sm' }) {
  const algo = (algorithm || '').toLowerCase()

  if (algo === 'jordan') {
    return (
      <span className={`inline-flex items-center space-x-1 font-mono font-medium rounded-full bg-purple-500/15 text-purple-300 border border-purple-500/30 ${size === 'xs' ? 'px-1.5 py-0.5 text-[10px]' : 'px-2.5 py-1 text-xs'}`}>
        <Brain className="w-3 h-3 text-purple-400" />
        <span>Jordan RNN</span>
      </span>
    )
  }

  if (algo === 'chaotic') {
    return (
      <span className={`inline-flex items-center space-x-1 font-mono font-medium rounded-full bg-pink-500/15 text-pink-300 border border-pink-500/30 ${size === 'xs' ? 'px-1.5 py-0.5 text-[10px]' : 'px-2.5 py-1 text-xs'}`}>
        <Waves className="w-3 h-3 text-pink-400" />
        <span>Chaotic Map</span>
      </span>
    )
  }

  return (
    <span className={`inline-flex items-center space-x-1 font-mono font-medium rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 ${size === 'xs' ? 'px-1.5 py-0.5 text-[10px]' : 'px-2.5 py-1 text-xs'}`}>
      <ShieldCheck className="w-3 h-3 text-emerald-400" />
      <span>AES-256-GCM</span>
    </span>
  )
}
