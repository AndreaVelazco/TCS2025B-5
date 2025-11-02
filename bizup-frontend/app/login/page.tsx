"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { api } from "@/lib/api"

export default function LoginPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    rememberMe: false,
  })
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError("")

    try {
      // Login to get JWT tokens
      const tokens = await api.login({
        correo: formData.email,
        password: formData.password,
      })

      // Save tokens
      api.setTokens(tokens.access, tokens.refresh)

      // Get user data
      const userData = await api.getCurrentUser()

      // Save user data (existing users have isNewUser: false)
      localStorage.setItem(
        "user",
        JSON.stringify({
          ...userData,
          isNewUser: false,
        }),
      )

      // Redirect to dashboard
      router.push("/dashboard")
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Credenciales inválidas. Intenta nuevamente."
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex bg-cyan-50">
      {/* Left Side - Login Form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          {/* Logo */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-cyan-900 rounded-2xl mb-4">
              <i className="fas fa-chart-line text-white text-2xl"></i>
            </div>
            <h1 className="font-heading font-black text-4xl text-slate-700 mb-2">BizUp</h1>
            <p className="text-gray-600">Tu aliado financiero</p>
          </div>

          {/* Login Card */}
          <div className="bg-white rounded-2xl p-8 shadow-lg">
            <h2 className="font-heading font-bold text-2xl text-slate-700 mb-2">Bienvenido emprendedor</h2>
            <p className="text-gray-600 mb-6">Ingresa tus credenciales para continuar</p>

            {error && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-800 text-sm">{error}</div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Email Input */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Correo Electrónico</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="fas fa-envelope text-gray-400"></i>
                  </div>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="w-full pl-10 pr-4 py-3 rounded-lg border-2 border-gray-300 focus:border-cyan-900 focus:outline-none focus:ring-3 focus:ring-cyan-900/10 transition-all"
                    placeholder="tu@email.com"
                    required
                  />
                </div>
              </div>

              {/* Password Input */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Contraseña</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="fas fa-lock text-gray-400"></i>
                  </div>
                  <input
                    type={showPassword ? "text" : "password"}
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    className="w-full pl-10 pr-12 py-3 rounded-lg border-2 border-gray-300 focus:border-cyan-900 focus:outline-none focus:ring-3 focus:ring-cyan-900/10 transition-all"
                    placeholder="••••••••"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  >
                    <i
                      className={`fas ${showPassword ? "fa-eye-slash" : "fa-eye"} text-gray-400 hover:text-gray-600`}
                    ></i>
                  </button>
                </div>
              </div>

              {/* Remember Me & Forgot Password */}
              <div className="flex items-center justify-between">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.rememberMe}
                    onChange={(e) => setFormData({ ...formData, rememberMe: e.target.checked })}
                    className="w-4 h-4 text-cyan-900 border-gray-300 rounded focus:ring-cyan-900"
                  />
                  <span className="ml-2 text-sm text-gray-600">Recordarme</span>
                </label>
                <Link href="#" className="text-sm font-semibold text-cyan-900 hover:underline">
                  ¿Olvidaste tu contraseña?
                </Link>
              </div>

              {/* Login Button */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-3 rounded-lg bg-cyan-900 text-white font-heading font-bold text-lg hover:bg-cyan-700 transition-all hover:-translate-y-0.5 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? "Iniciando sesión..." : "Iniciar Sesión"}
              </button>
            </form>

            {/* Sign Up Link */}
            <p className="text-center text-sm text-gray-600 mt-6">
              ¿No tienes una cuenta?{" "}
              <Link href="/register" className="font-semibold text-cyan-900 hover:underline">
                Regístrate gratis
              </Link>
            </p>
          </div>
        </div>
      </div>

      {/* Right Side - Features/Benefits */}
      <div className="hidden lg:flex flex-1 bg-gradient-to-br from-cyan-900 to-cyan-600 p-12 items-center justify-center">
        <div className="max-w-lg text-white">
          <h2 className="font-heading font-black text-4xl mb-4">Gestiona tu negocio de forma inteligente</h2>
          <p className="text-cyan-100 text-lg mb-12">
            Herramientas financieras diseñadas para emprendedores que buscan crecer y prosperar.
          </p>

          {/* Features List */}
          <div className="space-y-6">
            <div className="flex items-start space-x-4">
              <div className="w-15 h-15 bg-gradient-to-br from-amber-500 to-orange-500 rounded-xl flex items-center justify-center flex-shrink-0 p-4">
                <i className="fas fa-chart-bar text-white text-2xl"></i>
              </div>
              <div>
                <h3 className="font-heading font-bold text-xl mb-1">Control Financiero</h3>
                <p className="text-cyan-100">Monitorea tus ingresos y gastos en tiempo real</p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="w-15 h-15 bg-gradient-to-br from-amber-500 to-orange-500 rounded-xl flex items-center justify-center flex-shrink-0 p-4">
                <i className="fas fa-graduation-cap text-white text-2xl"></i>
              </div>
              <div>
                <h3 className="font-heading font-bold text-xl mb-1">Aprende y Crece</h3>
                <p className="text-cyan-100">Accede a cursos y recursos para mejorar tus habilidades</p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="w-15 h-15 bg-gradient-to-br from-amber-500 to-orange-500 rounded-xl flex items-center justify-center flex-shrink-0 p-4">
                <i className="fas fa-lightbulb text-white text-2xl"></i>
              </div>
              <div>
                <h3 className="font-heading font-bold text-xl mb-1">Oportunidades</h3>
                <p className="text-cyan-100">Descubre nuevas formas de hacer crecer tu negocio</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

