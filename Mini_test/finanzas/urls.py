from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroFinancieroViewSet, ReporteFinancieroViewSet, MetaFinancieraViewSet, DashboardViewSet

router = DefaultRouter()
router.register(r'registros', RegistroFinancieroViewSet)
router.register(r'reportes', ReporteFinancieroViewSet)
router.register(r'metas', MetaFinancieraViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]