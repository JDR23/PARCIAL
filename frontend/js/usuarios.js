// ======================
// CONFIGURACIÓN GENERAL
// ======================
const API_URL = "http://127.0.0.1:8000/usuarios/";
const LOGIN_URL = "http://127.0.0.1:8000/login";

// ======================
// VERIFICAR SESIÓN ACTIVA
// ======================
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");
    const formUsuario = document.getElementById("formUsuario");
    const loginForm = document.getElementById("loginForm");

    // Si estamos en usuarios.html y no hay token, redirigimos al login
    if (formUsuario && !token) {
        alert("⚠️ Debes iniciar sesión primero.");
        window.location.href = "index.html";
        return;
    }

    // Si estamos en el login.html (index.html) y hay token, redirigimos a usuarios.html
    if (loginForm && token) {
        window.location.href = "usuarios.html";
        return;
    }

    // Si estamos en login.html, escuchar el envío del formulario
    if (loginForm) {
        loginForm.addEventListener("submit", manejarLogin);
    }

    // Si estamos en usuarios.html y hay token, cargar los usuarios
    if (formUsuario && token) {
        cargarUsuarios();

        // Asignar el evento de agregar usuario
        formUsuario.addEventListener("submit", manejarAgregarUsuario);

        // Asignar el evento de cerrar sesión
        const btnCerrar = document.getElementById("cerrarSesion");
        if (btnCerrar) btnCerrar.addEventListener("click", cerrarSesion);
    }
});

// ======================
// FUNCIÓN DE LOGIN
// ======================
async function manejarLogin(e) {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!username || !password) {
        alert("⚠️ Completa todos los campos");
        return;
    }

    try {
        const respuesta = await fetch(LOGIN_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        if (!respuesta.ok) {
            alert("❌ Credenciales incorrectas");
            return;
        }

        const data = await respuesta.json();
        localStorage.setItem("token", data.access_token);
        alert("✅ Inicio de sesión exitoso");
        window.location.href = "usuarios.html";
    } catch (error) {
        console.error("Error al iniciar sesión:", error);
        alert("❌ Error de conexión con el servidor");
    }
}

// ======================
// CARGAR USUARIOS
// ======================
async function cargarUsuarios() {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
        const respuesta = await fetch(API_URL, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (respuesta.status === 401) {
            alert("⚠️ Sesión expirada. Vuelve a iniciar sesión.");
            localStorage.removeItem("token");
            window.location.href = "index.html";
            return;
        }

        if (!respuesta.ok) throw new Error("Error al cargar usuarios");

        const usuarios = await respuesta.json();
        mostrarUsuarios(usuarios);
    } catch (error) {
        console.error("Error:", error);
        alert("❌ No se pudieron cargar los usuarios");
    }
}

// ======================
// MOSTRAR USUARIOS EN TABLA
// ======================
function mostrarUsuarios(usuarios) {
    const tabla = document.getElementById("tablaUsuarios");
    if (!tabla) return;

    tabla.innerHTML = "";

    usuarios.forEach(usuario => {
        const fila = `
            <tr>
                <td>${usuario.id}</td>
                <td>${usuario.nombre}</td>
                <td>${usuario.correo}</td>
                <td>${usuario.contraseña}</td>
                <td>${usuario.rol}</td>
                <td>
                    <button class="btn btn-danger btn-sm" onclick="eliminarUsuario(${usuario.id})">🗑️ Eliminar</button>
                </td>
            </tr>
        `;
        tabla.innerHTML += fila;
    });
}

// ======================
// AGREGAR USUARIO
// ======================
async function manejarAgregarUsuario(e) {
    e.preventDefault();

    const token = localStorage.getItem("token");
    if (!token) {
        alert("⚠️ No hay sesión activa. Inicia sesión.");
        window.location.href = "index.html";
        return;
    }

    const usuario = {
        id: parseInt(document.getElementById("id").value),
        nombre: document.getElementById("nombre").value,
        correo: document.getElementById("correo").value,
        contraseña: document.getElementById("contraseña").value,
        rol: document.getElementById("rol").value
    };

    try {
        const respuesta = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(usuario)
        });

        if (respuesta.ok) {
            alert("✅ Usuario agregado correctamente");
            e.target.reset();
            cargarUsuarios();
        } else {
            const error = await respuesta.json();
            alert("❌ Error: " + (error.detail || "No autorizado"));
        }
    } catch (error) {
        console.error("Error:", error);
        alert("❌ No se pudo agregar el usuario");
    }
}

// ======================
// ELIMINAR USUARIO
// ======================
async function eliminarUsuario(id) {
    const token = localStorage.getItem("token");
    if (!confirm("¿Seguro que deseas eliminar este usuario?")) return;

    try {
        const respuesta = await fetch(API_URL + id, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (respuesta.ok) {
            alert("🗑️ Usuario eliminado correctamente");
            cargarUsuarios();
        } else {
            alert("❌ Error al eliminar usuario");
        }
    } catch (error) {
        console.error(error);
        alert("Error al eliminar usuario");
    }
}

// ======================
// CERRAR SESIÓN
// ======================
function cerrarSesion() {
    localStorage.removeItem("token");
    alert("👋 Sesión cerrada correctamente");
    window.location.href = "index.html";
}
