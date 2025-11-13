# Importar desde database.config para mantener compatibilidad
from database.config import Base, engine, get_db, SessionLocal

# Re-exportar para compatibilidad con imports directos desde database
__all__ = ["Base", "engine", "get_db", "SessionLocal"]

