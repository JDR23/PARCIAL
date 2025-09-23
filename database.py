from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cambia la URL a tu BD (ej: PostgreSQL, SQLite, etc.)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# Para PostgreSQL sería algo así:
# SQLALCHEMY_DATABASE_URL = "postgresql://usuario:password@localhost:5432/tu_basedatos"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
    ),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
