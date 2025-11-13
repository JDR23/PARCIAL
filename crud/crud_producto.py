from sqlalchemy.orm import Session
from sqlalchemy import func
from models.producto import Producto
from schemas import ProductoCreate, ProductoUpdate
import uuid


class ProductoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_producto(self, producto_data: ProductoCreate):
        nuevo_producto = Producto(
            id=str(uuid.uuid4()),
            nombre=producto_data.nombre,
            descripcion=getattr(producto_data, 'descripcion', None),
            precio=producto_data.precio,
            stock=getattr(producto_data, 'stock', 0),
        )
        self.db.add(nuevo_producto)
        self.db.commit()
        self.db.refresh(nuevo_producto)
        return nuevo_producto

    def obtener_productos(self, skip: int = 0, limit: int = 100):
        return self.db.query(Producto).offset(skip).limit(limit).all()

    def obtener_producto(self, producto_id: str):
        return self.db.query(Producto).filter(Producto.id == producto_id).first()

    def buscar_productos_por_nombre(self, nombre: str):
        # Usar func.lower para compatibilidad con SQLite y PostgreSQL
        return self.db.query(Producto).filter(
            func.lower(Producto.nombre).contains(func.lower(nombre))
        ).all()

    def actualizar_producto(self, producto_id: str, producto_data: ProductoUpdate):
        producto = self.obtener_producto(producto_id)
        if not producto:
            return None
        update_data = producto_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(producto, key, value)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def eliminar_producto(self, producto_id: str):
        producto = self.obtener_producto(producto_id)
        if not producto:
            return None
        self.db.delete(producto)
        self.db.commit()
        return producto
