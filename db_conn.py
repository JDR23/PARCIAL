# Este archivo está deprecado. Por favor usa database.py o database.config en su lugar.
# Se mantiene solo para compatibilidad con código existente.

from database.config import Base, engine, get_db, SessionLocal

__all__ = ["Base", "engine", "get_db", "SessionLocal"]
