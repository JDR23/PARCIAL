from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI(title="API de Usuarios")


# --- MODELO DE DATOS ---
class Usuario(BaseModel):
    id: int
    nombre: str
    apellido: str
    rol: str
    fecha_nacimiento: date


# --- "BASE DE DATOS" EN MEMORIA ---
usuarios = []

# --- ENDPOINTS CRUD ---


@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la API de Usuarios"}


# Crear un usuario
@app.post("/usuarios/", response_model=Usuario)
def crear_usuario(usuario: Usuario):
    for u in usuarios:
        if u.id == usuario.id:
            raise HTTPException(status_code=400, detail="El ID ya existe.")
    usuarios.append(usuario)
    return usuario


# Listar todos los usuarios
@app.get("/usuarios/", response_model=List[Usuario])
def listar_usuarios():
    return usuarios


# Obtener un usuario por su ID
@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int):
    for usuario in usuarios:
        if usuario.id == usuario_id:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


# Actualizar un usuario
@app.put("/usuarios/{usuario_id}", response_model=Usuario)
def actualizar_usuario(usuario_id: int, usuario_actualizado: Usuario):
    for i, usuario in enumerate(usuarios):
        if usuario.id == usuario_id:
            usuarios[i] = usuario_actualizado
            return usuario_actualizado
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


# Eliminar un usuario
@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    for i, usuario in enumerate(usuarios):
        if usuario.id == usuario_id:
            usuarios.pop(i)
            return {"mensaje": f"Usuario con ID {usuario_id} eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
