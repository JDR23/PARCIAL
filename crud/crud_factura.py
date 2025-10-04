"""
Operaciones CRUD para Factura y DetalleFactura
"""

from typing import List, Optional

from crud.crud_carrito import CarritoCRUD
from crud.crud_producto import ProductoCRUD
from entities.factura import DetalleFactura, Factura, FacturaCreate
from entities.producto import Producto
from sqlalchemy.orm import Session


class FacturaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_factura(self, factura_data: FacturaCreate) -> Factura:
        """
        Crea una nueva factura, sus detalles, actualiza el stock y vacía el carrito.

        Args:
            factura_data: Datos para la creación de la factura y sus detalles.

        Returns:
            La factura creada.

        Raises:
            ValueError: Si un producto no existe o no hay suficiente stock.
        """
        # 1. Calcular el total y verificar stock
        total_calculado = 0
        producto_crud = ProductoCRUD(self.db)

        for detalle in factura_data.detalles:
            producto_db: Optional[Producto] = producto_crud.obtener_producto(
                detalle.id_producto
            )
            if not producto_db:
                raise ValueError(f"El producto con ID {detalle.id_producto} no existe.")
            if producto_db.stock < detalle.cantidad:
                raise ValueError(
                    f"No hay suficiente stock para el producto '{producto_db.nombre}'. "
                    f"Stock disponible: {producto_db.stock}, Cantidad solicitada: {detalle.cantidad}"
                )
            total_calculado += detalle.cantidad * producto_db.precio

        # 2. Crear la factura principal
        db_factura = Factura(
            id_cliente=str(factura_data.id_cliente), total=total_calculado
        )
        self.db.add(db_factura)
        self.db.flush()  # Para obtener el id_factura generado por la BD

        # 3. Crear los detalles de la factura y actualizar stock
        for detalle in factura_data.detalles:
            producto_db = producto_crud.obtener_producto(detalle.id_producto)
            # Crear detalle
            db_detalle = DetalleFactura(
                id_factura=db_factura.id_factura,
                id_producto=detalle.id_producto,
                cantidad=detalle.cantidad,
                precio_unitario=producto_db.precio,
            )
            self.db.add(db_detalle)

            # Actualizar stock
            nuevo_stock = producto_db.stock - detalle.cantidad
            producto_crud.actualizar_stock(
                producto_id=detalle.id_producto, nuevo_stock=nuevo_stock
            )

        # 4. Vaciar el carrito del cliente
        carrito_crud = CarritoCRUD(self.db)
        carrito_crud.vaciar_carrito_cliente(str(factura_data.id_cliente))

        # 5. Confirmar todas las operaciones
        self.db.commit()
        self.db.refresh(db_factura)
        return db_factura

    def obtener_factura(self, factura_id: int) -> Optional[Factura]:
        """
        Obtiene una factura por su ID, incluyendo sus detalles.
        """
        return (
            self.db.query(Factura).filter(Factura.id_factura == factura_id).first()
        )

    def obtener_facturas_por_cliente(self, cliente_id: str) -> List[Factura]:
        """
        Obtiene todas las facturas de un cliente específico.
        """
        return (
            self.db.query(Factura)
            .filter(Factura.id_cliente == cliente_id)
            .order_by(Factura.fecha_creacion.desc())
            .all()
        )