import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Producto, Categoria, Pedido, FAQ

# --- VISTA PRINCIPAL ---
def lista_productos(request):
    productos = Producto.objects.all()
    carrito_session = request.session.get('carrito', {})
    
    carrito_completo = []
    subtotal_acumulado = 0
    
    for p_id, cantidad in carrito_session.items():
        try:
            p = Producto.objects.filter(id=p_id).first()
            if p:
                subtotal_item = p.precio * cantidad
                subtotal_acumulado += subtotal_item
                carrito_completo.append({
                    'producto': p,
                    'cantidad': cantidad,
                    'subtotal': subtotal_item
                })
        except Exception:
            continue

    # IMPORTANTE: Asegúrate de que esta ruta sea la correcta para tu lista.html
    return render(request, 'productos/lista.html', {
        'productos': productos,
        'carrito_detallado': carrito_completo,
        'subtotal_panel': subtotal_acumulado
    })

# --- GESTIÓN DEL CARRITO ---
def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    id_str = str(producto_id)
    
    carrito[id_str] = carrito.get(id_str, 0) + 1
    request.session['carrito'] = carrito
    request.session.modified = True
    
    total_items = sum(carrito.values())
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'ok',
            'carrito_total_items': total_items
        })
    
    return redirect(request.META.get('HTTP_REFERER', 'lista_productos'))

def ver_carrito(request):
    carrito_session = request.session.get('carrito', {})
    productos_finales = []
    total_compra = 0

    for p_id, cantidad in carrito_session.items():
        try:
            producto = Producto.objects.filter(id=p_id).first()
            if producto:
                subtotal = producto.precio * cantidad
                total_compra += subtotal
                productos_finales.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'subtotal': subtotal
                })
        except Exception:
            continue

    total_con_envio = total_compra  

    return render(request, 'productos/carrito.html', {
        'carrito': productos_finales,
        'total_carrito': total_compra,
        'total_con_envio': total_con_envio,
    })

def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    id_str = str(producto_id)
    if id_str in carrito:
        del carrito[id_str]
        request.session['carrito'] = carrito
        request.session.modified = True
    return redirect('ver_carrito')

def actualizar_carrito(request, producto_id, cantidad):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        carrito[str(producto_id)] = int(cantidad)
        request.session['carrito'] = carrito
        request.session.modified = True
    return JsonResponse({'success': True})

# --- FAQ ---
def faq_view(request):
    faqs = FAQ.objects.all().order_by('orden')
    return render(request, 'productos/faq.html', {'faqs': faqs})

# --- CHECKOUT Y PAGO ---
def checkout(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('ver_carrito')

    total = 0
    for producto_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id=producto_id)
            total += float(producto.precio) * int(cantidad)
        except Producto.DoesNotExist:
            continue

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        telefono = request.POST.get('telefono')
        metodo = request.POST.get('metodo_pago') 

        nuevo_pedido = Pedido.objects.create(
            nombre_completo=nombre,
            direccion=direccion,
            ciudad=ciudad,
            telefono=telefono,
            metodo_pago=metodo,
            total=total,
            pagado=False
        )

        request.session['carrito'] = {}
        request.session.modified = True
        
        if metodo == 'CONTRAENTREGA':
            return render(request, 'productos/pago_contraentrega.html', {'pedido': nuevo_pedido})
        
        elif metodo == 'TRANSFERENCIA':
            mensaje_wa = (
                f"🌿 *NUEVO PEDIDO GRASSPET*\n\n"
                f"Hola! Envío el comprobante de mi pedido.\n\n"
                f"📦 *Pedido:* #{nuevo_pedido.id}\n"
                f"👤 *Cliente:* {nuevo_pedido.nombre_completo}\n"
                f"💰 *Total:* ${nuevo_pedido.total}"
            )
            mensaje_codificado = urllib.parse.quote(mensaje_wa)
            # REEMPLAZA EL NÚMERO CON EL TUYO REAL
            whatsapp_url = f"https://wa.me/573159595732?text={mensaje_codificado}"

            return render(request, 'productos/transferenciaqr.html', {
                'pedido': nuevo_pedido,
                'whatsapp_url': whatsapp_url
            })

    return render(request, 'productos/checkout.html', {'total': total})