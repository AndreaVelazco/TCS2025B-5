<div align="center">
<table>
    <thead>
        <tr>
            <th>
                <img src="https://github.com/RodrigoStranger/imagenes-la-salle/blob/main/logo_secundario_color.png?raw=true" width="150"/>
            </th>
            <th>
                <span style="font-weight:bold;">UNIVERSIDAD LA SALLE DE AREQUIPA</span><br />
                <span style="font-weight:bold;">FACULTAD DE INGENIERÍAS Y ARQUITECTURA</span><br />
                <span style="font-weight:bold;">DEPARTAMENTO ACADEMICO DE INGENIERÍA Y MATEMÁTICAS</span><br />
                <span style="font-weight:bold;">CARRERA PROFESIONAL DE INGENIERÍA DE SOFTWARE</span>
            </th>
        </tr>
    </thead>
</table>
</div>

<div align="center">
  <h2 style="font-weight:bold;">TECNOLOGÍAS DE CONSTRUCCIÓN DE SOFTWARE</h2>
</div>

<div align="center">
<table>
    <thead>
        <tr>
            <th><strong>Semestre</strong></th>
            <th><strong>Profesor</strong></th>
            <th><strong>Créditos</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="center">2025 II</td>
            <td align="center">Edson Francisco Luque Mamani</td>
            <td align="center">4</td>
        </tr>
    </tbody>
</table>
</div>

<div align="center">
<table>
    <thead>
        <tr>
            <th><strong>Integrantes</strong></th>
            <th><strong>Correo</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="center">Andrea Del Rosario Velazco Yana</td>
            <td align="center">
                <a href="mailto:avelazcoy@ulasalle.edu.pe">avelazcoy@ulasalle.edu.pe</a>
            </td>
        </tr>
        <tr>
            <td align="center">Enyelbert Anderson Panta Huaracha</td>
            <td align="center">
                <a href="mailto:epantah@ulasalle.edu.pe">epantah@ulasalle.edu.pe</a>
            </td>
        </tr>
        <tr>
            <td align="center">Jerson Ernesto Chura Pacci</td>
            <td align="center">
                <a href="mailto:jchurap@ulasalle.edu.pe">jchurap@ulasalle.edu.pe</a>
            </td>
        </tr>
        <tr>
            <td align="center">Melany Yasmin Lazo Arana</td>
            <td align="center">
                <a href="mailto:mlazoa@ulasalle.edu.pe">mlazoa@ulasalle.edu.pe</a>
            </td>
        </tr>
    </tbody>
</table>
</div>

<div align="center">
  <h2 style="font-weight:bold;">BIZUP</h2>
  <p><strong>Plataforma de Educación Financiera y Gestión Personal para Perú</strong></p>
</div>

## Tecnologías Utilizadas

### Backend
[![Python][Python]][python-site]
[![Django][Django]][django-site]
[![PostgreSQL][PostgreSQL]][postgresql-site]
[![JWT][JWT]][jwt-site]

### Frontend
[![Next.js][Nextjs]][nextjs-site]
[![React][React]][react-site]
[![TypeScript][TypeScript]][typescript-site]
[![TailwindCSS][TailwindCSS]][tailwindcss-site]

### DevOps & Herramientas
[![Docker][Docker]][docker-site]
[![Nginx][Nginx]][nginx-site]
[![Git][Git]][git-site]
[![GitHub][GitHub]][github-site]

## Descripción del Proyecto

**BizUp** es una plataforma integral de educación financiera y gestión de finanzas personales diseñada específicamente para usuarios en Perú. Combina evaluación de conocimientos financieros, seguimiento de ingresos y gastos, recursos educativos personalizados y acceso a oportunidades económicas.

### Características Principales

- **Mini Test Financiero**: Evalúa el nivel de conocimiento financiero del usuario (principiante, intermedio, avanzado)
- **Gestión Financiera**: Registro y seguimiento de ingresos y gastos con reportes semanales automáticos
- **Recursos de Aprendizaje**: Recomendaciones personalizadas de contenido educativo según el nivel del usuario
- **Oportunidades Económicas**: Catálogo de programas, becas y cursos disponibles en Perú
- **Dashboard Interactivo**: Visualización de métricas financieras y progreso educativo

## Arquitectura del Proyecto

El proyecto utiliza una arquitectura de **microservicios containerizados** con Docker:

```
┌─────────────────────────────────────────────┐
│           Nginx (Proxy Reverso)             │
│              Puerto: 8095                   │
└─────────────┬───────────────────────────────┘
              │
      ┌───────┴────────┐
      │                │
┌─────▼─────┐    ┌────▼─────┐
│  Frontend │    │  Backend │
│  Next.js  │    │  Django  │
│  :3000    │    │  :8000   │
└───────────┘    └────┬─────┘
                      │
                ┌─────▼──────┐
                │ PostgreSQL │
                │   :5455    │
                └────────────┘
```

### Componentes

1. **PostgreSQL (Puerto 5455)**: Base de datos principal
2. **Backend Django (Puerto interno 8000)**: API REST con Django REST Framework
3. **Frontend Next.js (Puerto interno 3000)**: Interfaz de usuario con React 19
4. **Nginx (Puerto 8095)**: Proxy reverso y balanceador de carga

## Estructura del Proyecto

```
TCS2025B-5/
├── Mini_test/                    # Backend Django
│   ├── minitest/                 # Configuración del proyecto
│   ├── usuarios/                 # App de autenticación
│   ├── evaluaciones/             # App de mini tests
│   ├── finanzas/                 # App de gestión financiera
│   ├── aprendizaje/              # App de recursos educativos
│   ├── oportunidades/            # App de oportunidades económicas
│   ├── Dockerfile                # Imagen Docker del backend
│   ├── docker-entrypoint.sh      # Script de inicialización
│   └── requirements.txt          # Dependencias Python
│
├── bizup-frontend/               # Frontend Next.js
│   ├── src/
│   │   ├── app/                  # Páginas (App Router)
│   │   ├── components/           # Componentes reutilizables
│   │   └── lib/                  # Utilidades y API client
│   ├── Dockerfile                # Imagen Docker del frontend
│   └── package.json              # Dependencias Node.js
│
├── nginx/                        # Configuración Nginx
│   ├── nginx.conf                # Proxy reverso
│   └── Dockerfile                # Imagen Docker de Nginx
│
├── docker-compose.yml            # Orquestación de contenedores
├── .env                          # Variables de entorno
└── README.md                     # Este archivo
```

## Instalación y Despliegue con Docker

### Requisitos Previos

- Docker (versión 20.10 o superior)
- Docker Compose (versión 2.0 o superior)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/AndreaVelazco/TCS2025B-5.git
cd TCS2025B-5
```

2. **Levantar los servicios con Docker Compose**
```bash
docker-compose up -d
```

**¿Qué hace `docker-compose up -d`?**
- `docker-compose up`: Construye las imágenes (si no existen) y levanta todos los contenedores definidos en `docker-compose.yml`
- `-d` (detached): Ejecuta los contenedores en segundo plano, liberando la terminal

3. **Verificar el estado de los contenedores**
```bash
docker-compose ps
```

Deberías ver 4 contenedores en estado "Up":
- `bizup_db` - PostgreSQL
- `bizup_backend` - Django
- `bizup_frontend` - Next.js
- `bizup_nginx` - Nginx

4. **Acceder a la aplicación**
- **Aplicación**: http://localhost:8095
- **Admin Django**: http://localhost:8095/admin
  - Email: `admin@gmail.com`
  - Contraseña: `admin123`

### Comandos Útiles de Docker Compose

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend

# Detener los contenedores
docker-compose stop

# Iniciar contenedores detenidos
docker-compose start

# Detener y eliminar contenedores
docker-compose down

# Reconstruir un servicio
docker-compose up -d --build backend

# Ver uso de recursos
docker stats
```

## Base de Datos

### Módulos Principales

1. **usuarios**: Gestión de usuarios con modelo personalizado
2. **evaluaciones**: Sistema de mini tests con categorización
3. **finanzas**: Registro de transacciones y reportes semanales
4. **aprendizaje**: Recursos educativos y recomendaciones
5. **oportunidades**: Programas y becas disponibles

### Inicialización

El backend ejecuta automáticamente:
- Migraciones de base de datos
- Creación de superusuario
- Población de datos iniciales (preguntas, recursos, oportunidades)
- Recolección de archivos estáticos

## Autenticación

El sistema utiliza **JWT (JSON Web Tokens)** para autenticación:

- **Access Token**: Expira en 60 minutos
- **Refresh Token**: Expira en 7 días
- El modelo de usuario usa `correo` (email) como campo de autenticación

## API REST

El backend expone una API RESTful documentada en:
- Base URL: `http://localhost:8095/api`

### Endpoints Principales

```
POST   /api/token/                    # Obtener tokens JWT
POST   /api/token/refresh/            # Refrescar access token
GET    /api/usuarios/                 # Listar usuarios
POST   /api/evaluaciones/minitest/    # Enviar respuestas del test
GET    /api/finanzas/registros/       # Obtener registros financieros
POST   /api/finanzas/registros/       # Crear registro financiero
GET    /api/finanzas/reportes/        # Obtener reportes semanales
GET    /api/aprendizaje/recursos/     # Listar recursos educativos
GET    /api/aprendizaje/recomendaciones/ # Recomendaciones personalizadas
GET    /api/oportunidades/            # Listar oportunidades económicas
```

<!-- Badges -->
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[python-site]: https://www.python.org/

[Django]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
[django-site]: https://www.djangoproject.com/

[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[postgresql-site]: https://www.postgresql.org/

[JWT]: https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white
[jwt-site]: https://jwt.io/

[Nextjs]: https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[nextjs-site]: https://nextjs.org/

[React]: https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black
[react-site]: https://reactjs.org/

[TypeScript]: https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white
[typescript-site]: https://www.typescriptlang.org/

[TailwindCSS]: https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white
[tailwindcss-site]: https://tailwindcss.com/

[Docker]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[docker-site]: https://www.docker.com/

[Nginx]: https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white
[nginx-site]: https://nginx.org/

[Git]: https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white
[git-site]: https://git-scm.com/

[GitHub]: https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white
[github-site]: https://github.com/
