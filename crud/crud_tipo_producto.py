"""
Operaciones CRUD para la entidad TipoProducto
"""

from typing import List, Optional

from entities.tipo_producto import TipoProducto
from schemas import TipoProductoCreate, TipoProductoUpdate
from sqlalchemy.orm import Session


class TipoProductoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_tipo_producto(
        self, tipo_producto_data: TipoProductoCreate
    ) -> TipoProducto:
        """
        Crea un nuevo tipo de producto.
        """
        if not tipo_producto_data.nombre_categoria.strip():
            raise ValueError("El nombre de la categoría no puede estar vacío.")

        nuevo_tipo = TipoProducto(**tipo_producto_data.model_dump())
        self.db.add(nuevo_tipo)
        self.db.commit()
        self.db.refresh(nuevo_tipo)
        return nuevo_tipo

    def obtener_tipos_producto(
        self, skip: int = 0, limit: int = 100
    ) -> List[TipoProducto]:
        """
        Obtiene una lista de todos los tipos de producto.
        """
        return self.db.query(TipoProducto).offset(skip).limit(limit).all()

    def obtener_tipo_producto_por_id(
        self, tipo_producto_id: int
    ) -> Optional[TipoProducto]:
        """
        Obtiene un tipo de producto por su ID.
        """
        return (
            self.db.query(TipoProducto)
            .filter(TipoProducto.id_tipo_producto == tipo_producto_id)
            .first()
        )

    def actualizar_tipo_producto(
        self, tipo_producto_id: int, tipo_producto_data: TipoProductoUpdate
    ) -> Optional[TipoProducto]:
        """
        Actualiza un tipo de producto existente.
        """
        tipo_db = self.obtener_tipo_producto_por_id(tipo_producto_id)
        if not tipo_db:
            return None

        update_data = tipo_producto_data.model_dump(exclude_unset=True)

        if "nombre_categoria" in update_data and not update_data[
            "nombre_categoria"
        ].strip():
            raise ValueError("El nombre de la categoría no puede estar vacío.")

        for field, value in update_data.items():
            setattr(tipo_db, field, value)

        self.db.commit()
        self.db.refresh(tipo_db)
        return tipo_db

    def eliminar_tipo_producto(self, tipo_producto_id: int) -> bool:
        """
        Elimina un tipo de producto.
        """
        tipo_db = self.obtener_tipo_producto_por_id(tipo_producto_id)
        if tipo_db:
            # Aquí podrías añadir una validación para no eliminar
            # si hay productos asociados a este tipo.
            self.db.delete(tipo_db)
            self.db.commit()
            return True
        return False