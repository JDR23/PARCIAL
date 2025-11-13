from sqlalchemy.orm import Session
from models.tipo_producto import TipoProducto
from schemas import TipoProductoCreate, TipoProductoUpdate
import uuid


class TipoProductoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_tipo_producto(self, tipo_data: TipoProductoCreate):
        nuevo_tipo = TipoProducto(
            id=str(uuid.uuid4()),
            nombre=tipo_data.nombre,
            descripcion=getattr(tipo_data, 'descripcion', None),
        )
        self.db.add(nuevo_tipo)
        self.db.commit()
        self.db.refresh(nuevo_tipo)
        return nuevo_tipo

    def obtener_tipos_producto(self, skip: int = 0, limit: int = 100):
        return self.db.query(TipoProducto).offset(skip).limit(limit).all()

    def obtener_tipo_producto_por_id(self, tipo_id: str):
        return self.db.query(TipoProducto).filter(TipoProducto.id == tipo_id).first()

    def actualizar_tipo_producto(self, tipo_id: str, tipo_data: TipoProductoUpdate):
        tipo = self.obtener_tipo_producto_por_id(tipo_id)
        if not tipo:
            return None
        update_data = tipo_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(tipo, key, value)
        self.db.commit()
        self.db.refresh(tipo)
        return tipo

    def eliminar_tipo_producto(self, tipo_id: str):
        tipo = self.obtener_tipo_producto_por_id(tipo_id)
        if not tipo:
            return None
        self.db.delete(tipo)
        self.db.commit()
        return tipo

    def buscar_tipos_producto_por_nombre(self, nombre: str):
        from sqlalchemy import func
        return self.db.query(TipoProducto).filter(
            func.lower(TipoProducto.nombre).contains(func.lower(nombre))
        ).all()
