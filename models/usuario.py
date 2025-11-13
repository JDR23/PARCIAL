from sqlalchemy import Column, String
import uuid
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, nullable=False, unique=True)
    contrasena = Column(String, nullable=False)
    rol = Column(String, nullable=False)
