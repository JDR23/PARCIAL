const API_URL = "http://127.0.0.1:8000/usuarios/";

const form = document.getElementById("formUsuario");
const tabla = document.getElementById("tablaUsuarios");

// Listar usuarios
async function listarUsuarios() {
    const res = await fetch(API_URL);
    const data = await res.json();
    tabla.innerHTML = "";
    data.forEach(u => {
        tabla.innerHTML += `
            <tr>
                <td>${u.nombre}</td>
                <td>${u.correo}</td>
                <td>${u.rol}</td>
                <td>
                    <button class="btn btn-sm btn-warning" onclick="editarUsuario('${u.id}', '${u.nombre}', '${u.correo}', '${u.rol}')">Editar</button>
                    <button class="btn btn-sm btn-danger" onclick="eliminarUsuario('${u.id}')">Eliminar</button>
                </td>
            </tr>
        `;
    });
}

// Crear o actualizar
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const usuario = {
        nombre: document.getElementById("nombre").value,
        correo: document.getElementById("correo").value,
        rol: document.getElementById("rol").value
    };
    const id = document.getElementById("usuario_id").value;
    const method = id ? "PUT" : "POST";
    const url = id ? `${API_URL}${id}` : API_URL;

    await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(usuario)
    });
    form.reset();
    listarUsuarios();
});

// Editar
function editarUsuario(id, nombre, correo, rol) {
    document.getElementById("usuario_id").value = id;
    document.getElementById("nombre").value = nombre;
    document.getElementById("correo").value = correo;
    document.getElementById("rol").value = rol;
}

// Eliminar
async function eliminarUsuario(id) {
    if (confirm("¿Seguro que deseas eliminar este usuario?")) {
        await fetch(`${API_URL}${id}`, { method: "DELETE" });
        listarUsuarios();
    }
}

listarUsuarios();
