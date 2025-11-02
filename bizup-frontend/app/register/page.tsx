"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { api } from "@/lib/api"

export default function RegisterPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    businessType: "",
    acceptTerms: false,
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError("Las contraseñas no coinciden")
      return
    }

    if (!formData.acceptTerms) {
      setError("Debes aceptar los términos y condiciones")
      return
    }

    if (formData.password.length < 8) {
      setError("La contraseña debe tener al menos 8 caracteres")
      return
    }

    setIsLoading(true)

    try {
      // Register user
      const userData = await api.register({
        nombre: formData.name,
        correo: formData.email,
        password: formData.password,
        perfil: formData.businessType,
      })

      // Login to get JWT tokens
      const tokens = await api.login({
        correo: formData.email,
        password: formData.password,
      })

      // Save tokens
      api.setTokens(tokens.access, tokens.refresh)

      // Save user data with isNewUser flag
      localStorage.setItem(
        "user",
        JSON.stringify({
          ...userData,
          isNewUser: true,
        }),
      )

      // Redirect to mini-test for new users
  alert("Cuenta creada exitosamente. Ahora puedes iniciar sesión.")
  router.push("/mini-test")

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Error al crear la cuenta. Intenta nuevamente."
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex bg-cyan-50">
      {/* Left Side - Register Form */}
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

          {/* Register Card */}
          <div className="bg-white rounded-2xl p-8 shadow-lg">
            <h2 className="font-heading font-bold text-2xl text-slate-700 mb-2">Crea tu cuenta</h2>
            <p className="text-gray-600 mb-6">Comienza tu viaje hacia el éxito financiero</p>

            {error && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-800 text-sm">{error}</div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Name Input */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Nombre Completo</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="fas fa-user text-gray-400"></i>
                  </div>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full pl-10 pr-4 py-3 rounded-lg border-2 border-gray-300 focus:border-cyan-900 focus:outline-none focus:ring-3 focus:ring-cyan-900/10 transition-all"
                    placeholder="Tu nombre"
                    required
                  />
                </div>
              </div>

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

              {/* Business Type Input */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Tipo de Negocio</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="fas fa-briefcase text-gray-400"></i>
                  </div>
                  <select
                    value={formData.businessType}
                    onChange={(e) => setFormData({ ...formData, businessType: e.target.value })}
                    className="w-full pl-10 pr-4 py-3 rounded-lg border-2 border-gray-300 focus:border-cyan-900 focus:outline-none focus:ring-3 focus:ring-cyan-900/10 transition-all appearance-none bg-white"
                    required
                  >
                    <option value="">Selecciona tu tipo de negocio</option>
                    <option value="comercio">Comercio</option>
                    <option value="servicios">Servicios</option>
                    <option value="manufactura">Manufactura</option>
                    <option value="tecnologia">Tecnología</option>
                    <option value="alimentos">Alimentos y Bebidas</option>
                    <option value="otro">Otro</option>
                  </select>
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
                    minLength={8}
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
                <p className="text-xs text-gray-500 mt-1">Mínimo 8 caracteres</p>
              </div>

              {/* Confirm Password Input */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Confirmar Contraseña</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="fas fa-lock text-gray-400"></i>
                  </div>
                  <input
                    type={showConfirmPassword ? "text" : "password"}
                    value={formData.confirmPassword}
                    onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                    className="w-full pl-10 pr-12 py-3 rounded-lg border-2 border-gray-300 focus:border-cyan-900 focus:outline-none focus:ring-3 focus:ring-cyan-900/10 transition-all"
                    placeholder="••••••••"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  >
                    <i
                      className={`fas ${showConfirmPassword ? "fa-eye-slash" : "fa-eye"} text-gray-400 hover:text-gray-600`}
                    ></i>
                  </button>
                </div>
              </div>

              {/* Terms and Conditions */}
              <div className="flex items-start">
                <input
                  type="checkbox"
                  checked={formData.acceptTerms}
                  onChange={(e) => setFormData({ ...formData, acceptTerms: e.target.checked })}
                  className="w-4 h-4 mt-1 text-cyan-900 border-gray-300 rounded focus:ring-cyan-900"
                />
                <label className="ml-2 text-sm text-gray-600">
                  Acepto los{" "}
                  <Link href="#" className="text-cyan-900 hover:underline font-semibold">
                    términos y condiciones
                  </Link>{" "}
                  y la{" "}
                  <Link href="#" className="text-cyan-900 hover:underline font-semibold">
                    política de privacidad
                  </Link>
                </label>
              </div>

              {/* Register Button */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-3 rounded-lg bg-cyan-900 text-white font-heading font-bold text-lg hover:bg-cyan-700 transition-all hover:-translate-y-0.5 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? "Creando cuenta..." : "Crear Cuenta"}
              </button>
            </form>

            {/* Login Link */}
            <p className="text-center text-sm text-gray-600 mt-6">
              ¿Ya tienes una cuenta?{" "}
              <Link href="/login" className="font-semibold text-cyan-900 hover:underline">
                Inicia sesión
              </Link>
            </p>
          </div>
        </div>
      </div>

      {/* Right Side - Same as login */}
      <div className="hidden lg:flex flex-1 bg-gradient-to-br from-cyan-900 to-cyan-600 p-12 items-center justify-center">
        <div className="max-w-lg text-white">
          <h2 className="font-heading font-black text-4xl mb-4">Únete a cientos de emprendedores exitosos</h2>
          <p className="text-cyan-100 text-lg mb-12">
            Comienza a gestionar tus finanzas de manera profesional y accede a recursos educativos personalizados.
          </p>

          {/* Benefits */}
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <i className="fas fa-check-circle text-amber-400 text-xl"></i>
              <span className="text-cyan-50">Registro gratuito y sin compromisos</span>
            </div>
            <div className="flex items-center space-x-3">
              <i className="fas fa-check-circle text-amber-400 text-xl"></i>
              <span className="text-cyan-50">Recomendaciones personalizadas</span>
            </div>
            <div className="flex items-center space-x-3">
              <i className="fas fa-check-circle text-amber-400 text-xl"></i>
              <span className="text-cyan-50">Acceso a recursos educativos gratuitos</span>
            </div>
            <div className="flex items-center space-x-3">
              <i className="fas fa-check-circle text-amber-400 text-xl"></i>
              <span className="text-cyan-50">Alertas financieras inteligentes</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}


