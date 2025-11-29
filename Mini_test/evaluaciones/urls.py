from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MiniTestViewSet, PreguntaTestViewSet

router = DefaultRouter()
router.register(r'tests', MiniTestViewSet)
router.register(r'preguntas', PreguntaTestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]