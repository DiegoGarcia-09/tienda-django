from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('actualizar_carrito/<int:producto_id>/<int:cantidad>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('preguntas-frecuentes/', views.faq_view, name='faq'),
    path('finalizar-compra/', views.checkout, name='checkout'),
]