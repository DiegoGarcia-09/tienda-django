from django.contrib import admin
from .models import Producto, Categoria, Pedido

admin.site.register(Categoria)
admin.site.register(Pedido)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # ELIMINAMOS 'imagen' y usamos solo los campos que existen
    list_display = ('nombre', 'precio', 'stock', 'categoria')
    search_fields = ('nombre',)
    list_filter = ('categoria',)