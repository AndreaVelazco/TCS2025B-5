from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OportunidadEconomicaViewSet

router = DefaultRouter()
router.register(r'', OportunidadEconomicaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
