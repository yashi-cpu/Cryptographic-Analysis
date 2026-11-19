import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import SecureChat from './pages/SecureChat'
import EncryptionLab from './pages/EncryptionLab'
import ImageCrypto from './pages/ImageCrypto'
import AttackerSim from './pages/AttackerSim'
import Analytics from './pages/Analytics'
import About from './pages/About'

export default function App() {
  return (
    <div className="flex min-h-screen bg-gray-950 text-gray-100 font-sans">
      {/* Fixed Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <main className="flex-1 p-6 overflow-y-auto">
        <Routes>
          <Route path="/" element={<SecureChat />} />
          <Route path="/encryption-lab" element={<EncryptionLab />} />
          <Route path="/image-crypto" element={<ImageCrypto />} />
          <Route path="/attacker" element={<AttackerSim />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>
    </div>
  )
}
