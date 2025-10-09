from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexión a tu base de datos PostgreSQL
DATABASE_URL = (
    "postgresql+psycopg2://postgres:tu_contraseña@localhost:5432/tu_basededatos"
)

# Crear el motor
engine = create_engine(DATABASE_URL)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarar la base de datos
Base = declarative_base()


# Esta es la función que te falta 👇
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
