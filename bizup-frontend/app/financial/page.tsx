"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import Sidebar from "@/components/sidebar"
import { api } from "@/lib/api"

export default function FinancialPage() {
  const router = useRouter()
  const [userName, setUserName] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [submitting, setSubmitting] = useState(false)
  const [movimientos, setMovimientos] = useState<any[]>([])
  const [formData, setFormData] = useState({
    tipo: "ingreso",
    monto: "",
    categoria: "salario",
    descripcion: "",
  })

  useEffect(() => {
    const userStr = localStorage.getItem("user")
    if (!userStr) {
      router.push("/login")
      return
    }

    const user = JSON.parse(userStr)
    setUserName(user.nombre || user.name || "Usuario")

    // Cargar movimientos recientes
    fetchMovimientos()
  }, [router])

  const fetchMovimientos = async () => {
    setLoading(true)
    try {
      if (!api.isAuthenticated()) {
        router.push("/login")
        return
      }
      const data = await api.getDashboard()
      setMovimientos(data.registros_recientes || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleFormChange = (e: any) => {
    const { name, value } = e.target
    
    // Si cambia el tipo, resetear la categoría a la primera opción de ese tipo
    if (name === "tipo") {
      setFormData({
        ...formData,
        tipo: value,
        categoria: value === "ingreso" ? "salario" : "alimentacion"
      })
    } else {
      setFormData((prev) => ({
        ...prev,
        [name]: value,
      }))
    }
  }

  const handleSubmitMovimiento = async (e: any) => {
    e.preventDefault()
    setSubmitting(true)
    setError("")

    try {
      const monto = parseFloat(formData.monto)
      
      if (!formData.monto || isNaN(monto) || monto <= 0) {
        setError("Por favor ingresa un monto válido mayor a 0")
        setSubmitting(false)
        return
      }

      if (!formData.categoria) {
        setError("Por favor selecciona una categoría")
        setSubmitting(false)
        return
      }

      const fechaActual = new Date().toISOString()
      
      console.log("Enviando movimiento:", {
        tipo: formData.tipo,
        monto: monto,
        categoria: formData.categoria,
        descripcion: formData.descripcion,
        fecha: fechaActual
      })

      await api.createMovimiento(
        formData.tipo as "ingreso" | "gasto",
        monto,
        formData.categoria,
        formData.descripcion,
        fechaActual
      )

      // Recargar movimientos
      await fetchMovimientos()

      // Reset form - mantener el tipo seleccionado
      const tipoActual = formData.tipo
      setFormData({
        tipo: tipoActual,
        monto: "",
        categoria: tipoActual === "ingreso" ? "salario" : "alimentacion",
        descripcion: "",
      })

      // Mostrar mensaje de éxito
      setError("")
      alert("✅ Movimiento registrado exitosamente")
    } catch (err) {
      console.error("Error al crear movimiento:", err)
      const msg = err instanceof Error ? err.message : "Error al crear movimiento"
      setError(msg)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="flex h-screen bg-cyan-50">
      <Sidebar />

      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-heading font-bold text-2xl text-slate-700">Gestión Financiera</h2>
              <p className="text-sm text-gray-600 mt-1">Administra tus ingresos y gastos</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3">
                <div className="text-right">
                  <p className="font-medium text-slate-700">{userName}</p>
                  <p className="text-sm text-gray-600">Emprendedor</p>
                </div>
                <div className="w-10 h-10 bg-amber-500 rounded-full flex items-center justify-center">
                  <i className="fas fa-user text-white"></i>
                </div>
              </div>
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-6xl mx-auto">
            {/* Formulario de Registro */}
            <div className="bg-white rounded-xl p-6 shadow-sm mb-6">
              <h3 className="font-heading font-bold text-lg text-slate-700 mb-4">
                Registrar Nuevo Movimiento
              </h3>

              <div className="space-y-4">
                {error && (
                  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                    {error}
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Tipo */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Tipo de Movimiento
                    </label>
                    <select
                      name="tipo"
                      value={formData.tipo}
                      onChange={handleFormChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
                    >
                      <option value="ingreso">Ingreso</option>
                      <option value="gasto">Gasto</option>
                    </select>
                  </div>

                  {/* Monto */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Monto (S/.)
                    </label>
                    <input
                      type="number"
                      name="monto"
                      value={formData.monto}
                      onChange={handleFormChange}
                      placeholder="0.00"
                      step="0.01"
                      min="0"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
                      required
                    />
                  </div>

                  {/* Categoría */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Categoría
                    </label>
                    <select
                      name="categoria"
                      value={formData.categoria}
                      onChange={handleFormChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
                      required
                    >
                      {formData.tipo === "ingreso" ? (
                        <>
                          <option value="salario">Salario</option>
                          <option value="freelance">Freelance</option>
                          <option value="negocio">Negocio Propio</option>
                          <option value="inversion">Inversión</option>
                          <option value="otro_ingreso">Otro Ingreso</option>
                        </>
                      ) : (
                        <>
                          <option value="alimentacion">Alimentación</option>
                          <option value="transporte">Transporte</option>
                          <option value="vivienda">Vivienda</option>
                          <option value="servicios">Servicios</option>
                          <option value="educacion">Educación</option>
                          <option value="salud">Salud</option>
                          <option value="entretenimiento">Entretenimiento</option>
                          <option value="ropa">Ropa</option>
                          <option value="deudas">Pago de Deudas</option>
                          <option value="ahorro">Ahorro</option>
                          <option value="otro_gasto">Otro Gasto</option>
                        </>
                      )}
                    </select>
                  </div>

                  {/* Descripción */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Descripción (opcional)
                    </label>
                    <input
                      type="text"
                      name="descripcion"
                      value={formData.descripcion}
                      onChange={handleFormChange}
                      placeholder="Ej: Salario mensual, Almuerzo, etc"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
                    />
                  </div>
                </div>

                {/* Botón de envío */}
                <div className="flex justify-end pt-2">
                  <button
                    onClick={handleSubmitMovimiento}
                    disabled={submitting}
                    className="bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-400 text-white font-medium py-3 px-8 rounded-lg transition-colors flex items-center gap-2"
                  >
                    {submitting ? (
                      <>
                        <i className="fas fa-spinner fa-spin"></i>
                        Guardando...
                      </>
                    ) : (
                      <>
                        <i className="fas fa-save"></i>
                        Guardar Movimiento
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>

            {/* Lista de Movimientos Recientes */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-heading font-bold text-lg text-slate-700">
                  Movimientos Recientes
                </h3>
                <button
                  onClick={fetchMovimientos}
                  className="text-sm text-cyan-600 hover:text-cyan-700 flex items-center gap-2"
                >
                  <i className="fas fa-sync-alt"></i>
                  Actualizar
                </button>
              </div>

              {loading ? (
                <div className="text-center py-8">
                  <i className="fas fa-spinner fa-spin text-cyan-600 text-2xl mb-2"></i>
                  <p className="text-sm text-gray-600">Cargando movimientos...</p>
                </div>
              ) : movimientos.length === 0 ? (
                <div className="text-center py-8">
                  <i className="fas fa-inbox text-gray-300 text-4xl mb-3"></i>
                  <p className="text-gray-600">No hay movimientos registrados</p>
                  <p className="text-sm text-gray-500 mt-1">
                    Comienza registrando tu primer ingreso o gasto
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {movimientos.map((mov: any) => (
                    <div
                      key={mov.id_registro}
                      className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <div className="flex items-center gap-4">
                        <div
                          className={`w-12 h-12 ${
                            mov.tipo === "ingreso" ? "bg-green-100" : "bg-red-100"
                          } rounded-lg flex items-center justify-center`}
                        >
                          <i
                            className={`fas ${
                              mov.tipo === "ingreso"
                                ? "fa-arrow-up text-green-600"
                                : "fa-arrow-down text-red-600"
                            } text-lg`}
                          ></i>
                        </div>
                        <div>
                          <p className="font-medium text-slate-700">
                            {getCategoriaLabel(mov.categoria)} {mov.descripcion && `- ${mov.descripcion}`}
                          </p>
                          <p className="text-sm text-gray-600">
                            {formatDate(mov.fecha)}
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <span
                          className={`font-bold text-lg ${
                            mov.tipo === "ingreso" ? "text-green-600" : "text-red-600"
                          }`}
                        >
                          {mov.tipo === "ingreso" ? "+" : "-"}
                          {formatCurrency(mov.monto)}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

function formatCurrency(value: number | string) {
  const num = typeof value === "string" ? parseFloat(String(value)) : (value as number) || 0
  try {
    return new Intl.NumberFormat("es-PE", { style: "currency", currency: "PEN" }).format(Number(num))
  } catch (e) {
    return `S/. ${Number(num).toFixed(2)}`
  }
}

function formatDate(dateStr: string) {
  if (!dateStr) return ""
  const d = new Date(dateStr)
  if (isNaN(d.getTime())) return dateStr
  return d.toLocaleString("es-PE", { dateStyle: "medium", timeStyle: "short" })
}

function getCategoriaLabel(categoria: string): string {
  const labels: Record<string, string> = {
    // Ingresos
    "salario": "Salario",
    "freelance": "Freelance",
    "negocio": "Negocio Propio",
    "inversion": "Inversión",
    "otro_ingreso": "Otro Ingreso",
    // Gastos
    "alimentacion": "Alimentación",
    "transporte": "Transporte",
    "vivienda": "Vivienda",
    "servicios": "Servicios",
    "educacion": "Educación",
    "salud": "Salud",
    "entretenimiento": "Entretenimiento",
    "ropa": "Ropa",
    "deudas": "Pago de Deudas",
    "ahorro": "Ahorro",
    "otro_gasto": "Otro Gasto",
  }
  return labels[categoria] || categoria
}