"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import Sidebar from "@/components/sidebar"
export default function LearningPage() {
  const router = useRouter()
  const [userName, setUserName] = useState("")

  useEffect(() => {
    const userStr = localStorage.getItem("user")
    if (!userStr) {
      router.push("/login")
      return
    }

    const user = JSON.parse(userStr)
    setUserName(user.name)
  }, [router])

  return (
    <div className="flex h-screen bg-cyan-50">
      <Sidebar />

      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-heading font-bold text-2xl text-slate-700">Módulo de Aprendizaje</h2>
              <p className="text-sm text-gray-600 mt-1">Recursos para tu crecimiento financiero</p>
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
          <div className="max-w-4xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-1 gap-6">
              {/* Recursos Recomendados */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
                <h3 className="text-lg font-semibold text-slate-700 mb-4 flex items-center">
                  <i className="fas fa-book-open text-cyan-900 mr-2"></i> Recursos Recomendados
                </h3>
                <ul className="space-y-3 text-gray-600 text-sm">
                  <li className="flex items-center">
                    <i className="fas fa-file-pdf text-red-500 mr-2"></i> Guías (PDF)
                  </li>
                  <li className="flex items-center">
                    <i className="fas fa-video text-amber-500 mr-2"></i> Videos
                  </li>
                  <li className="flex items-center">
                    <i className="fas fa-book text-green-500 mr-2"></i> Cursos
                  </li>
                </ul>
                <Link
                  href="/recommendations"
                  className="mt-4 w-full block text-center bg-cyan-900 text-white py-2 px-4 rounded-md hover:bg-cyan-700 transition-colors"
                >
                  Ver recursos
                </Link>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
