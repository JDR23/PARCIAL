from sqlalchemy.orm import Session
from models.factura import Factura
import uuid


def get_facturas(db: Session):
    return db.query(Factura).all()


def get_factura(db: Session, factura_id: str):
    return db.query(Factura).filter(Factura.id == factura_id).first()


def create_factura(db: Session, factura_data):
    nueva_factura = Factura(
        id=str(uuid.uuid4()),
        cliente_id=factura_data.cliente_id,
        total=factura_data.total,
    )
    db.add(nueva_factura)
    db.commit()
    db.refresh(nueva_factura)
    return nueva_factura


def update_factura(db: Session, factura_id: str, factura_data):
    factura = get_factura(db, factura_id)
    if not factura:
        return None
    for key, value in factura_data.dict(exclude_unset=True).items():
        setattr(factura, key, value)
    db.commit()
    db.refresh(factura)
    return factura


def delete_factura(db: Session, factura_id: str):
    factura = get_factura(db, factura_id)
    if not factura:
        return None
    db.delete(factura)
    db.commit()
    return factura
