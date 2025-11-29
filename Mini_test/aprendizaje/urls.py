from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecursoAprendizajeViewSet, RecomendacionViewSet

router = DefaultRouter()
router.register(r'recursos', RecursoAprendizajeViewSet)
router.register(r'recomendaciones', RecomendacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
