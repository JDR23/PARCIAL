"""
Operaciones CRUD para Carrito
"""

from typing import List, Optional
from uuid import UUID

from entities.carrito import Carrito
from sqlalchemy.orm import Session


class CarritoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def agregar_al_carrito(
        self,
        id_producto: int,
        id_cliente: str,
        id_cliente_creacion: Optional[str] = None,
    ) -> Carrito:
        """
        Agrega un producto al carrito de un cliente.

        Args:
            id_producto: ID del producto a agregar.
            id_cliente: ID del cliente (UUID como string).
            id_cliente_creacion: ID del cliente que realiza la operación.

        Returns:
            El item del carrito creado.
        """
        if id_cliente_creacion is None:
            id_cliente_creacion = id_cliente

        item_carrito = Carrito(
            id_producto=id_producto,
            id_cliente=id_cliente,
            id_cliente_creacion=id_cliente_creacion,
        )
        self.db.add(item_carrito)
        self.db.commit()
        self.db.refresh(item_carrito)
        return item_carrito

    def obtener_carrito_por_cliente(self, id_cliente: str) -> List[Carrito]:
        """
        Obtiene todos los items del carrito para un cliente específico.

        Args:
            id_cliente: ID del cliente (UUID como string).

        Returns:
            Lista de items en el carrito.
        """
        return self.db.query(Carrito).filter(Carrito.id_cliente == id_cliente).all()

    def obtener_item_carrito(self, id_carrito: int) -> Optional[Carrito]:
        """
        Obtiene un item específico del carrito por su ID.

        Args:
            id_carrito: ID del item del carrito.

        Returns:
            El item del carrito o None si no se encuentra.
        """
        return self.db.query(Carrito).filter(Carrito.id_carrito == id_carrito).first()

    def eliminar_item_carrito(self, id_carrito: int) -> bool:
        """
        Elimina un item del carrito.

        Args:
            id_carrito: ID del item del carrito a eliminar.

        Returns:
            True si se eliminó, False en caso contrario.
        """
        item_carrito = self.obtener_item_carrito(id_carrito)
        if item_carrito:
            self.db.delete(item_carrito)
            self.db.commit()
            return True
        return False

    def vaciar_carrito_cliente(self, id_cliente: str) -> int:
        """
        Elimina todos los items del carrito de un cliente.

        Args:
            id_cliente: ID del cliente (UUID como string).

        Returns:
            El número de items eliminados.
        """
        items_eliminados = (
            self.db.query(Carrito).filter(Carrito.id_cliente == id_cliente).delete()
        )
        self.db.commit()
        return items_eliminados