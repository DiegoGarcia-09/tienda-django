from django.contrib import admin
from .models import Producto, Categoria, Pedido

# Registramos Categoria y Pedido para que aparezcan en el panel
admin.site.register(Categoria)
admin.site.register(Pedido)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Esto organiza las columnas que ves en la lista de productos
    list_display = ('nombre', 'precio', 'stock', 'categoria')
    # Esto añade un buscador por nombre
    search_fields = ('nombre',)
    # Esto añade un filtro lateral por categoría
    list_filter = ('categoria',)