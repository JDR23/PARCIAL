const API_URL = "http://127.0.0.1:8000/usuarios/";

const form = document.getElementById("formUsuario");
const tabla = document.getElementById("tablaUsuarios");
const btnMostrar = document.getElementById("btnMostrar");
const btnBuscar = document.getElementById("btnBuscar");
const inputBuscar = document.getElementById("inputBuscar");

let editando = false;
let idEditando = null;

// ✅ Mostrar todos los usuarios
async function mostrarUsuarios() {
    const res = await fetch(API_URL);
    const data = await res.json();

    tabla.innerHTML = "";
    data.forEach(usuario => {
        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${usuario.id}</td>
            <td>${usuario.nombre}</td>
            <td>${usuario.correo}</td>
            <td>${usuario.rol}</td>
            <td>
                <button class="btn btn-warning btn-sm" onclick="editarUsuario(${usuario.id})">Editar</button>
                <button class="btn btn-danger btn-sm" onclick="eliminarUsuario(${usuario.id})">Eliminar</button>
            </td>
        `;
        tabla.appendChild(fila);
    });
}

// ✅ Crear o actualizar usuario
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const usuario = {
        id: document.getElementById("id").value,
        nombre: document.getElementById("nombre").value,
        correo: document.getElementById("correo").value,
        contraseña: document.getElementById("contrasena").value,
        rol: document.getElementById("rol").value
    };

    let res;
    if (editando) {
        res = await fetch(API_URL + idEditando, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(usuario)
        });
        editando = false;
        idEditando = null;
    } else {
        res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(usuario)
        });
    }

    if (res.ok) {
        form.reset();
        mostrarUsuarios();
    }
});

// ✅ Editar usuario
async function editarUsuario(id) {
    const res = await fetch(API_URL + id);
    const usuario = await res.json();

    document.getElementById("id").value = usuario.id;
    document.getElementById("nombre").value = usuario.nombre;
    document.getElementById("correo").value = usuario.correo;
    document.getElementById("contrasena").value = usuario.contraseña;
    document.getElementById("rol").value = usuario.rol;

    editando = true;
    idEditando = id;
}

// ✅ Eliminar usuario
async function eliminarUsuario(id) {
    if (confirm("¿Seguro que quieres eliminar este usuario?")) {
        await fetch(API_URL + id, { method: "DELETE" });
        mostrarUsuarios();
    }
}

// ✅ Buscar usuario por nombre
btnBuscar.addEventListener("click", async () => {
    const nombre = inputBuscar.value.trim().toLowerCase();
    if (!nombre) return alert("Escribe un nombre para buscar");

    const res = await fetch(API_URL);
    const data = await res.json();
    const filtrados = data.filter(u => u.nombre.toLowerCase().includes(nombre));

    tabla.innerHTML = "";
    filtrados.forEach(usuario => {
        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${usuario.id}</td>
            <td>${usuario.nombre}</td>
            <td>${usuario.correo}</td>
            <td>${usuario.rol}</td>
            <td>
                <button class="btn btn-warning btn-sm" onclick="editarUsuario(${usuario.id})">Editar</button>
                <button class="btn btn-danger btn-sm" onclick="eliminarUsuario(${usuario.id})">Eliminar</button>
            </td>
        `;
        tabla.appendChild(fila);
    });
});

// ✅ Evento para mostrar todos los usuarios
btnMostrar.addEventListener("click", mostrarUsuarios);

// Mostrar usuarios al iniciar
mostrarUsuarios();
