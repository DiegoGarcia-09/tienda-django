from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=0) # Ideal para pesos colombianos
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    # SOLUCIÓN RÁPIDA: Copia el link directo de Cloudinary aquí
    imagen_url = models.CharField(
        max_length=500, 
        null=True, 
        blank=True, 
        verbose_name="URL de la imagen (Cloudinary)"
    )
    
    # Campo opcional por si decides volver al método anterior luego
    # imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class FAQ(models.Model):
    pregunta = models.CharField(max_length=255)
    respuesta = models.TextField()
    orden = models.IntegerField(default=0) # Para organizar cuál va primero

    def __str__(self):
        return self.pregunta
    
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre_completo = models.CharField(max_length=100)
    direccion = models.CharField(max_length=250)
    ciudad = models.CharField(max_length=100)
    # Agregamos el teléfono aquí mismo
    telefono = models.CharField(max_length=20, null=True, blank=True) 
    metodo_pago = models.CharField(max_length=50, choices=[
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
        ('CONTRAENTREGA', 'Pago contra entrega'),
        ('MERCADOPAGO', 'Mercado Pago')
    ])
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.nombre_completo}"
    
    from cloudinary.models import CloudinaryField
    imagen = CloudinaryField('image', null=True, blank=True)