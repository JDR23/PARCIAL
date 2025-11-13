from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List
from pydantic import BaseModel

app = FastAPI(title="API de Usuarios (en memoria)")

# Montar carpeta frontend como estática
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


# ---------------------------
# MODELO (Pydantic simple)
# ---------------------------
class UsuarioModel(BaseModel):
    id: int
    nombre: str
    correo: str
    contrasena: str
    rol: str


# ---------------------------
# "Base de datos" en memoria
# ---------------------------
usuarios = [
    {"id": 1, "nombre": "Juan Pérez", "correo": "juan@mail.com", "contrasena": "1234", "rol": "admin"},
    {"id": 2, "nombre": "Ana López",  "correo": "ana@mail.com",  "contrasena": "abcd", "rol": "usuario"},
]


# ---------------------------
# RUTAS API (JSON)
# ---------------------------
@app.get("/usuarios/", response_model=List[UsuarioModel])
def listar_usuarios(nombre: str = None):
    """
    Listar usuarios. Opcional: filtrado por nombre vía query param ?nombre=...
    """
    if nombre:
        q = nombre.lower()
        return [u for u in usuarios if q in u["nombre"].lower()]
    return usuarios


@app.get("/usuarios/{usuario_id}", response_model=UsuarioModel)
def obtener_usuario(usuario_id: int):
    for u in usuarios:
        if u["id"] == usuario_id:
            return u
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.post("/usuarios/", response_model=UsuarioModel)
def crear_usuario(payload: UsuarioModel):
    # verificar id único
    if any(u["id"] == payload.id for u in usuarios):
        raise HTTPException(status_code=400, detail="El ID ya existe")
    nuevo = payload.dict()
    usuarios.append(nuevo)
    return nuevo


@app.put("/usuarios/{usuario_id}", response_model=UsuarioModel)
def actualizar_usuario(usuario_id: int, payload: UsuarioModel):
    for i, u in enumerate(usuarios):
        if u["id"] == usuario_id:
            usuarios[i] = payload.dict()
            return usuarios[i]
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    global usuarios
    before = len(usuarios)
    usuarios = [u for u in usuarios if u["id"] != usuario_id]
    if len(usuarios) == before:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"ok": True, "message": "Usuario eliminado"}


# ---------------------------
# SERVIR FRONTEND
# ---------------------------
@app.get("/", include_in_schema=False)
def root():
    # devuelve el archivo estático principal
    return FileResponse("frontend/usuarios.html")
