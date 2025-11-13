const fetch = require("node-fetch"); // si es Node.js, instalar con npm i node-fetch

async function recuperarAdmin() {
    const admin = {
        username: "admin",               // nombre de usuario que quieras
        correo: "admin@correo.com",      // correo que recuerdes o uno nuevo
        password: "admin123",            // contraseña temporal
        rol: "admin"
    };

    try {
        const respuesta = await fetch("http://127.0.0.1:8000/usuarios/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(admin)
        });

        if (respuesta.ok) {
            console.log("✅ Admin creado o actualizado correctamente");
        } else {
            const error = await respuesta.json();
            console.log("❌ Error:", error);
        }
    } catch (error) {
        console.error("Error al conectarse al backend:", error);
    }
}

recuperarAdmin();

