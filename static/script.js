// --- FUNCIONES DE VALIDACIÓN ---
function validar_inputs() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    if (username === "" || password === "") {
        alert("Porfavor ingrese sus credenciales");
        return false;
    }
    return true;
}

function validar_inputs_reg() {
    const usuario = document.getElementById("usuario").value;
    const username = document.getElementById("username_register").value;
    const password = document.getElementById("password_register").value;
    if (username === "" || password === "" || usuario === "") {
        alert("Porfavor ingrese sus credenciales");
        return false;
    }
    return true;
}

// --- LÓGICA DEL MENÚ Y OVERLAY ---
const menuBtn = document.querySelector('#mobile-menu');
const navList = document.querySelector('#nav-list');
const overlay = document.querySelector('#overlay');

// Función única para abrir/cerrar
const toggleMenu = () => {
    menuBtn.classList.toggle('is-active');
    navList.classList.toggle('active');
    overlay.classList.toggle('active');

    // Evita que el fondo se mueva cuando el menú está abierto
    if (navList.classList.contains('active')) {
        document.body.style.overflow = 'hidden';
    } else {
        document.body.style.overflow = 'auto';
    }
};

// Eventos
menuBtn.addEventListener('click', toggleMenu);
overlay.addEventListener('click', toggleMenu);

// Cerrar si se hace clic en un link del menú
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        if (navList.classList.contains('active')) toggleMenu();
    });
});