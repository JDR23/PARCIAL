"""
API de Tipos de Producto - Endpoints para gestión de categorías de productos
"""

from typing import List

from crud.crud_tipo_producto import TipoProductoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import TipoProductoCreate, TipoProductoResponse, TipoProductoUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/tipos_producto", tags=["Tipos de Producto"])


@router.post(
    "/", response_model=TipoProductoResponse, status_code=status.HTTP_201_CREATED
)
async def crear_tipo_producto(
    tipo_data: TipoProductoCreate, db: Session = Depends(get_db)
):
    """
    Crea un nuevo tipo de producto (categoría).
    """
    try:
        crud = TipoProductoCRUD(db)
        nuevo_tipo = crud.crear_tipo_producto(tipo_data)
        return nuevo_tipo
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el tipo de producto: {str(e)}",
        )


@router.get("/", response_model=List[TipoProductoResponse])
async def obtener_tipos_producto(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtiene una lista de todos los tipos de producto.
    """
    crud = TipoProductoCRUD(db)
    tipos = crud.obtener_tipos_producto(skip=skip, limit=limit)
    return tipos


@router.get("/{tipo_id}", response_model=TipoProductoResponse)
async def obtener_tipo_producto(tipo_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un tipo de producto por su ID.
    """
    crud = TipoProductoCRUD(db)
    tipo = crud.obtener_tipo_producto_por_id(tipo_id)
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de producto no encontrado",
        )
    return tipo


@router.put("/{tipo_id}", response_model=TipoProductoResponse)
async def actualizar_tipo_producto(
    tipo_id: int, tipo_data: TipoProductoUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza un tipo de producto existente.
    """
    crud = TipoProductoCRUD(db)
    try:
        tipo_actualizado = crud.actualizar_tipo_producto(tipo_id, tipo_data)
        if not tipo_actualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de producto no encontrado",
            )
        return tipo_actualizado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{tipo_id}", status_code=status.HTTP_200_OK)
async def eliminar_tipo_producto(tipo_id: int, db: Session = Depends(get_db)):
    """
    Elimina un tipo de producto por su ID.
    """
    crud = TipoProductoCRUD(db)
    if not crud.obtener_tipo_producto_por_id(tipo_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de producto no encontrado",
        )

    eliminado = crud.eliminar_tipo_producto(tipo_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar el tipo de producto. "
            "Es posible que esté siendo usado por algún producto.",
        )

    return {"mensaje": "Tipo de producto eliminado exitosamente."}