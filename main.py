from fastapi import FastAPI
from database import engine, Base
from routers import usuario_router

# Crear las tablas en la BD si no existen
Base.metadata.create_all(bind=engine)

# Inicializar la app
app = FastAPI(title="Parcial - Gestión de Usuarios")

# Registrar routers
app.include_router(usuario_router.router, prefix="/usuarios", tags=["Usuarios"])
