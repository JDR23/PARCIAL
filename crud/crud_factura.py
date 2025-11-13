from sqlalchemy.orm import Session
from models.factura import Factura
from schemas import FacturaCreate
import uuid


class FacturaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_factura(self, factura_data: FacturaCreate):
        nueva_factura = Factura(
            id=str(uuid.uuid4()),
            cliente_id=factura_data.cliente_id,
            total=factura_data.total,
        )
        self.db.add(nueva_factura)
        self.db.commit()
        self.db.refresh(nueva_factura)
        return nueva_factura

    def obtener_factura(self, factura_id: str):
        return self.db.query(Factura).filter(Factura.id == factura_id).first()

    def obtener_facturas_por_cliente(self, cliente_id: str):
        return self.db.query(Factura).filter(Factura.cliente_id == cliente_id).all()

    def obtener_facturas(self, skip: int = 0, limit: int = 100):
        return self.db.query(Factura).offset(skip).limit(limit).all()
