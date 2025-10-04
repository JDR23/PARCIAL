"""
Operaciones CRUD para Producto
"""

from typing import List, Optional

from entities.producto import Producto
from schemas import ProductoCreate, ProductoUpdate
from sqlalchemy.orm import Session


class ProductoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_producto(self, producto_data: ProductoCreate) -> Producto:
        """
        Crea un nuevo producto.

        Args:
            producto_data: Datos del producto a crear.

        Returns:
            El objeto Producto creado.

        Raises:
            ValueError: Si los datos de entrada no son válidos.
        """
        if producto_data.precio <= 0:
            raise ValueError("El precio debe ser un número positivo.")
        if producto_data.stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        # Aquí podrías añadir una validación para asegurar que `categoria_id` existe.

        nuevo_producto = Producto(**producto_data.model_dump())
        self.db.add(nuevo_producto)
        self.db.commit()
        self.db.refresh(nuevo_producto)
        return nuevo_producto

    def obtener_producto(self, producto_id: int) -> Optional[Producto]:
        """
        Obtiene un producto por su ID.

        Args:
            producto_id: ID del producto.

        Returns:
            El objeto Producto o None si no se encuentra.
        """
        return self.db.query(Producto).filter(Producto.id == producto_id).first()

    def obtener_productos(self, skip: int = 0, limit: int = 100) -> List[Producto]:
        """
        Obtiene una lista de productos con paginación.

        Args:
            skip: Número de registros a saltar.
            limit: Número máximo de registros a devolver.

        Returns:
            Lista de objetos Producto.
        """
        return self.db.query(Producto).offset(skip).limit(limit).all()

    def buscar_productos_por_nombre(self, nombre: str) -> List[Producto]:
        """
        Busca productos cuyo nombre contenga el texto proporcionado.

        Args:
            nombre: Texto a buscar en el nombre del producto.

        Returns:
            Lista de productos que coinciden con la búsqueda.
        """
        return self.db.query(Producto).filter(Producto.nombre.ilike(f"%{nombre}%")).all()

    def actualizar_producto(
        self, producto_id: int, producto_data: ProductoUpdate
    ) -> Optional[Producto]:
        """
        Actualiza un producto existente.

        Args:
            producto_id: ID del producto a actualizar.
            producto_data: Datos para actualizar.

        Returns:
            El objeto Producto actualizado o None si no se encuentra.
        """
        producto_db = self.obtener_producto(producto_id)
        if not producto_db:
            return None

        update_data = producto_data.model_dump(exclude_unset=True)

        if "precio" in update_data and update_data["precio"] <= 0:
            raise ValueError("El precio debe ser un número positivo.")
        if "stock" in update_data and update_data["stock"] < 0:
            raise ValueError("El stock no puede ser negativo.")

        for field, value in update_data.items():
            setattr(producto_db, field, value)

        self.db.commit()
        self.db.refresh(producto_db)
        return producto_db

    def actualizar_stock(self, producto_id: int, nuevo_stock: int) -> Optional[Producto]:
        """
        Actualiza únicamente el stock de un producto.

        Args:
            producto_id: ID del producto.
            nuevo_stock: Nueva cantidad de stock.

        Returns:
            El objeto Producto actualizado o None si no se encuentra.
        """
        producto_db = self.obtener_producto(producto_id)
        if not producto_db:
            return None
        if nuevo_stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        producto_db.stock = nuevo_stock
        self.db.commit()
        self.db.refresh(producto_db)
        return producto_db

    def eliminar_producto(self, producto_id: int) -> bool:
        """
        Elimina un producto de la base de datos.

        Args:
            producto_id: ID del producto a eliminar.

        Returns:
            True si se eliminó correctamente, False en caso contrario.
        """
        producto_db = self.obtener_producto(producto_id)
        if producto_db:
            self.db.delete(producto_db)
            self.db.commit()
            return True
        return False