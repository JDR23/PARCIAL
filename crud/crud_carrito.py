from sqlalchemy.orm import Session
from models.carrito import Carrito
import uuid


def get_carritos(db: Session):
    return db.query(Carrito).all()


def get_carrito(db: Session, carrito_id: str):
    return db.query(Carrito).filter(Carrito.id == carrito_id).first()


def create_carrito(db: Session, carrito_data):
    nuevo_carrito = Carrito(
        id=str(uuid.uuid4()),
        usuario_id=carrito_data.usuario_id,
        producto_id=carrito_data.producto_id,
        cantidad=carrito_data.cantidad,
    )
    db.add(nuevo_carrito)
    db.commit()
    db.refresh(nuevo_carrito)
    return nuevo_carrito


def update_carrito(db: Session, carrito_id: str, carrito_data):
    carrito = get_carrito(db, carrito_id)
    if not carrito:
        return None
    for key, value in carrito_data.dict(exclude_unset=True).items():
        setattr(carrito, key, value)
    db.commit()
    db.refresh(carrito)
    return carrito


def delete_carrito(db: Session, carrito_id: str):
    carrito = get_carrito(db, carrito_id)
    if not carrito:
        return None
    db.delete(carrito)
    db.commit()
    return carrito
