"""
API de Facturas - Endpoints para gestión de facturas
"""

from typing import List
from uuid import UUID

from crud.crud_factura import FacturaCRUD
from database.config import get_db
from entities.factura import FacturaCreate, FacturaResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/facturas", tags=["Facturas"])


@router.post("/", response_model=FacturaResponse, status_code=status.HTTP_201_CREATED)
async def crear_factura(factura_data: FacturaCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva factura.

    Este endpoint realiza varias acciones:
    - Valida que los productos existan y haya stock suficiente.
    - Crea la factura y sus detalles.
    - Actualiza el stock de los productos vendidos.
    - Vacía el carrito del cliente.

    Toda la operación es una transacción: si algo falla, nada se guarda.
    """
    factura_crud = FacturaCRUD(db)
    try:
        nueva_factura = factura_crud.crear_factura(factura_data)
        return nueva_factura
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # En una app real, aquí se registraría el error detallado.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error inesperado al procesar la factura: {e}",
        )


@router.get("/{factura_id}", response_model=FacturaResponse)
async def obtener_factura(factura_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una factura por su ID.
    """
    factura_crud = FacturaCRUD(db)
    factura = factura_crud.obtener_factura(factura_id)
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
        )
    return factura


@router.get("/cliente/{cliente_id}", response_model=List[FacturaResponse])
async def obtener_facturas_del_cliente(
    cliente_id: UUID, db: Session = Depends(get_db)
):
    """
    Obtiene todas las facturas de un cliente específico.
    """
    factura_crud = FacturaCRUD(db)
    facturas = factura_crud.obtener_facturas_por_cliente(str(cliente_id))
    if not facturas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron facturas para este cliente.",
        )
    return facturas