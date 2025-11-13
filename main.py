from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión inicial a la base de datos
def crear_tabla_usuarios():
    conn = sqlite3.connect("basedatos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

crear_tabla_usuarios()

# Archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="vista")

# Ruta de inicio
@app.get("/inicio", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse("inicio.html", {"request": request})

# Ruta para login
@app.post("/login")
async def login(request: Request, nombre_usuario: str = Form(...), contrasena: str = Form(...)):
    conn = sqlite3.connect("basedatos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = ? AND contrasena = ?", (nombre_usuario, contrasena))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        rol = usuario[3]
        if rol == "admin":
            return RedirectResponse(url="/menu_admin", status_code=303)
        else:
            return RedirectResponse(url="/menu_usuario", status_code=303)
    else:
        return templates.TemplateResponse("inicio.html", {"request": request, "error": "Credenciales incorrectas"})

# Ruta menú de administrador
@app.get("/menu_admin", response_class=HTMLResponse)
async def menu_admin(request: Request):
    return templates.TemplateResponse("menu_admin.html", {"request": request, "usuario": "admin"})

# Ruta menú de usuario
@app.get("/menu_usuario", response_class=HTMLResponse)
async def menu_usuario(request: Request):
    return templates.TemplateResponse("menu_usuario.html", {"request": request, "usuario": "usuario"})

# Ruta para crear un administrador de emergencia (GET o POST)
@app.get("/crear_admin_emergencia")
@app.post("/crear_admin_emergencia")
def crear_admin_emergencia():
    conn = sqlite3.connect("basedatos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE rol = 'admin'")
    admin = cursor.fetchone()

    if admin:
        conn.close()
        return {"mensaje": "Ya existe un administrador."}

    cursor.execute(
        "INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES (?, ?, ?)",
        ("admin", "1234", "admin")
    )
    conn.commit()
    conn.close()
    return {"mensaje": "Administrador creado con éxito. Usuario: admin, Contraseña: 1234"}

# Ruta raíz
@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/inicio")
