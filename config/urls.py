# config/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from gestion.views import MyTokenObtainPairView

# --- ESTRUCTURA DE URLS UNIFICADA ---
# Creamos una lista para TODAS las rutas de la API.
api_urlpatterns = [
    # Esta línea incluye todas las URLs de 'gestion' (maquinas, salas, etc.)
    path('', include('gestion.urls')),
    
    # --- LA CORRECCIÓN ESTÁ AQUÍ ---
    # Añadimos la ruta de 'refresh' dentro de la API, donde pertenece.
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # La ruta principal '/api/v1/' ahora incluye TODAS las rutas de la API.
    path('api/v1/', include(api_urlpatterns)),
]