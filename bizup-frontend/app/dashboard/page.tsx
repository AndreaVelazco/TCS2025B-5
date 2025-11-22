"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import Sidebar from "@/components/sidebar"
import { api } from "@/lib/api"

export default function DashboardPage() {
  const router = useRouter()
  const [userName, setUserName] = useState("")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [dashboard, setDashboard] = useState<any>(null)

  useEffect(() => {
    const userStr = localStorage.getItem("user")
    if (!userStr) {
      router.push("/login")
      return
    }

    const user = JSON.parse(userStr)
    setUserName(user.nombre || user.name || "Usuario")

    const fetchDashboard = async () => {
      setLoading(true)
      setError("")
      try {
        if (!api.isAuthenticated()) {
          router.push("/login")
          return
        }
        const data = await api.getDashboard()
        setDashboard(data)
      } catch (err) {
        console.error(err)
        const msg = err instanceof Error ? err.message : "Error al obtener datos"
        setError(msg)
      } finally {
        setLoading(false)
      }
    }

    fetchDashboard()
  }, [router])

  return (
    <div className="flex h-screen bg-cyan-50">
      <Sidebar />

      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-heading font-bold text-2xl text-slate-700">Bienvenido</h2>
              <p className="text-sm text-gray-600 mt-1">Resumen de tu situación financiera actual</p>
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
          {/* Financial Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {/* Ingresos */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-lg flex items-center justify-center">
                  <i className="fas fa-arrow-up text-white text-lg"></i>
                </div>
                <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">+12.5%</span>
              </div>
              <h3 className="font-heading font-semibold text-slate-700 mb-1">Ingresos del Mes</h3>
              <p className="font-heading font-black text-3xl text-green-600 mb-2">
                {loading ? "Cargando..." : dashboard ? formatCurrency(dashboard.total_ingresos) : "-"}
              </p>
              <p className="text-sm text-gray-600">vs. mes anterior: S/.2,180,000</p>
            </div>

            {/* Gastos */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-gradient-to-br from-red-500 to-red-600 rounded-lg flex items-center justify-center">
                  <i className="fas fa-arrow-down text-white text-lg"></i>
                </div>
                <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded-full">+8.2%</span>
              </div>
              <h3 className="font-heading font-semibold text-slate-700 mb-1">Gastos del Mes</h3>
              <p className="font-heading font-black text-3xl text-red-600 mb-2">
                {loading ? "Cargando..." : dashboard ? formatCurrency(dashboard.total_gastos) : "-"}
              </p>
              <p className="text-sm text-gray-600">vs. mes anterior: S/.1,750,000</p>
            </div>

            {/* Saldo Disponible */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-gradient-to-br from-cyan-900 to-cyan-600 rounded-lg flex items-center justify-center">
                  <i className="fas fa-piggy-bank text-white text-lg"></i>
                </div>
                <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">+25.8%</span>
              </div>
              <h3 className="font-heading font-semibold text-slate-700 mb-1">Saldo Disponible</h3>
              <p className="font-heading font-black text-3xl text-cyan-900">
                {loading ? "Cargando..." : dashboard ? formatCurrency(dashboard.balance) : "-"}
              </p>
              <p className="text-sm text-gray-600">Ahorro acumulado este mes</p>
            </div>
          </div>

          {/* Quick Actions & Recent Activity */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">

            {/* Actividad Reciente */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <h3 className="font-heading font-bold text-lg text-slate-700 mb-4">Actividad Reciente</h3>
              <div className="space-y-4">
                {loading && <p className="text-sm text-gray-600">Cargando actividad...</p>}
                {!loading && error && <p className="text-sm text-red-600">{error}</p>}
                {!loading && !error && dashboard && dashboard.registros_recientes.length === 0 && (
                  <div className="text-center py-8">
                    <i className="fas fa-inbox text-gray-300 text-4xl mb-2"></i>
                    <p className="text-gray-600">No hay movimientos recientes.</p>
                  </div>
                )}

                {!loading && !error && dashboard && dashboard.registros_recientes.slice(0, 5).map((r: any) => (
                  <div key={r.id_registro} className="flex items-center space-x-3">
                    <div className={`w-8 h-8 ${r.tipo === 'ingreso' ? 'bg-green-100' : 'bg-red-100'} rounded-full flex items-center justify-center`}>
                      <i className={`fas ${r.tipo === 'ingreso' ? 'fa-plus text-green-600' : 'fa-minus text-red-600'} text-xs`}></i>
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-sm">{r.descripcion || r.categoria}</p>
                      <p className="text-xs text-gray-600">{formatDate(r.fecha)}</p>
                    </div>
                    <span className={`font-bold ${r.tipo === 'ingreso' ? 'text-green-600' : 'text-red-600'}`}>
                      {r.tipo === 'ingreso' ? '+' : '-'}{formatCurrency(r.monto)}
                    </span>
                  </div>
                ))}
              </div>

              <button 
                onClick={() => router.push("/financial")}
                className="w-full mt-4 text-sm text-center py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Ver toda la actividad →
              </button>
            </div>

            {/* Alertas Financieras */}
            <div className="bg-white rounded-xl p-6 shadow-sm lg:col-span-1">
              <h3 className="font-heading font-bold text-lg text-slate-700 mb-4">Alertas y Recomendaciones</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="flex items-start space-x-3">
                    <i className="fas fa-exclamation-triangle text-red-600 text-lg mt-1"></i>
                    <div>
                      <h4 className="font-semibold text-red-900 mb-1">Gastos Excesivos Detectados</h4>
                      <p className="text-sm text-red-800">
                        Tus gastos están superando tu promedio mensual. Revisa tu presupuesto.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-start space-x-3">
                    <i className="fas fa-lightbulb text-blue-600 text-lg mt-1"></i>
                    <div>
                      <h4 className="font-semibold text-blue-900 mb-1">Recomendación</h4>
                      <p className="text-sm text-blue-800">
                        Tienes recursos de aprendizaje pendientes que pueden ayudarte.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
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