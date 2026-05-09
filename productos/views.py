from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto



def lista_productos(request):
    productos = Producto.objects.all()
    carrito_session = request.session.get('carrito', {})
    
    carrito_completo = []
    subtotal_acumulado = 0
    
    for p_id, cantidad in carrito_session.items():
        try:
            p = Producto.objects.get(id=p_id)
            subtotal_item = p.precio * cantidad
            subtotal_acumulado += subtotal_item
            carrito_completo.append({
                'producto': p,
                'cantidad': cantidad,
                'subtotal': subtotal_item
            })
        except Producto.DoesNotExist:
            continue

    return render(request, 'productos/lista.html', {
        'productos': productos,
        'carrito_detallado': carrito_completo,
        'subtotal_panel': subtotal_acumulado
    })

from django.http import JsonResponse # Asegúrate de tener este import arriba

def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    id_str = str(producto_id)
    
    # Sumamos el producto
    carrito[id_str] = carrito.get(id_str, 0) + 1
    request.session['carrito'] = carrito
    request.session.modified = True
    
    # Calculamos el total de items para el numerito verde
    total_items = sum(carrito.values())
    
    # SI ES AJAX (JavaScript), respondemos con datos, no con redirección
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'ok',
            'carrito_total_items': total_items
        })
    
    # SI NO ES AJAX (por si falla el JS), redirigimos a donde estaba
    return redirect(request.META.get('HTTP_REFERER', 'lista_productos'))

def ver_carrito(request):
    carrito_session = request.session.get('carrito', {})
    productos_finales = []
    total_compra = 0

    for p_id, cantidad in carrito_session.items():
        try:
            producto = Producto.objects.get(id=p_id)
            subtotal = producto.precio * cantidad
            total_compra += subtotal

            productos_finales.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })

        except Producto.DoesNotExist:
            continue

    return render(request, 'productos/carrito.html', {
        'carrito': productos_finales,
        'total': total_compra
    })
    

def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    id_str = str(producto_id)
    
    if id_str in carrito:
        del carrito[id_str]
        request.session['carrito'] = carrito
        request.session.modified = True
    
    return redirect('ver_carrito')

from django.http import JsonResponse

def actualizar_carrito(request, producto_id, cantidad):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        carrito[str(producto_id)] = int(cantidad)
        request.session['carrito'] = carrito
        request.session.modified = True
    return JsonResponse({'success': True})

from .models import FAQ # Asegúrate de importar el modelo que creamos antes

def faq_view(request):
    # Traemos todas las preguntas organizadas por el campo 'orden'
    faqs = FAQ.objects.all().order_by('orden')
    return render(request, 'productos/faq.html', {'faqs': faqs})

from django.shortcuts import render, redirect
from .models import Pedido # El que acabamos de crear

import urllib.parse  # Importante para que el mensaje de WhatsApp no se rompa con espacios
from .models import Producto, Pedido # Asegúrate de tener estas importaciones arriba
import urllib.parse
from django.shortcuts import render, redirect
from .models import Pedido, Producto  # Asegúrate de que las importaciones sean correctas

import urllib.parse
from django.shortcuts import render, redirect
from .models import Pedido, Producto 

import urllib.parse
from django.shortcuts import render, redirect
from .models import Pedido, Producto 

def checkout(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('ver_carrito')

    # --- Cálculo del Total ---
    total = 0
    for producto_id, item in carrito.items():
        if isinstance(item, dict):
            precio = float(item.get('precio', 0))
            cantidad = int(item.get('cantidad', 1))
            total += precio * cantidad
        else:
            try:
                producto = Producto.objects.get(id=producto_id)
                total += float(producto.precio) * int(item)
            except Producto.DoesNotExist:
                continue

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        telefono = request.POST.get('telefono')
        metodo = request.POST.get('metodo_pago') 

        # 1. Guardamos el pedido en la base de datos
        nuevo_pedido = Pedido.objects.create(
            nombre_completo=nombre,
            direccion=direccion,
            ciudad=ciudad,
            telefono=telefono,
            metodo_pago=metodo,
            total=total,
            pagado=False
        )

        # 2. Limpiamos el carrito
        request.session['carrito'] = {}
        
        # 3. Redirección según tu HTML (TRANSFERENCIA o CONTRAENTREGA)
        if metodo == 'CONTRAENTREGA':
            # Usa el nombre de archivo que me diste
            return render(request, 'productos/pago_contraentrega.html', {'pedido': nuevo_pedido})
        
        elif metodo == 'TRANSFERENCIA':
            # Preparamos el mensaje de WhatsApp
            mensaje_wa = (
                f"🌿 *NUEVO PEDIDO GRASSPET*\n\n"
                f"Hola! Envío el comprobante de mi pedido.\n\n"
                f"📦 *Pedido:* #{nuevo_pedido.id}\n"
                f"👤 *Cliente:* {nuevo_pedido.nombre_completo}\n"
                f"💰 *Total:* ${nuevo_pedido.total}"
            )
            
            mensaje_codificado = urllib.parse.quote(mensaje_wa)
            # REEMPLAZA EL NÚMERO: Pon el tuyo con el 57 inicial
            whatsapp_url = f"https://wa.me/573001234567?text={mensaje_codificado}"

            # Usa el nombre de archivo que me diste
            return render(request, 'productos/transferenciaqr.html', {
                'pedido': nuevo_pedido,
                'whatsapp_url': whatsapp_url
            })

    return render(request, 'productos/checkout.html', {'total': total})

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags



def confirmar_pedido(request):
    if request.method == 'POST':
        # ... (aquí guardas tu pedido en la base de datos) ...
        # Definimos los valores que el correo necesita mostrar
        carrito_items = carrito.get_items() # O la lógica que uses para listar productos
        subtotal_calc = sum(item.total_item for item in carrito_items)

        # Lógica de envío (Villeta/Funza)
        ciudad_destino = request.POST.get('ciudad', '').lower()
        envio_calc = 35000 if ciudad_destino == 'villeta' else 0

        # Total Final
        total_calc = subtotal_calc + envio_calc

        # Guardamos el pedido para generar el ID real
        nuevo_pedido = Pedido.objects.create(
            usuario=request.user,
            total=total_calc,
            direccion=request.POST.get('direccion')
        )
        # Preparamos los datos para el correo
        contexto = {
            'usuario': request.user,
            'carrito': carrito,      # Los productos
            'subtotal': subtotal,    # Suma de productos
            'envio': costo_envio,    # Lo que calculamos para Villeta/Funza
            'total': total_final,    # La suma de todo
            'direccion': request.POST.get('direccion')
        }

        # Renderizamos el HTML que diseñamos antes
        html_content = render_to_string('emails/confirmacion_pedido.html', contexto)
        text_content = strip_tags(html_content)

        # Creamos el correo
        email = EmailMultiAlternatives(
            subject=f'¡Pedido Recibido! GrassPet #{pedido_id}',
            body=text_content,
            from_email='GrassPet <tu-correo@gmail.com>',
            to=[request.user.email],
        )
        email.attach_alternative(html_content, "text/html")
        
        # ¡ENVIAR!
        email.send()

        return render(request, 'exito.html')
    
