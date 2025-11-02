"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { api } from "@/lib/api"

interface Question {
  id_pregunta: number
  categoria: string
  pregunta: string
  opciones: string[]
  nivel_dificultad: string
}

export default function MiniTestPage() {
  const router = useRouter()
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<Record<number, number>>({})
  const [isComplete, setIsComplete] = useState(false)
  const [userName, setUserName] = useState("")
  const [questions, setQuestions] = useState<Question[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!api.isAuthenticated()) {
      router.push("/minitest")
      return
    }

    const loadData = async () => {
      try {
        const user = await api.getCurrentUser()
        setUserName(user.nombre)

        // Check if user has already taken the test
        const lastTest = await api.getLastTestResult()
        if (lastTest) {
          // User has already taken the test, redirect to dashboard
          router.push("/dashboard")
          return
        }

        // Fetch test questions
        const fetchedQuestions = await api.getTestQuestions(5)
        setQuestions(fetchedQuestions)
        setLoading(false)
      } catch (err) {
        console.error("[v0] Error loading test data:", err)
        setError("Error al cargar el test. Por favor, intenta de nuevo.")
        setLoading(false)
      }
    }

    loadData()
  }, [router])

  const handleAnswer = (optionIndex: number) => {
    const newAnswers = { ...answers, [questions[currentQuestion].id_pregunta]: optionIndex }
    setAnswers(newAnswers)

    // Move to next question or complete
    if (currentQuestion < questions.length - 1) {
      setTimeout(() => {
        setCurrentQuestion(currentQuestion + 1)
      }, 300)
    } else {
      setIsComplete(true)
    }
  }

  const handleComplete = async () => {
    try {
      // Convert answers to backend format
      const answersArray = Object.entries(answers).map(([pregunta_id, respuesta]) => ({
        pregunta_id: Number.parseInt(pregunta_id),
        respuesta,
      }))

      // Submit to backend
      const result = await api.submitTestAnswers(answersArray)

      // Save result to localStorage for recommendations page
      localStorage.setItem("testResult", JSON.stringify(result))

      // Redirect to recommendations
      router.push("/recommendations")
    } catch (err) {
      console.error("[v0] Error submitting test:", err)
      setError("Error al enviar el test. Por favor, intenta de nuevo.")
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-cyan-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-cyan-900 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600 font-semibold">Cargando test...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-cyan-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-lg p-8 text-center">
          <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <i className="fas fa-exclamation-triangle text-red-600 text-3xl"></i>
          </div>
          <h2 className="font-heading font-bold text-2xl text-slate-700 mb-3">Error</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => router.push("/dashboard")}
            className="w-full py-3 rounded-lg bg-cyan-900 text-white font-heading font-bold text-lg hover:bg-cyan-700 transition-all"
          >
            Volver al Dashboard
          </button>
        </div>
      </div>
    )
  }

  if (questions.length === 0) {
    return (
      <div className="min-h-screen bg-cyan-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-lg p-8 text-center">
          <p className="text-gray-600">No hay preguntas disponibles.</p>
        </div>
      </div>
    )
  }

  const progress = ((currentQuestion + 1) / questions.length) * 100

  if (isComplete) {
    return (
      <div className="min-h-screen bg-cyan-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-lg p-8 text-center">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <i className="fas fa-check text-green-600 text-3xl"></i>
          </div>
          <h2 className="font-heading font-bold text-2xl text-slate-700 mb-3">¡Test Completado!</h2>
          <p className="text-gray-600 mb-6">
            Gracias por completar el test, {userName}. Ahora vamos a mostrarte recursos personalizados según tus
            respuestas.
          </p>
          <button
            onClick={handleComplete}
            className="w-full py-3 rounded-lg bg-cyan-900 text-white font-heading font-bold text-lg hover:bg-cyan-700 transition-all hover:-translate-y-0.5 hover:shadow-lg"
          >
            Ver Mis Recomendaciones
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-cyan-50 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-cyan-900 rounded-2xl mb-4">
            <i className="fas fa-clipboard-list text-white text-2xl"></i>
          </div>
          <h1 className="font-heading font-black text-3xl text-slate-700 mb-2">Test de Evaluación Inicial</h1>
          <p className="text-gray-600">Ayúdanos a conocerte mejor para personalizar tu experiencia</p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-semibold text-slate-700">
              Pregunta {currentQuestion + 1} de {questions.length}
            </span>
            <span className="text-sm font-semibold text-cyan-900">{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div
              className="bg-gradient-to-r from-cyan-900 to-cyan-600 h-full rounded-full transition-all duration-500 ease-out"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>

        {/* Question Card */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-6">
          <h2 className="font-heading font-bold text-xl text-slate-700 mb-6">{questions[currentQuestion].pregunta}</h2>

          <div className="space-y-3">
            {questions[currentQuestion].opciones.map((option, index) => (
              <button
                key={index}
                onClick={() => handleAnswer(index)}
                className={`w-full text-left p-4 rounded-lg border-2 transition-all hover:border-cyan-900 hover:bg-cyan-50 ${
                  answers[questions[currentQuestion].id_pregunta] === index
                    ? "border-cyan-900 bg-cyan-50"
                    : "border-gray-200 bg-white"
                }`}
              >
                <div className="flex items-center space-x-3">
                  <div
                    className={`w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0 ${
                      answers[questions[currentQuestion].id_pregunta] === index
                        ? "border-cyan-900 bg-cyan-900"
                        : "border-gray-300"
                    }`}
                  >
                    {answers[questions[currentQuestion].id_pregunta] === index && (
                      <i className="fas fa-check text-white text-xs"></i>
                    )}
                  </div>
                  <span className="font-medium text-slate-700">{option}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Navigation */}
        <div className="flex justify-between items-center">
          <button
            onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
            disabled={currentQuestion === 0}
            className="px-6 py-2 rounded-lg border-2 border-gray-300 text-gray-700 font-semibold hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <i className="fas fa-arrow-left mr-2"></i>
            Anterior
          </button>

          <div className="flex space-x-2">
            {questions.map((_, index) => (
              <div
                key={index}
                className={`w-2 h-2 rounded-full transition-all ${
                  index === currentQuestion
                    ? "bg-cyan-900 w-8"
                    : index < currentQuestion
                      ? "bg-cyan-600"
                      : "bg-gray-300"
                }`}
              ></div>
            ))}
          </div>

          <button
            onClick={() => {
              if (answers[questions[currentQuestion].id_pregunta] !== undefined) {
                if (currentQuestion < questions.length - 1) {
                  setCurrentQuestion(currentQuestion + 1)
                } else {
                  setIsComplete(true)
                }
              }
            }}
            disabled={answers[questions[currentQuestion].id_pregunta] === undefined}
            className="px-6 py-2 rounded-lg bg-cyan-900 text-white font-semibold hover:bg-cyan-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {currentQuestion === questions.length - 1 ? "Finalizar" : "Siguiente"}
            <i className="fas fa-arrow-right ml-2"></i>
          </button>
        </div>
      </div>
    </div>
  )
}
