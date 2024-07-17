const registerButton = document.getElementById("register");
const loginButton = document.getElementById("login");
const container = document.getElementById("container");

registerButton.addEventListener("click", () => {
  container.classList.add("right-panel-active");
});

loginButton.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
});

function togglePassword(fieldId) {
  const field = document.getElementById(fieldId);
  if (field.type === "password") {
    field.type = "text";
  } else {
    field.type = "password";
  }
}

// JavaScript para mostrar y ocultar el contenedor de mensajes flash
document.addEventListener('DOMContentLoaded', function() {
  const flashMessages = document.querySelector('.flash-messages');
  const messages = flashMessages.querySelectorAll('li');

  // Verificar si hay mensajes para mostrar
  if (messages.length > 0) {
      flashMessages.classList.add('active'); // Mostrar el contenedor
  } else {
      flashMessages.classList.remove('active'); // Ocultar el contenedor si no hay mensajes
  }
});

function closeFlashMessage(button) {
  // Encuentra el elemento li padre del botón y lo elimina
  const li = button.parentElement;
  li.remove();
}
