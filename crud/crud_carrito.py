from sqlalchemy.orm import Session
from models.carrito import Carrito
from schemas import CarritoCreate
import uuid


class CarritoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def agregar_al_carrito(self, carrito_data: CarritoCreate):
        nuevo_carrito = Carrito(
            id=str(uuid.uuid4()),
            usuario_id=carrito_data.usuario_id,
            producto_id=carrito_data.producto_id,
            cantidad=carrito_data.cantidad,
        )
        self.db.add(nuevo_carrito)
        self.db.commit()
        self.db.refresh(nuevo_carrito)
        return nuevo_carrito

    def obtener_carrito_por_usuario(self, usuario_id: str):
        return self.db.query(Carrito).filter(Carrito.usuario_id == usuario_id).all()

    def obtener_item_carrito(self, carrito_id: str):
        return self.db.query(Carrito).filter(Carrito.id == carrito_id).first()

    def eliminar_item_carrito(self, carrito_id: str):
        carrito = self.obtener_item_carrito(carrito_id)
        if not carrito:
            return None
        self.db.delete(carrito)
        self.db.commit()
        return carrito

    def vaciar_carrito_usuario(self, usuario_id: str):
        items = self.obtener_carrito_por_usuario(usuario_id)
        count = len(items)
        for item in items:
            self.db.delete(item)
        self.db.commit()
        return count
