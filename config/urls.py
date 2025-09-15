# config/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
# Importamos NUESTRA vista personalizada para obtener el token
from gestion.views import MyTokenObtainPairView

urlpatterns = [
    # 1. La ruta del Panel de Administración
    path('admin/', admin.site.urls),
    
    # 2. La ruta principal a nuestra API, que redirige al "mapa del barrio" (gestion.urls)
    path('api/v1/', include('gestion.urls')),

    # 3. Las rutas para la autenticación (la oficina de pasaportes)
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]