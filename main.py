from fastapi import FastAPI
from database import Base, engine
from routers import usuario_router

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="Parcial 1 - API",
    description="Aplicativo de ejemplo con FastAPI, SQLAlchemy y Pydantic",
    version="1.0.0",
)

# Incluir routers (ya tienen prefix y tags definidos en usuario_router.py)
app.include_router(usuario_router.router)


# Ruta raíz
@app.get("/")
def root():
    return {"mensaje": "Aplicativo corriendo correctamente"}
