from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import usuario_router, cliente, producto, tipo_producto, carrito, factura
import uuid

# Crear las tablas de la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Tienda Online",
    description="API REST para gestión de tienda online",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar carpeta frontend como estática
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Incluir routers
app.include_router(usuario_router.router)
app.include_router(cliente.router)
app.include_router(producto.router)
app.include_router(tipo_producto.router)
app.include_router(carrito.router)
app.include_router(factura.router)


# Crear usuario admin por defecto si no existe ninguno
@app.on_event("startup")
async def crear_admin_inicial():
    from database.config import SessionLocal
    from models.usuario import Usuario
    db = SessionLocal()
    try:
        # Verificar si ya existe algún usuario
        usuarios_existentes = db.query(Usuario).count()
        if usuarios_existentes == 0:
            # Crear admin inicial
            admin_inicial = Usuario(
                id=str(uuid.uuid4()),
                nombre="Administrador",
                correo="admin@tienda.com",
                contrasena="admin123",
                rol="admin"
            )
            db.add(admin_inicial)
            db.commit()
            print("[INFO] Usuario administrador inicial creado: admin@tienda.com / admin123")
    except Exception as e:
        print(f"[ERROR] Error al crear admin inicial: {e}")
    finally:
        db.close()

# Ruta raíz - servir el frontend
@app.get("/", include_in_schema=False)
def root():
    return FileResponse("frontend/index.html")
