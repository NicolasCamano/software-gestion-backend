# gestion/serializers.py

from rest_framework import serializers
from .models import SalaJuegos, Maquina, Recaudacion, RegistroInventario, Mantenimiento
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class SalaJuegosSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaJuegos
        fields = ['id', 'nombre_sala', 'direccion']

class MaquinaSerializer(serializers.ModelSerializer):
    sala = SalaJuegosSerializer(read_only=True)
    sala_id = serializers.PrimaryKeyRelatedField(
        queryset=SalaJuegos.objects.all(), source='sala', write_only=True, required=False, allow_null=True
    )
    class Meta:
        model = Maquina
        # Añadimos los nuevos campos al serializer
        fields = ['id', 'codigo_maquina', 'nombre_maquina', 'precio_juego', 'sala', 'sala_id', 
                  'categoria', 'subtipo', 'producto_en_maquina', 'capacidad_producto']

# Nuevo serializer para el nuevo modelo
class RegistroInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroInventario
        fields = '__all__'

class RecaudacionSerializer(serializers.ModelSerializer):
    diferencia = serializers.ReadOnlyField()
    recaudacion_calculada = serializers.ReadOnlyField()
    
    class Meta:
        model = Recaudacion
        fields = '__all__'

class MantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mantenimiento
        fields = '__all__'
    
    # Validamos que la descripción no exceda los 150 caracteres
    def validate_descripcion(self, value):
        if len(value) > 150:
            raise serializers.ValidationError("La descripción no puede exceder los 150 caracteres.")
        return value
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Añadimos campos personalizados al payload del token
        token['username'] = user.username
        # Obtenemos los nombres de los grupos y los añadimos como una lista
        token['groups'] = [group.name for group in user.groups.all()]

        return token