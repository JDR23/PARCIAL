from sqlalchemy.orm import Session
from entities.cliente import Cliente
from schemas import ClienteCreate, ClienteUpdate


def crear_cliente(db: Session, cliente: ClienteCreate):
    nuevo_cliente = Cliente(**cliente.model_dump())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


def listar_clientes(db: Session):
    return db.query(Cliente).all()


def actualizar_cliente(db: Session, cliente_id: int, cliente: ClienteUpdate):
    cliente_db = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente_db:
        for key, value in cliente.model_dump().items():
            setattr(cliente_db, key, value)
        db.commit()
        db.refresh(cliente_db)
    return cliente_db


def eliminar_cliente(db: Session, cliente_id: int):
    cliente_db = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente_db:
        db.delete(cliente_db)
        db.commit()
    return cliente_db
