"""
Operaciones CRUD para la entidad Cliente
"""

from typing import List, Optional

from entities.cliente import Cliente
from schemas import ClienteCreate, ClienteUpdate
from sqlalchemy.orm import Session


class ClienteCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_cliente(self, cliente_data: ClienteCreate) -> Cliente:
        """
        Crea un nuevo cliente en la base de datos.

        Args:
            cliente_data: Datos del cliente a crear.

        Returns:
            El objeto Cliente creado.
        """
        nuevo_cliente = Cliente(**cliente_data.model_dump())
        self.db.add(nuevo_cliente)
        self.db.commit()
        self.db.refresh(nuevo_cliente)
        return nuevo_cliente

    def obtener_clientes(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """
        Obtiene una lista de todos los clientes con paginación.

        Args:
            skip: Número de registros a saltar.
            limit: Número máximo de registros a devolver.

        Returns:
            Lista de objetos Cliente.
        """
        return self.db.query(Cliente).offset(skip).limit(limit).all()

    def obtener_cliente_por_id(self, cliente_id: int) -> Optional[Cliente]:
        """
        Obtiene un cliente por su ID.

        Args:
            cliente_id: ID del cliente a buscar.

        Returns:
            El objeto Cliente o None si no se encuentra.
        """
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def actualizar_cliente(
        self, cliente_id: int, cliente_data: ClienteUpdate
    ) -> Optional[Cliente]:
        """
        Actualiza un cliente existente.

        Args:
            cliente_id: ID del cliente a actualizar.
            cliente_data: Datos para actualizar.

        Returns:
            El objeto Cliente actualizado o None si no se encuentra.
        """
        cliente_db = self.obtener_cliente_por_id(cliente_id)
        if not cliente_db:
            return None

        update_data = cliente_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(cliente_db, field, value)

        self.db.commit()
        self.db.refresh(cliente_db)
        return cliente_db

    def eliminar_cliente(self, cliente_id: int) -> bool:
        """
        Elimina un cliente de la base de datos.

        Args:
            cliente_id: ID del cliente a eliminar.

        Returns:
            True si se eliminó correctamente, False en caso contrario.
        """
        cliente_db = self.obtener_cliente_por_id(cliente_id)
        if cliente_db:
            # Aquí podrías añadir lógica para manejar dependencias,
            # como facturas o carritos asociados al cliente.
            self.db.delete(cliente_db)
            self.db.commit()
            return True
        return False