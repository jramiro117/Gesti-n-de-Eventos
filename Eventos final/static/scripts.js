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
const usuarioContainer = document.querySelector('.usuario-container'); // Contenedor donde se mostrará la información del usuario

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

// Función para mostrar la información del usuario en la barra lateral
function mostrarInfoUsuario() {
    fetch('/obtener_usuario')
        .then(response => response.json())
        .then(data => {
            const infoUsuarioHTML = `
                <div class="info-usuario">
                    <img src="${data.usuario.foto}" alt="Foto de Usuario">
                    <div class="nombre-email">
                        <div class="nombre">${data.usuario.nombre}</div>
                        <div class="email">${data.usuario.email}</div>
                    </div>
                </div>
            `;
            usuarioContainer.innerHTML = infoUsuarioHTML; // Mostramos la información del usuario
        })
        .catch(error => {
            console.error('Error al obtener datos del usuario:', error);
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
    return fetch('/obtener_eventos')
        .then(response => response.json())
        .then(data => data.eventos); // Ajusta según la estructura de tu API
}

// Renderizamos todos los eventos al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    mostrarInfoUsuario(); // Mostramos la información del usuario al cargar la página
    obtenerEventos().then(eventos => {
        renderizarEventos(eventos);
    });
});

// Evento para enviar el formulario de perfil por AJAX
document.addEventListener('DOMContentLoaded', function() {
    const formPerfil = document.querySelector('#formPerfil');

    if (formPerfil) {
        formPerfil.addEventListener('submit', function(event) {
            event.preventDefault(); // Evitar el envío del formulario por defecto

            // Lógica para enviar el formulario por AJAX
            enviarFormularioPerfil();
        });
    }
});

// Función para enviar el formulario de perfil por AJAX
function enviarFormularioPerfil() {
    const formPerfil = document.querySelector('#formPerfil');
    const formData = new FormData(formPerfil);

    fetch('/editar_perfil', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Manejar la respuesta del servidor (por ejemplo, mostrar mensajes de éxito o error)
        console.log(data);
        // Actualizar la interfaz de usuario si es necesario
        if (data.success) {
            alert('Perfil actualizado correctamente.');
            // Puedes agregar aquí lógica adicional para actualizar la interfaz de usuario si es necesario
        } else {
            alert('Hubo un error al actualizar el perfil.');
        }
    })
    .catch(error => {
        console.error('Error al enviar el formulario:', error);
        alert('Error al actualizar el perfil.');
    });
}
