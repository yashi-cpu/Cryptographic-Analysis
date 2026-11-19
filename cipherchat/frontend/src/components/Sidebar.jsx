import React from 'react'
import { NavLink } from 'react-router-dom'
import { 
  MessageSquareLock, 
  FlaskConical, 
  Image as ImageIcon, 
  ShieldAlert, 
  BarChart3, 
  Info,
  ShieldCheck,
  Cpu
} from 'lucide-react'

export default function Sidebar() {
  const navItems = [
    { to: '/', label: 'Secure Chat', icon: MessageSquareLock, tag: 'WhatsApp Sim' },
    { to: '/encryption-lab', label: 'Encryption Lab', icon: FlaskConical, tag: 'Pipeline' },
    { to: '/image-crypto', label: 'Image Cryptography', icon: ImageIcon, tag: 'Visual' },
    { to: '/attacker', label: 'Attacker Simulation', icon: ShieldAlert, tag: 'Eve / MITM' },
    { to: '/analytics', label: 'Performance Analytics', icon: BarChart3, tag: 'Benchmarks' },
    { to: '/about', label: 'About Project', icon: Info, tag: 'MSc Viva' },
  ]

  return (
    <aside className="w-64 bg-gray-950/95 border-r border-gray-800/80 flex flex-col justify-between h-screen sticky top-0 backdrop-blur z-20">
      <div>
        {/* Brand Header */}
        <div className="p-5 border-b border-gray-800/80 flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-emerald-700 flex items-center justify-center shadow-lg shadow-emerald-500/20 border border-emerald-400/30">
            <ShieldCheck className="w-6 h-6 text-black" />
          </div>
          <div>
            <div className="flex items-center space-x-1.5">
              <span className="font-extrabold text-lg tracking-tight text-white">Cipher</span>
              <span className="font-extrabold text-lg tracking-tight text-emerald-400">Chat</span>
            </div>
            <p className="text-[10px] text-gray-400 font-mono tracking-wider uppercase">Neural & Chaotic Crypto</p>
          </div>
        </div>

        {/* Navigation links */}
        <nav className="p-3 space-y-1.5">
          <p className="px-3 py-2 text-[11px] font-semibold tracking-wider text-gray-500 uppercase font-mono">
            Navigation
          </p>
          {navItems.map((item) => {
            const Icon = item.icon
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all group ${
                    isActive
                      ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 shadow-sm shadow-emerald-500/10'
                      : 'text-gray-400 hover:text-gray-200 hover:bg-gray-900/60 border border-transparent'
                  }`
                }
              >
                <div className="flex items-center space-x-3">
                  <Icon className="w-4 h-4 transition-transform group-hover:scale-110" />
                  <span>{item.label}</span>
                </div>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-gray-800 text-gray-400 font-mono">
                  {item.tag}
                </span>
              </NavLink>
            )
          })}
        </nav>
      </div>

      {/* Footer Info */}
      <div className="p-4 border-t border-gray-800/80 bg-gray-900/40">
        <div className="flex items-center space-x-2 text-xs text-gray-400">
          <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
          <span className="font-mono">Backend: Connected</span>
        </div>
        <p className="text-[11px] text-gray-400 mt-1 font-mono">
          FastAPI • Port 8000
        </p>
      </div>
    </aside>
  )
}
