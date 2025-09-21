# gestion/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SalaJuegosViewSet, 
    MaquinaViewSet, 
    RecaudacionViewSet, 
    RegistroInventarioViewSet, 
    MantenimientoViewSet,
    crear_superusuario_temporal 
)

# Este router crea las rutas para todos nuestros modelos de la app 'gestion'
router = DefaultRouter()
router.register(r'salas', SalaJuegosViewSet, basename='sala')
router.register(r'maquinas', MaquinaViewSet, basename='maquina')
router.register(r'recaudaciones', RecaudacionViewSet, basename='recaudacion')
router.register(r'inventario', RegistroInventarioViewSet, basename='registroinventario') 
router.register(r'mantenimientos', MantenimientoViewSet, basename='mantenimiento')


# Exportamos las URLs que el router ha generado
urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('', include(router.urls)),
    # 2. Añade esta nueva línea para la URL secreta
    path('crear-superusuario-secreto-ahora/', crear_superusuario_temporal, name='crear_superusuario_temporal'),
]


