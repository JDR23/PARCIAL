from sqlalchemy.orm import Session
from models.cliente import Cliente
import uuid


def get_clientes(db: Session):
    return db.query(Cliente).all()


def get_cliente(db: Session, cliente_id: str):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()


def create_cliente(db: Session, cliente_data):
    nuevo_cliente = Cliente(
        id=str(uuid.uuid4()),
        nombre=cliente_data.nombre,
        correo=cliente_data.correo,
        telefono=cliente_data.telefono,
    )
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


def update_cliente(db: Session, cliente_id: str, cliente_data):
    cliente = get_cliente(db, cliente_id)
    if not cliente:
        return None
    for key, value in cliente_data.dict(exclude_unset=True).items():
        setattr(cliente, key, value)
    db.commit()
    db.refresh(cliente)
    return cliente


def delete_cliente(db: Session, cliente_id: str):
    cliente = get_cliente(db, cliente_id)
    if not cliente:
        return None
    db.delete(cliente)
    db.commit()
    return cliente
