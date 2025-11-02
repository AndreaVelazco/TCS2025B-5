# Sistema de Gestión Financiera y Educativa

Este proyecto es una plataforma integral que combina evaluación financiera, gestión de finanzas personales, recursos educativos y oportunidades económicas. Está desarrollado con Django y Django REST Framework.

## Estructura del Proyecto

El proyecto está organizado en módulos especializados:

### 1. Módulo de Usuarios
Gestión de usuarios y autenticación.
- **Modelo Principal**: `Usuario`
  - id_usuario (PK)
  - nombre
  - correo
  - contraseña (hash)
  - perfil (principiante/intermedio/avanzado)

### 2. Módulo de Evaluaciones
Sistema de evaluación de conocimientos financieros.
- **Modelo Principal**: `MiniTest`
  - id_test (PK)
  - id_usuario (FK → Usuario)
  - resultado (JSON)
  - fecha
  - nivel_determinado

### 3. Módulo de Finanzas
Gestión de registros y reportes financieros.
- **Modelos**:
  - `RegistroFinanciero`
    - id_registro (PK)
    - id_usuario (FK → Usuario)
    - tipo (ingreso/gasto)
    - monto
    - fecha
    - categoria
    - oportunidad (FK → OportunidadEconomica)
  
  - `ReporteFinanciero`
    - id_reporte (PK)
    - id_usuario (FK → Usuario)
    - mes/año
    - total_ingresos
    - total_gastos
    - balance

### 4. Módulo de Aprendizaje
Recursos educativos y sistema de recomendaciones.
- **Modelos**:
  - `RecursoAprendizaje`
    - id_recurso (PK)
    - tipo
    - titulo
    - enlace
    - tematica
  
  - `Recomendacion`
    - id_recomendacion (PK)
    - id_usuario (FK → Usuario)
    - id_recurso (FK → RecursoAprendizaje)
    - criterio
    - fecha_recomendacion

### 5. Módulo de Oportunidades
Gestión de oportunidades económicas.
- **Modelo Principal**: `OportunidadEconomica`
  - id_oportunidad (PK)
  - nombre_programa
  - tipo
  - institucion
  - enlace
  - fecha_inicio
  - fecha_fin

## Relaciones entre Módulos

1. **Usuario como Centro**
   - Un usuario puede tener múltiples tests (1:N)
   - Un usuario puede tener múltiples registros financieros (1:N)
   - Un usuario puede tener múltiples reportes financieros (1:N)
   - Un usuario puede recibir múltiples recomendaciones (1:N)

2. **Integración de Servicios**
   - Las recomendaciones se basan en recursos de aprendizaje (N:1)
   - Los registros financieros pueden estar vinculados a oportunidades económicas (N:1)

## Requisitos del Sistema

- Python 3.x
- PostgreSQL
- Django 5.2
- Django REST Framework
- pip (gestor de paquetes de Python)

## Configuración del Entorno

1. Crear un entorno virtual:
```bash
python -m venv venv
```

2. Activar el entorno virtual:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Instalar las dependencias:
```bash
pip install django djangorestframework django-cors-headers psycopg2
```

## Configuración del Proyecto

1. Aplicar las migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

2. Crear un superusuario:
```bash
python manage.py createsuperuser
```

3. Iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```

## Estructura del Proyecto

El proyecto está organizado en los siguientes módulos:

- **usuarios**: Gestión de usuarios y autenticación
- **evaluaciones**: Sistema de evaluación y tests
- **finanzas**: Gestión de registros financieros y reportes
- **aprendizaje**: Recursos de aprendizaje y recomendaciones
- **oportunidades**: Gestión de oportunidades económicas

## API Endpoints

### Usuarios
- `GET /api/usuarios/`: Lista de usuarios
- `POST /api/usuarios/`: Crear usuario
- `GET /api/usuarios/me/`: Obtener usuario actual

### Evaluaciones
- `GET /api/evaluaciones/tests/`: Lista de tests
- `POST /api/evaluaciones/tests/obtener_preguntas/`: Obtener preguntas para test
- `POST /api/evaluaciones/tests/enviar_respuestas/`: Enviar respuestas

### Finanzas
- `GET /api/finanzas/registros/`: Lista de registros financieros
- `GET /api/finanzas/reportes/`: Lista de reportes financieros
- `GET /api/finanzas/metas/`: Lista de metas financieras

### Aprendizaje
- `GET /api/aprendizaje/recursos/`: Lista de recursos de aprendizaje
- `GET /api/aprendizaje/recomendaciones/`: Lista de recomendaciones

### Oportunidades
- `GET /api/oportunidades/`: Lista de oportunidades económicas
- `GET /api/oportunidades/vigentes/`: Lista de oportunidades vigentes
- `GET /api/oportunidades/por_tipo/`: Filtrar oportunidades por tipo

## Autenticación (JWT)

El proyecto usa tokens JWT para autenticar peticiones a la API. Endpoints disponibles:

- `POST /api/token/` - Obtener pair de tokens (access + refresh)
- `POST /api/token/refresh/` - Refrescar token de acceso usando refresh token

Ejemplo con cURL para obtener tokens:

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"correo": "test@test.com", "password": "password123"}'
```

Respuesta esperada:

```json
{
  "access": "<ACCESS_TOKEN>",
  "refresh": "<REFRESH_TOKEN>"
}
```

Usar el token de acceso en las peticiones protegidas:

Header:

```
Authorization: Bearer <ACCESS_TOKEN>
```

Ejemplo con cURL (obtener recursos protegidos):

```bash
curl -X GET http://localhost:8000/api/finanzas/registros/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

## Desarrollo

Para contribuir al proyecto:

1. Crear una nueva rama para tu feature
2. Desarrollar y probar los cambios
3. Crear un pull request con una descripción detallada

## Notas de Seguridad

- Cambiar SECRET_KEY en producción
- Configurar DEBUG = False en producción
- Actualizar ALLOWED_HOSTS según necesidad
- Implementar autenticación JWT para la API