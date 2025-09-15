from django.db import models
from django.contrib.auth.models import User

class SalaJuegos(models.Model):
    nombre_sala = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, blank=True)
    def __str__(self): return self.nombre_sala

class Maquina(models.Model):
    CATEGORIAS = [
        ('ENTRETENIMIENTO', 'Entretenimiento'),
        ('VENDING', 'Vending'),
        ('OTRA', 'Otra'),
    ]
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='ENTRETENIMIENTO')
    subtipo = models.CharField(max_length=100, blank=True, null=True)
    codigo_maquina = models.CharField(max_length=50, unique=True)
    nombre_maquina = models.CharField(max_length=100)
    precio_juego = models.DecimalField(max_digits=10, decimal_places=2)
    sala = models.ForeignKey(SalaJuegos, on_delete=models.SET_NULL, null=True, blank=True, related_name='maquinas')
    
    # --- NUEVOS CAMPOS PARA INVENTARIO SIMPLE ---
    # Asumimos por ahora que cada máquina maneja un tipo principal de producto.
    producto_en_maquina = models.CharField(max_length=100, blank=True, null=True, help_text="Ej: Peluche Capibara, Coca-Cola 500ml")
    capacidad_producto = models.PositiveIntegerField(default=0, help_text="La cantidad fija que debe llevar la máquina de este producto.")

    def __str__(self): return f"{self.nombre_maquina} ({self.codigo_maquina})"

# --- MODELO DE CARGA DE MERCADERÍA SIMPLIFICADO ---
# Ahora se llamará 'RegistroInventario' para ser más claro.
class RegistroInventario(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='inventario')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    # Los dos únicos datos que introduce el operario:
    stock_encontrado = models.PositiveIntegerField(help_text="Cantidad que queda en la máquina al llegar.")
    cantidad_repuesta = models.PositiveIntegerField(help_text="Cantidad de producto nuevo que se añadió.")

    def __str__(self):
           return f"Inventario de {self.maquina.nombre_maquina} el {self.fecha.strftime('%Y-%m-%d')}"
      
class Recaudacion(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='recaudaciones')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_recaudacion = models.DateTimeField(auto_now_add=True)
    contador_anterior = models.BigIntegerField()
    contador_actual = models.BigIntegerField()
    efectivo_contado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def diferencia(self):
        return self.contador_actual - self.contador_anterior

    @property
    def recaudacion_calculada(self):
        return self.diferencia * self.maquina.precio_juego

    def __str__(self):
        return f"Recaudación de {self.maquina.nombre_maquina} el {self.fecha_recaudacion.strftime('%Y-%m-%d')}"


class Mantenimiento(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='mantenimientos')
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    # Usamos un TextField para el informe, validaremos la longitud en el serializer.
    descripcion = models.TextField()

    def __str__(self):
        return f"Mantenimiento de {self.maquina.nombre_maquina} el {self.fecha.strftime('%Y-%m-%d')}"