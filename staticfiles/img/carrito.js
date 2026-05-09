document.addEventListener('DOMContentLoaded', function() {
    const ciudadSelect = document.getElementById('select-ciudad');
    const envioDisplay = document.getElementById('envio-valor');
    const totalDisplay = document.getElementById('total-valor');

    // Leemos los datos que preparamos en el HTML
    const jsonCarrito = document.getElementById('datos-carrito').textContent;
    const items = JSON.parse(jsonCarrito);
    const totalBase = window.TOTAL_BASE_GRASSPET;

    function recalcular() {
        const destino = ciudadSelect.value;
        let costoEnvioTotal = 0;

        items.forEach(item => {
            if (destino === "villeta") {
                // Tarifa Villeta: XL $65.000, Normal $35.000
                costoEnvioTotal += item.esXL ? 65000 : 35000;
            } else if (destino === "funza") {
                costoEnvioTotal += 0;
            } else if (destino === "faca") {
                costoEnvioTotal += item.esXL ? 28000 : 15000;
            }
            // Puedes agregar más ciudades aquí
        });

        // Actualizar visualmente el Envío
        if (envioDisplay) {
            envioDisplay.innerText = costoEnvioTotal > 0 ? 
                "$ " + costoEnvioTotal.toLocaleString('es-CO') : "¡Gratis!";
        }

        // Actualizar el Total Final
        if (totalDisplay) {
            const granTotal = totalBase + costoEnvioTotal;
            totalDisplay.innerText = "$ " + granTotal.toLocaleString('es-CO', { 
                minimumFractionDigits: 1,
                maximumFractionDigits: 1 
            });
        }
    }

    if (ciudadSelect) {
        ciudadSelect.addEventListener('change', recalcular);
    }
});