"use client"

import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"

export default function Sidebar() {
  const pathname = usePathname()
  const router = useRouter()

  const handleLogout = () => {
    localStorage.removeItem("user")
    localStorage.removeItem("testResults")
    router.push("/login")
  }

  const navItems = [
    { href: "/dashboard", icon: "fa-home", label: "Dashboard" },
    { href: "/financial", icon: "fa-wallet", label: "Gestión Financiera" },
    { href: "/learning", icon: "fa-graduation-cap", label: "Aprendizaje" },
    { href: "/opportunities", icon: "fa-handshake", label: "Oportunidades" },
  ]

  const secondaryItems = [
    { href: "/settings", icon: "fa-cog", label: "Configuración" },
    { href: "/help", icon: "fa-question-circle", label: "Ayuda" },
  ]

  return (
    <div className="w-64 bg-white border-r border-gray-200 flex flex-col h-screen">
      {/* Logo/Header */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-cyan-900 rounded-lg flex items-center justify-center">
            <i className="fas fa-chart-line text-white text-lg"></i>
          </div>
          <div>
            <h1 className="font-heading font-bold text-lg text-slate-700">BizUp</h1>
            <p className="text-xs text-gray-500">Tu aliado financiero</p>
          </div>
        </div>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
              pathname === item.href
                ? "bg-cyan-900 text-white"
                : "text-slate-600 hover:bg-yellow-50 hover:text-cyan-900"
            }`}
          >
            <i className={`fas ${item.icon} w-5`}></i>
            <span className="font-medium">{item.label}</span>
          </Link>
        ))}

        <div className="pt-4 border-t border-gray-200 mt-4">
          {secondaryItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                pathname === item.href
                  ? "bg-cyan-900 text-white"
                  : "text-slate-600 hover:bg-yellow-50 hover:text-cyan-900"
              }`}
            >
              <i className={`fas ${item.icon} w-5`}></i>
              <span className="font-medium">{item.label}</span>
            </Link>
          ))}
        </div>
      </nav>

      {/* User Profile */}
      <div className="p-4 border-t border-gray-200">
        <button
          onClick={handleLogout}
          className="w-full flex items-center justify-center space-x-2 px-4 py-2 text-sm text-gray-600 hover:text-red-600 transition-colors"
        >
          <i className="fas fa-sign-out-alt"></i>
          <span>Cerrar Sesión</span>
        </button>
      </div>
    </div>
  )
}
