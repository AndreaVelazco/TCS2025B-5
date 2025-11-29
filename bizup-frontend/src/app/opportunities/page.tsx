"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import Sidebar from "@/components/sidebar"
import { api } from "@/lib/api"

interface Oportunidad {
  id_oportunidad: number
  nombre_programa: string
  tipo: string
  institucion: string
  enlace: string
  descripcion: string
  requisitos: string
  monto: number | null
  fecha_inicio: string | null
  fecha_fin: string | null
  activa: boolean
  fecha_publicacion: string
}

export default function OpportunitiesPage() {
  const router = useRouter()
  const [userName, setUserName] = useState("")
  const [oportunidades, setOportunidades] = useState<Oportunidad[]>([])
  const [filteredOportunidades, setFilteredOportunidades] = useState<Oportunidad[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [selectedTipo, setSelectedTipo] = useState<string>("all")
  const [searchQuery, setSearchQuery] = useState("")

  const tiposOportunidad = [
    { value: "all", label: "Todas", icon: "fas fa-layer-group" },
    { value: "beca", label: "Becas", icon: "fas fa-graduation-cap" },
    { value: "subvencion", label: "Subvenciones", icon: "fas fa-hand-holding-usd" },
    { value: "credito", label: "Créditos", icon: "fas fa-credit-card" },
    { value: "empleo", label: "Empleo", icon: "fas fa-briefcase" },
    { value: "capacitacion", label: "Capacitación", icon: "fas fa-chalkboard-teacher" },
    { value: "emprendimiento", label: "Emprendimiento", icon: "fas fa-rocket" },
  ]

  useEffect(() =>  {
    if (!api.isAuthenticated()) {
      router.push("/login")
      return
    }

    const loadData = async () =>  {
      try {
        const user = await api.getCurrentUser()
        setUserName(user.nombre)

        const data = await api.getOportunidades()
        setOportunidades(data)
        setFilteredOportunidades(data)
        setLoading(false)
      } catch (err) {
        console.error("[Opportunities] Error loading data:", err)
        setError("Error al cargar las oportunidades")
        setLoading(false)
      }
    }

    loadData()
  }, [router])

  useEffect(() =>  {
    let filtered = oportunidades

    if (selectedTipo !== "all") {
      filtered = filtered.filter((op) =>  op.tipo === selectedTipo)
    }

    if (searchQuery) {
      filtered = filtered.filter(
        (op) => 
          op.nombre_programa.toLowerCase().includes(searchQuery.toLowerCase()) ||
          op.institucion.toLowerCase().includes(searchQuery.toLowerCase()) ||
          op.descripcion.toLowerCase().includes(searchQuery.toLowerCase()),
      )
    }

    setFilteredOportunidades(filtered)
  }, [selectedTipo, searchQuery, oportunidades])

  const getTipoIcon = (tipo: string) =>  {
    const tipoObj = tiposOportunidad.find((t) =>  t.value === tipo)
    return tipoObj?.icon || "fas fa-circle"
  }

  const getTipoLabel = (tipo: string) =>  {
    const tipoObj = tiposOportunidad.find((t) =>  t.value === tipo)
    return tipoObj?.label || tipo
  }

  const formatMonto = (monto: number | null) =>  {
    if (!monto) return "No especificado"
    return new Intl.NumberFormat("es-PE", {
      style: "currency",
      currency: "PEN",
    }).format(monto)
  }

  const formatFecha = (fecha: string | null) =>  {
    if (!fecha) return "Sin fecha límite"
    return new Date(fecha).toLocaleDateString("es-PE", {
      year: "numeric",
      month: "long",
      day: "numeric",
    })
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-cyan-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-cyan-900 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600 font-semibold">Cargando oportunidades...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex h-screen bg-cyan-50">
      <Sidebar />

      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-heading font-bold text-2xl text-slate-700">Oportunidades Económicas</h2>
              <p className="text-sm text-gray-600 mt-1">
                Descubre {filteredOportunidades.length} programa(s) de apoyo y financiamiento
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3">
                <div className="text-right">
                  <p className="font-medium text-slate-700">{userName}</p>
                  <p className="text-sm text-gray-600">Usuario</p>
                </div>
                <div className="w-10 h-10 bg-amber-500 rounded-full flex items-center justify-center">
                  <i className="fas fa-user text-white"></i>
                </div>
              </div>
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                <p className="text-red-600">{error}</p>
              </div>
            )}

            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1">
                  <div className="relative">
                    <i className="fas fa-search absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                    <input
                      type="text"
                      placeholder="Buscar por nombre, institución..."
                      value={searchQuery}
                      onChange={ (e) => setSearchQuery(e.target.value)}
                      className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-900 focus:border-transparent"
                    /> 
                  </div>
                </div>

                <div className="md:w-64">
                  <select
                    value={selectedTipo}
                    onChange={ (e) => setSelectedTipo(e.target.value)} 
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-900 focus:border-transparent"
                  > 
                    {tiposOportunidad.map((tipo) =>  (
                      <option key={tipo.value} value={tipo.value}>
                        {tipo.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {filteredOportunidades.length === 0 ? (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
                <i className="fas fa-search text-gray-300 text-5xl mb-4"></i>
                <h3 className="font-heading font-bold text-xl text-slate-700 mb-2">No se encontraron oportunidades</h3>
                <p className="text-gray-600">Intenta ajustar los filtros de búsqueda</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {filteredOportunidades.map((oportunidad) =>  (           

                  <div
                    key={oportunidad.id_oportunidad}
                    className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
                  >
                    <div className="p-6">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-start space-x-3">
                          <div className="w-12 h-12 bg-cyan-100 rounded-lg flex items-center justify-center flex-shrink-0">
                            <i className={`${getTipoIcon(oportunidad.tipo)} text-cyan-900 text-xl`}></i>
                          </div>
                          <div>
                            <h3 className="font-heading font-bold text-lg text-slate-700">
                              {oportunidad.nombre_programa}
                            </h3>
                            <p className="text-sm text-gray-600">{oportunidad.institucion}</p>
                          </div>
                        </div>
                        <span className="px-3 py-1 bg-cyan-50 text-cyan-900 text-xs font-semibold rounded-full">
                          {getTipoLabel(oportunidad.tipo)}
                        </span>
                      </div>

                      <p className="text-gray-600 text-sm mb-4 line-clamp-3">{oportunidad.descripcion}</p>

                      <div className="grid grid-cols-2 gap-4 mb-4">
                        <div>
                          <p className="text-xs text-gray-500 mb-1">Monto</p>
                          <p className="font-semibold text-slate-700">{formatMonto(oportunidad.monto)}</p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-500 mb-1">Fecha límite</p>
                          <p className="font-semibold text-slate-700">{formatFecha(oportunidad.fecha_fin)}</p>
                        </div>
                      </div>

                      <div className="bg-gray-50 rounded-lg p-3 mb-4">
                        <p className="text-xs text-gray-500 mb-1">Requisitos principales</p>
                        <p className="text-sm text-gray-700 line-clamp-2">{oportunidad.requisitos}</p>
                      </div>

<div className="flex space-x-3">
  <a
    href={oportunidad.enlace}
    target="_blank"
    rel="noopener noreferrer"
    className="flex-1 py-2 px-4 bg-cyan-900 text-white rounded-lg font-semibold text-center hover:bg-cyan-700 transition-colors"
  >
    <i className="fas fa-external-link-alt mr-2"></i>
    Visitar Sitio
  </a>
  <button className="px-4 py-2 border-2 border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
    <i className="fas fa-bookmark text-gray-600"></i>
  </button>
</div>
                    </div>
                    </div>
                ))}
                </div>
            )}
            </div>
        </main>
        </div>
    </div>
    )
}



