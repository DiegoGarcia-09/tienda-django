def carrito_contador(request):
    carrito = request.session.get('carrito', {})
    total_items = sum(carrito.values())
    return {
        'total_items_carrito': total_items
    }