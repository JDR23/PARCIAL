from sqlalchemy.orm import Session
from models.producto import Producto
import uuid


def get_productos(db: Session):
    return db.query(Producto).all()


def get_producto(db: Session, producto_id: str):
    return db.query(Producto).filter(Producto.id == producto_id).first()


def create_producto(db: Session, producto_data):
    nuevo_producto = Producto(
        id=str(uuid.uuid4()),
        nombre=producto_data.nombre,
        descripcion=producto_data.descripcion,
        precio=producto_data.precio,
        tipo_id=producto_data.tipo_id,
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto


def update_producto(db: Session, producto_id: str, producto_data):
    producto = get_producto(db, producto_id)
    if not producto:
        return None
    for key, value in producto_data.dict(exclude_unset=True).items():
        setattr(producto, key, value)
    db.commit()
    db.refresh(producto)
    return producto


def delete_producto(db: Session, producto_id: str):
    producto = get_producto(db, producto_id)
    if not producto:
        return None
    db.delete(producto)
    db.commit()
    return producto
