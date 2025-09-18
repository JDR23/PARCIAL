from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 👇 Tu cadena de conexión adaptada para SQLAlchemy
DATABASE_URL = "postgresql://neondb_owner:npg_nDTfmNS5cxJ9@ep-blue-star-adunfkf2-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Crear el engine
engine = create_engine(DATABASE_URL)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para heredar en tus entidades
Base = declarative_base()


# Dependencia para obtener sesión en el código
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
