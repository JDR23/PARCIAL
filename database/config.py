from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Obtener la URL de la base de datos desde variables de entorno
# Si no existe, usar SQLite local por defecto (solo para desarrollo)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Si no hay DATABASE_URL configurada, usar SQLite local
    DATABASE_URL = "sqlite:///./test.db"
    print("[INFO] DATABASE_URL no configurada. Usando SQLite local (test.db)")
    print("[INFO] Para usar Neon PostgreSQL, crea un archivo .env con DATABASE_URL")
else:
    db_name = DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else 'SQLite'
    print(f"[INFO] Usando base de datos: {db_name}")

# Configurar el motor de base de datos
if DATABASE_URL.startswith("sqlite"):
    # Configuración para SQLite
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        echo=False
    )
elif DATABASE_URL.startswith("postgresql"):
    # Configuración para PostgreSQL (Neon)
    # Asegurar que tenga SSL si es necesario
    if "sslmode" not in DATABASE_URL:
        if "?" in DATABASE_URL:
            DATABASE_URL += "&sslmode=require"
        else:
            DATABASE_URL += "?sslmode=require"
    
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,  # Verificar conexiones antes de usarlas
        pool_recycle=300,     # Reciclar conexiones cada 5 minutos
    )
else:
    # Para otros tipos de base de datos
    engine = create_engine(DATABASE_URL, echo=False)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarar la base de datos
Base = declarative_base()


# Función para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

