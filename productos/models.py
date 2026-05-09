from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    # Cambiamos decimal_places a 0 para Pesos Colombianos
    precio = models.DecimalField(max_digits=12, decimal_places=0) 
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class FAQ(models.Model):
    pregunta = models.CharField(max_length=255)
    respuesta = models.TextField()
    orden = models.IntegerField(default=0) # Para organizar cuál va primero

    def __str__(self):
        return self.pregunta
    
# En productos/models.py
class Pedido(models.Model):
    # ... tus otros campos ...
    imagen = CloudinaryField('image', null=True, blank=True) # Agrega null y blank