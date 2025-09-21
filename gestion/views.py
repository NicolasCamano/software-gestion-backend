# gestion/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse
from rest_framework.decorators import action 
from django_filters.rest_framework import DjangoFilterBackend
from .models import SalaJuegos, Maquina, Recaudacion, RegistroInventario, Mantenimiento
from .serializers import (
    SalaJuegosSerializer, MaquinaSerializer, RecaudacionSerializer, 
    RegistroInventarioSerializer, MantenimientoSerializer, MyTokenObtainPairSerializer
)
from .permissions import EsAdministrador, EsTecnico, EsRepositor
import qrcode
import io

# --- ViewSets con la Lógica de Permisos Simplificada ---

# SalaJuegos y MaquinaViewSet no cambian, su lógica es correcta.
class SalaJuegosViewSet(viewsets.ModelViewSet):
    queryset = SalaJuegos.objects.all()
    serializer_class = SalaJuegosSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']: return [IsAuthenticated()]
        return [EsAdministrador()]

class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sala']
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'qr_code']: return [IsAuthenticated()]
        return [EsAdministrador()]
    @action(detail=True, methods=['get'])
    def qr_code(self, request, pk=None):
        # ... (código del QR)
        maquina = self.get_object()
        url_a_codificar = f"http://localhost:3000/maquinas/{maquina.id}"
        qr_img = qrcode.make(url_a_codificar)
        buffer = io.BytesIO()
        qr_img.save(buffer, format='PNG')
        return HttpResponse(buffer.getvalue(), content_type="image/png")

# --- ¡NUEVA LÓGICA SIMPLIFICADA PARA RECAUDACIONES! ---
class RecaudacionViewSet(viewsets.ModelViewSet):
    queryset = Recaudacion.objects.all()
    serializer_class = RecaudacionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['maquina']
    
    def get_permissions(self):
        # Regla 1: Para EDITAR una recaudación existente (cambiar contadores históricos),
        # se debe ser Administrador.
        if self.action in ['update', 'partial_update', 'destroy']:
            return [EsAdministrador()]
        
        # Regla 2: Para CUALQUIER OTRA COSA (ver la lista, ver detalles, crear una nueva),
        # solo se necesita estar logueado.
        return [IsAuthenticated()]

class RegistroInventarioViewSet(viewsets.ModelViewSet):
    queryset = RegistroInventario.objects.all()
    serializer_class = RegistroInventarioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['maquina']
    permission_classes = [IsAuthenticated] # Mantenemos el permiso simple

class MantenimientoViewSet(viewsets.ModelViewSet):
    queryset = Mantenimiento.objects.all()
    serializer_class = MantenimientoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['maquina']
    # Ahora, la única regla es que el usuario debe haber iniciado sesión.
    permission_classes = [IsAuthenticated]
    
# La vista del Token no cambia.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


    # gestion/views.py

# ... (todo tu código anterior de ViewSets se queda como está) ...


# --- CÓDIGO TEMPORAL PARA CREAR UN SUPERUSUARIO ---
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny]) # Permite que cualquiera visite esta URL sin login
def crear_superusuario_temporal(request):
    User = get_user_model()
    USERNAME = 'adminprod' # Elige un nombre de usuario
    PASSWORD = 'PasswordSeguroParaProd123!' # Elige una contraseña segura
    EMAIL = 'admin@example.com'

    if User.objects.filter(username=USERNAME).exists():
        return Response({"status": "error", "message": f"El usuario '{USERNAME}' ya existe."})

    try:
        User.objects.create_superuser(username=USERNAME, email=EMAIL, password=PASSWORD)
        return Response({"status": "éxito", "message": f"Superusuario '{USERNAME}' creado. ¡Ahora borra este código!"})
    except Exception as e:
        return Response({"status": "error", "message": str(e)})