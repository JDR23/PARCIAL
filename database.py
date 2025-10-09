from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -------------------------------------------------------------------
# Configuración de la base de datos
# -------------------------------------------------------------------

# Cambia 'usuarios.db' por el nombre de tu base si es diferente
DATABASE_URL = "sqlite:///./usuarios.db"

# Crear el motor de conexión
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de modelos
Base = declarative_base()


# -------------------------------------------------------------------
# Dependencia que devuelve una sesión de base de datos
# -------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
