"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import Sidebar from "@/components/sidebar"
import { api, type Recomendacion } from "@/lib/api"

export default function RecommendationsPage() {
  const router = useRouter()
  const [userName, setUserName] = useState("")
  const [recommendations, setRecommendations] = useState<Recomendacion[]>([])
  const [profileSummary, setProfileSummary] = useState("")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    const loadRecommendations = async () => {
      try {
        if (!api.isAuthenticated()) {
          router.push("/login")
          return
        }

        const user = await api.getCurrentUser()
        setUserName(user.nombre)

        const recs = await api.getMyRecommendations()
        setRecommendations(recs)

        const summary = `Basado en tu perfil como emprendedor de nivel ${user.perfil}, hemos seleccionado estos recursos para ayudarte a mejorar tus habilidades financieras.`
        setProfileSummary(summary)

        setLoading(false)
      } catch (err) {
        console.error("[v0] Error loading recommendations:", err)
        setError("Error al cargar las recomendaciones")
        setLoading(false)
      }
    }

    loadRecommendations()
  }, [router])

  const handleViewResource = async (rec: Recomendacion) => {
    try {
      if (!rec.visto) {
        await api.markRecommendationAsSeen(rec.id_recomendacion)
        setRecommendations((prev) =>
          prev.map((r) => (r.id_recomendacion === rec.id_recomendacion ? { ...r, visto: true } : r)),
        )
      }
      window.open(rec.recurso.enlace, "_blank")
    } catch (err) {
      console.error("[v0] Error marking as seen:", err)
    }
  }

  const handleRateRecommendation = async (rec: Recomendacion, util: boolean) => {
    try {
      await api.rateRecommendation(rec.id_recomendacion, util)
      setRecommendations((prev) =>
        prev.map((r) => (r.id_recomendacion === rec.id_recomendacion ? { ...r, util } : r)),
      )
    } catch (err) {
      console.error("[v0] Error rating recommendation:", err)
    }
  }

  const getTypeLabel = (type: string) => {
    switch (type) {
      case "video":
        return "Video"
      case "articulo":
        return "Artículo"
      case "curso":
        return "Curso"
      case "podcast":
        return "Podcast"
      case "infografia":
        return "Infografía"
      default:
        return type
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case "video":
        return "fa-video"
      case "articulo":
        return "fa-file-alt"
      case "curso":
        return "fa-graduation-cap"
      case "podcast":
        return "fa-podcast"
      case "infografia":
        return "fa-chart-bar"
      default:
        return "fa-file"
    }
  }

  const getColorClasses = (type: string) => {
    switch (type) {
      case "video":
        return "text-blue-500"
      case "articulo":
        return "text-red-500"
      case "curso":
        return "text-green-500"
      case "podcast":
        return "text-purple-500"
      case "infografia":
        return "text-orange-500"
      default:
        return "text-gray-500"
    }
  }

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-cyan-50">
        <i className="fas fa-spinner fa-spin text-4xl text-cyan-900"></i>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex h-screen items-center justify-center bg-cyan-50">
        <div className="text-center">
          <i className="fas fa-exclamation-circle text-4xl text-red-500 mb-4"></i>
          <p className="text-gray-600 mb-4">{error}</p>
          <Link href="/dashboard" className="text-cyan-900 hover:underline">
            Volver al Dashboard
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="flex h-screen bg-cyan-50">
      <Sidebar />

      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-heading font-bold text-2xl text-slate-700">Recursos Recomendados</h2>
              <p className="text-sm text-gray-600 mt-1">{profileSummary}</p>
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

        {/* Main content */}
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-4xl mx-auto space-y-4">
            {recommendations.length === 0 ? (
              <div className="bg-white rounded-xl shadow-sm p-8 text-center">
                <i className="fas fa-inbox text-4xl text-gray-300 mb-4"></i>
                <p className="text-gray-600">No hay recomendaciones disponibles en este momento.</p>
                <p className="text-sm text-gray-500 mt-2">
                  Completa el mini-test para recibir recomendaciones personalizadas.
                </p>
              </div>
            ) : (
              recommendations.map((rec) => (
                <div
                  key={rec.id_recomendacion}
                  className="bg-white rounded-xl shadow-sm p-5 hover:shadow-md transition-all hover:-translate-y-0.5"
                >
                  <div className="flex items-start gap-4">
                    <i
                      className={`fas ${getTypeIcon(rec.recurso.tipo)} ${getColorClasses(
                        rec.recurso.tipo,
                      )} text-2xl mt-1`}
                    ></i>
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="text-lg font-semibold text-slate-700">{rec.recurso.titulo}</h4>
                        {rec.visto && (
                          <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">Visto</span>
                        )}
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{rec.recurso.descripcion}</p>
                      <p className="text-xs text-gray-500 mb-3">
                        Tipo: {getTypeLabel(rec.recurso.tipo)} • Temática: {rec.recurso.tematica} • Nivel:{" "}
                        {rec.recurso.nivel}
                      </p>
                      <div className="flex items-center gap-3">
                        <button
                          onClick={() => handleViewResource(rec)}
                          className="text-cyan-900 hover:underline text-sm font-semibold inline-flex items-center"
                        >
                          Ver recurso
                          <i className="fas fa-arrow-right ml-2 text-xs"></i>
                        </button>
                        {rec.visto && rec.util === null && (
                          <div className="flex items-center gap-2 ml-auto">
                            <span className="text-xs text-gray-600">¿Te fue útil?</span>
                            <button
                              onClick={() => handleRateRecommendation(rec, true)}
                              className="text-green-600 hover:text-green-700 text-sm"
                              title="Útil"
                            >
                              <i className="fas fa-thumbs-up"></i>
                            </button>
                            <button
                              onClick={() => handleRateRecommendation(rec, false)}
                              className="text-red-600 hover:text-red-700 text-sm"
                              title="No útil"
                            >
                              <i className="fas fa-thumbs-down"></i>
                            </button>
                          </div>
                        )}
                        {rec.util !== null && (
                          <span className="text-xs text-gray-500 ml-auto">
                            {rec.util ? "✓ Marcado como útil" : "✗ Marcado como no útil"}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))
            )}

            {/* Tip box */}
            <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-start gap-3">
              <i className="fas fa-info-circle text-blue-600 text-lg mt-0.5"></i>
              <div>
                <h5 className="font-semibold text-blue-900 mb-1">Tip: Actualiza tus recomendaciones</h5>
                <p className="text-sm text-blue-800">
                  A medida que uses la plataforma y registres tus finanzas, iremos ajustando las recomendaciones para
                  que sean aún más relevantes para ti.
                </p>
              </div>
            </div>

            
          </div>
        </main>
      </div>
    </div>
  )
}
