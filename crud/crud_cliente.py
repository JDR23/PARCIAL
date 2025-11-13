from sqlalchemy.orm import Session
from models.cliente import Cliente
from schemas import ClienteCreate, ClienteUpdate
import uuid


class ClienteCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_cliente(self, cliente_data: ClienteCreate):
        nuevo_cliente = Cliente(
            id=str(uuid.uuid4()),
            nombre=cliente_data.nombre,
            correo=cliente_data.correo,
            telefono=getattr(cliente_data, 'telefono', None),
            direccion=getattr(cliente_data, 'direccion', None),
        )
        self.db.add(nuevo_cliente)
        self.db.commit()
        self.db.refresh(nuevo_cliente)
        return nuevo_cliente

    def obtener_clientes(self, skip: int = 0, limit: int = 100):
        return self.db.query(Cliente).offset(skip).limit(limit).all()

    def obtener_cliente_por_id(self, cliente_id: str):
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def actualizar_cliente(self, cliente_id: str, cliente_data: ClienteUpdate):
        cliente = self.obtener_cliente_por_id(cliente_id)
        if not cliente:
            return None
        update_data = cliente_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(cliente, key, value)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def eliminar_cliente(self, cliente_id: str):
        cliente = self.obtener_cliente_por_id(cliente_id)
        if not cliente:
            return None
        self.db.delete(cliente)
        self.db.commit()
        return cliente

    def buscar_clientes(self, nombre: str = None, correo: str = None):
        from sqlalchemy import func
        query = self.db.query(Cliente)
        if nombre:
            query = query.filter(func.lower(Cliente.nombre).contains(func.lower(nombre)))
        if correo:
            query = query.filter(func.lower(Cliente.correo).contains(func.lower(correo)))
        return query.all()
