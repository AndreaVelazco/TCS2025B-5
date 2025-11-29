// API service for Django backend integration
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api"

interface RegisterData {
  nombre: string
  correo: string
  password: string
  perfil: string
}

interface LoginData {
  correo: string
  password: string
}

interface TokenResponse {
  access: string
  refresh: string
}

interface UserData {
  id_usuario: number
  nombre: string
  correo: string
  perfil: string
  fecha_registro: string
}

interface TestQuestion {
  id_pregunta: number
  categoria: string
  pregunta: string
  opciones: string[]
  nivel_dificultad: string
}

interface TestAnswer {
  pregunta_id: number
  respuesta: number
}

interface TestResult {
  id_test: number
  id_usuario: number
  resultado: Record<string, number>
  puntuacion_total: number
  nivel_determinado: string
  fecha: string
}

interface RecursoAprendizaje {
  id_recurso: number
  tipo: "video" | "articulo" | "curso" | "podcast" | "infografia"
  titulo: string
  enlace: string
  tematica: string
  descripcion: string
  nivel: "principiante" | "intermedio" | "avanzado"
  fecha_creacion: string
}

interface Recomendacion {
  id_recomendacion: number
  id_usuario: number
  id_recurso: number
  recurso: RecursoAprendizaje
  criterio: string
  fecha_recomendacion: string
  visto: boolean
  util: boolean | null
}

interface DashboardCategory {
  categoria: string
  total: number
}

interface DashboardData {
  total_ingresos: number
  total_gastos: number
  balance: number
  resumen_por_categoria: DashboardCategory[]
  registros_recientes: Array<{
    id_registro: number
    tipo: string
    monto: string | number
    fecha: string
    categoria: string
    descripcion?: string
  }>
  metas_activas: Array<{
    id_meta: number
    nombre: string
    monto_objetivo: string | number
    monto_actual: string | number
    estado: string
  }>
}

class ApiService {
  // Authentication
  async register(data: RegisterData): Promise<UserData> {
    console.log("[v0] Registering user:", { ...data, password: "***" })
    console.log("[v0] API URL:", `${API_URL}/usuarios/`)

    const response = await fetch(`${API_URL}/usuarios/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })

    return this.handleResponse<UserData>(response)
  }

  async login(data: LoginData): Promise<TokenResponse> {
    console.log("[v0] Logging in user:", { ...data, password: "***" })
    console.log("[v0] API URL:", `${API_URL}/token/`)

    const response = await fetch(`${API_URL}/token/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })

    return this.handleResponse<TokenResponse>(response)
  }

  async getCurrentUser(): Promise<UserData> {
    const token = this.getAccessToken()
    if (!token) {
      throw new Error("No hay token de autenticación")
    }

    const response = await fetch(`${API_URL}/usuarios/me/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    return this.handleResponse<UserData>(response)
  }

  async refreshToken(): Promise<TokenResponse> {
    const refreshToken = this.getRefreshToken()
    if (!refreshToken) {
      throw new Error("No hay refresh token")
    }

    const response = await fetch(`${API_URL}/token/refresh/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh: refreshToken }),
    })

    return this.handleResponse<TokenResponse>(response)
  }

  // Token management
  setTokens(access: string, refresh: string) {
    localStorage.setItem("access_token", access)
    localStorage.setItem("refresh_token", refresh)
  }

  getAccessToken(): string | null {
    return localStorage.getItem("access_token")
  }

  getRefreshToken(): string | null {
    return localStorage.getItem("refresh_token")
  }

  clearTokens() {
    localStorage.removeItem("access_token")
    localStorage.removeItem("refresh_token")
    localStorage.removeItem("user")
  }

  isAuthenticated(): boolean {
    return !!this.getAccessToken()
  }

  // Mini-test
  async getTestQuestions(cantidad = 5): Promise<TestQuestion[]> {
    const token = this.getAccessToken()
    const response = await fetch(`${API_URL}/evaluaciones/tests/obtener_preguntas/?cantidad=${cantidad}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    return this.handleResponse<TestQuestion[]>(response)
  }

async submitTestAnswers(answers: TestAnswer[]): Promise<TestResult> {
  const token = this.getAccessToken()
  
  // Convertir el formato de TestAnswer[] a lo que espera el backend
  const formattedAnswers = answers.map(answer => ({
    pregunta_id: answer.pregunta_id,
    respuesta: answer.respuesta
  }))
  
  console.log("[API] Enviando respuestas del test:", formattedAnswers)
  
  const response = await fetch(`${API_URL}/evaluaciones/tests/enviar_respuestas/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ respuestas: formattedAnswers }),
  })

  return this.handleResponse<TestResult>(response)
}

  async getLastTestResult(): Promise<TestResult | null> {
    const token = this.getAccessToken()
    const response = await fetch(`${API_URL}/evaluaciones/tests/ultimo_resultado/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.status === 404) {
      return null
    }

    return this.handleResponse<TestResult>(response)
  }

  // Recommendations
  async getMyRecommendations(): Promise<Recomendacion[]> {
    const token = this.getAccessToken()
    const response = await fetch(`${API_URL}/aprendizaje/recomendaciones/mis_recomendaciones/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    return this.handleResponse<Recomendacion[]>(response)
  }

  async markRecommendationAsSeen(id: number): Promise<void> {
    const token = this.getAccessToken()
    const response = await fetch(`${API_URL}/aprendizaje/recomendaciones/${id}/marcar_visto/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    await this.handleResponse<void>(response)
  }

  async rateRecommendation(id: number, util: boolean): Promise<void> {
    const token = this.getAccessToken()
    const response = await fetch(`${API_URL}/aprendizaje/recomendaciones/${id}/calificar/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ util }),
    })

    await this.handleResponse<void>(response)
  }

  async getResourcesByTopic(tematica: string): Promise<RecursoAprendizaje[]> {
    const token = this.getAccessToken()
    const response = await fetch(`${API_URL}/aprendizaje/recursos/por_tematica/?tematica=${tematica}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    return this.handleResponse<RecursoAprendizaje[]>(response)
  }

  async getResourcesByLevel(nivel?: string): Promise<RecursoAprendizaje[]> {
    const token = this.getAccessToken()
    const url = nivel
      ? `${API_URL}/aprendizaje/recursos/por_nivel/?nivel=${nivel}`
      : `${API_URL}/aprendizaje/recursos/por_nivel/`

    const response = await fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    return this.handleResponse<RecursoAprendizaje[]>(response)
  }
  // Agregar ANTES del último cierre de la clase ApiService (antes de la última llave })

// Opportunities
async getOportunidades(): Promise<any[]> {
  const token = this.getAccessToken()
  const response = await fetch(`${API_URL}/oportunidades/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  const data = await this.handleResponse<any>(response)
  
  // El backend devuelve un objeto con paginación: { count, results }
  // Extraemos solo el array de results
  if (data && data.results && Array.isArray(data.results)) {
    return data.results
  }
  
  // Si por alguna razón devuelve directamente el array
  if (Array.isArray(data)) {
    return data
  }
  
  console.error("[API] Formato inesperado de oportunidades:", data)
  return []
}

async getOportunidadesPorTipo(tipo: string): Promise<any[]> {
  const token = this.getAccessToken()
  const response = await fetch(`${API_URL}/oportunidades/?tipo=${tipo}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  const data = await this.handleResponse<any>(response)
  
  // Extraer results si existe
  if (data && data.results && Array.isArray(data.results)) {
    return data.results
  }
  
  if (Array.isArray(data)) {
    return data
  }
  
  return []
}

async getOportunidadesVigentes(): Promise<any[]> {
  const token = this.getAccessToken()
  const response = await fetch(`${API_URL}/oportunidades/vigentes/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  const data = await this.handleResponse<any>(response)
  
  // El endpoint /vigentes/ devuelve directamente el array
  if (Array.isArray(data)) {
    return data
  }
  
  if (data && data.results && Array.isArray(data.results)) {
    return data.results
  }
  
  return []
}
  // Dashboard
  async getDashboard(): Promise<DashboardData> {
    const token = this.getAccessToken()
    const response = await fetch(`${API_URL}/finanzas/dashboard/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    return this.handleResponse<DashboardData>(response)
  }

async createMovimiento(
  tipo: "ingreso" | "gasto", 
  monto: number, 
  categoria: string, 
  descripcion: string = "",
  fecha?: string
): Promise<any> {
  const token = this.getAccessToken()
  
  const payload: any = {
    tipo,
    monto,
    categoria,
    descripcion,
  }
  
  if (fecha) {
    payload.fecha = fecha
  }
  
  console.log("[API] Enviando movimiento:", payload)
  
  // CAMBIAR ESTA LÍNEA - usar /registros/ en lugar de /dashboard/
  const response = await fetch(`${API_URL}/finanzas/registros/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  })

  return this.handleResponse<any>(response)
}

  private async handleResponse<T>(response: Response): Promise<T> {
  console.log("[v0] API Response:", {
    url: response.url,
    status: response.status,
    statusText: response.statusText,
    contentType: response.headers.get("content-type"),
  })

  const contentType = response.headers.get("content-type")
  
  let data: any
  
  if (!contentType || !contentType.includes("application/json")) {
    const text = await response.text()
    console.error("[v0] Non-JSON response:", text.substring(0, 500))
    throw new Error(
      `El servidor devolvió HTML en lugar de JSON. Verifica que el backend esté corriendo en ${API_URL}`,
    )
  }

  try {
    data = await response.json()
  } catch (e) {
    console.error("[v0] Error parsing JSON:", e)
    throw new Error("Error al parsear la respuesta del servidor")
  }

  if (!response.ok) {
    console.error("[v0] API Error Response:", data)
    console.error("[v0] API Error Keys:", Object.keys(data))
    
    // Intentar extraer el mensaje de error de diferentes formatos
    let errorMessage = "Error en la petición"
    
    if (data.detail) {
      errorMessage = data.detail
    } else if (data.message) {
      errorMessage = data.message
    } else if (data.error) {
      errorMessage = data.error
    } else if (typeof data === 'string') {
      errorMessage = data
    } else {
      // Si hay errores de validación de campos
      const errors = []
      for (const [key, value] of Object.entries(data)) {
        if (Array.isArray(value)) {
          errors.push(`${key}: ${value.join(', ')}`)
        } else {
          errors.push(`${key}: ${value}`)
        }
      }
      if (errors.length > 0) {
        errorMessage = errors.join('; ')
      }
    }
    
    throw new Error(errorMessage)
  }

  return data
}
}

export const api = new ApiService()
export type { RecursoAprendizaje, Recomendacion }

