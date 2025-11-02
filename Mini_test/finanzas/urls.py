from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroFinancieroViewSet, ReporteFinancieroViewSet, MetaFinancieraViewSet

router = DefaultRouter()
router.register(r'registros', RegistroFinancieroViewSet)
router.register(r'reportes', ReporteFinancieroViewSet)
router.register(r'metas', MetaFinancieraViewSet)

urlpatterns = [
    path('', include(router.urls)),
]