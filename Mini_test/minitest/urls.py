from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from usuarios.auth import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/evaluaciones/', include('evaluaciones.urls')),
    path('api/finanzas/', include('finanzas.urls')),
    path('api/aprendizaje/', include('aprendizaje.urls')),
    path('api/oportunidades/', include('oportunidades.urls')),
    # JWT auth endpoints
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
