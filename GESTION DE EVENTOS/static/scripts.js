// Variables globales
const menu = document.querySelector('.menu');
const barraLateral = document.querySelector('.barra-lateral');
const spans = document.querySelectorAll('span');
const palanca = document.querySelector('.switch');
const circulo = document.querySelector('.circulo');
const cloud = document.getElementById('cloud');
const crearEvento = document.getElementById('crear-evento');
const opcionesUsuario = document.getElementById('opciones-usuario');
const aplicarFiltrosBtn = document.getElementById('aplicar-filtros');
const listaEventos = document.getElementById('lista-eventos');
const inputFecha = document.getElementById('fecha');
const inputLugar = document.getElementById('lugar');

// Función para renderizar eventos según los filtros aplicados
function renderizarEventos(eventos) {
    listaEventos.innerHTML = ''; // Limpiamos la lista de eventos existentes

    eventos.forEach(evento => {
        const eventoHTML = `
            <li>
                <div class="evento-container">
                    <h3>${evento.nombre}</h3>
                    <p>Fecha: ${evento.fecha}</p>
                    <p>Lugar: ${evento.lugar}</p>
                    <p>Descripción: ${evento.descripcion}</p>
                    <button>Registrarse</button>
                </div>
            </li>
        `;
        listaEventos.innerHTML += eventoHTML; // Agregamos cada evento al HTML
    });
}

// Función para aplicar los filtros y actualizar la lista de eventos
function aplicarFiltros() {
    // Implementa la lógica para obtener los eventos dinámicamente
    obtenerEventos().then(eventos => {
        const filtroFecha = inputFecha.value;
        const filtroLugar = inputLugar.value.trim().toLowerCase();

        // Filtramos los eventos según los criterios seleccionados
        const eventosFiltrados = eventos.filter(evento => {
            const fechaEvento = evento.fecha;
            const lugarEvento = evento.lugar.toLowerCase();

            // Aplicamos filtro de fecha si está seleccionada
            if (filtroFecha && filtroFecha !== '') {
                if (fechaEvento !== filtroFecha) {
                    return false;
                }
            }

            // Aplicamos filtro de lugar si está ingresado
            if (filtroLugar && filtroLugar !== '') {
                if (!lugarEvento.includes(filtroLugar)) {
                    return false;
                }
            }

            return true; // El evento pasa todos los filtros
        });

        renderizarEventos(eventosFiltrados); // Mostramos los eventos filtrados
    });
}

// Evento click para el botón "Aplicar Filtros"
if (aplicarFiltrosBtn) {
    aplicarFiltrosBtn.addEventListener('click', aplicarFiltros);
}

// Lógica adicional para el botón de crear evento (si es necesario)
if (crearEvento) {
    crearEvento.addEventListener('click', () => {
        // Puedes añadir aquí la lógica específica para el botón crear evento
    });
}

// Aquí puedes agregar las funciones y eventos existentes para mostrar/ocultar la barra lateral,
// cambiar al modo oscuro, mostrar opciones de usuario, etc.

// Evento para mostrar/ocultar la barra lateral
menu.addEventListener('click', () => {
    barraLateral.classList.toggle('max-barra-lateral');
    if (barraLateral.classList.contains('max-barra-lateral')) {
        menu.children[0].style.display = 'none';
        menu.children[1].style.display = 'block';
    } else {
        menu.children[0].style.display = 'block';
        menu.children[1].style.display = 'none';
    }
    if (window.innerWidth <= 320) {
        barraLateral.classList.add('mini-barra-lateral');
        spans.forEach(span => {
            span.classList.add('oculto');
        });
    }
});

// Evento para cambiar al modo oscuro
palanca.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    circulo.classList.toggle('prendido');
});

// Evento para mostrar/ocultar la barra lateral en modo mini
cloud.addEventListener('click', () => {
    barraLateral.classList.toggle('mini-barra-lateral');
    spans.forEach(span => {
        span.classList.toggle('oculto');
    });
});

// Evento para mostrar las opciones del usuario
opcionesUsuario.addEventListener('click', () => {
    const opcionesMenu = document.querySelector('.opciones-menu');
    opcionesMenu.classList.toggle('visible');
});

// Función para obtener eventos desde una fuente externa (ajusta según tu backend/API)
function obtenerEventos() {
    return fetch('url_de_tu_api_eventos')
        .then(response => response.json())
        .then(data => data.eventos); // Ajusta según la estructura de tu API
}

// Renderizamos todos los eventos al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    obtenerEventos().then(eventos => {
        renderizarEventos(eventos);
    });
});
