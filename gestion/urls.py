# gestion/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SalaJuegosViewSet, MaquinaViewSet, RecaudacionViewSet, 
    RegistroInventarioViewSet, MantenimientoViewSet
)

router = DefaultRouter()
router.register(r'salas', SalaJuegosViewSet, basename='sala')
router.register(r'maquinas', MaquinaViewSet, basename='maquina')
router.register(r'recaudaciones', RecaudacionViewSet, basename='recaudacion')
router.register(r'inventario', RegistroInventarioViewSet, basename='registroinventario')
router.register(r'mantenimientos', MantenimientoViewSet, basename='mantenimiento')

urlpatterns = [
    path('', include(router.urls)),
]