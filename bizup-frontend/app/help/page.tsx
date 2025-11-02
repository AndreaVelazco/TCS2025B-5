"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import Sidebar from "@/components/sidebar"

export default function HelpPage() {
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
              <h2 className="font-heading font-bold text-2xl text-slate-700">Ayuda</h2>
              <p className="text-sm text-gray-600 mt-1">Encuentra respuestas a tus preguntas</p>
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
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
              <i className="fas fa-question-circle text-cyan-900 text-5xl mb-4"></i>
              <h3 className="font-heading font-bold text-xl text-slate-700 mb-2">Centro de Ayuda</h3>
              <p className="text-gray-600">
                Esta funcionalidad estará disponible próximamente. Aquí encontrarás guías y soporte.
              </p>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
