"""
API de Carrito - Endpoints para gestión del carrito de compras
"""

from typing import List

from crud.crud_carrito import CarritoCRUD
from database.config import get_db
from entities.carrito import CarritoCreate, CarritoResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/carrito", tags=["Carrito"])


@router.post("/", response_model=CarritoResponse, status_code=status.HTTP_201_CREATED)
async def agregar_producto_al_carrito(
    item: CarritoCreate, db: Session = Depends(get_db)
):
    """
    Agrega un producto al carrito de un cliente.
    """
    try:
        carrito_crud = CarritoCRUD(db)
        # Aquí podrías añadir validaciones, como verificar si el producto y el cliente existen.
        nuevo_item = carrito_crud.agregar_al_carrito(
            id_producto=item.id_producto,
            id_cliente=item.id_cliente,
            id_cliente_creacion=item.id_cliente_creacion,
        )
        return nuevo_item
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al agregar producto al carrito: {str(e)}",
        )


@router.get("/{id_cliente}", response_model=List[CarritoResponse])
async def obtener_carrito_del_cliente(id_cliente: str, db: Session = Depends(get_db)):
    """
    Obtiene todos los productos en el carrito de un cliente específico.
    """
    try:
        carrito_crud = CarritoCRUD(db)
        items_carrito = carrito_crud.obtener_carrito_por_cliente(id_cliente)
        return items_carrito
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el carrito del cliente: {str(e)}",
        )


@router.delete("/item/{id_carrito}", status_code=status.HTTP_200_OK)
async def eliminar_item_del_carrito(id_carrito: int, db: Session = Depends(get_db)):
    """
    Elimina un item específico del carrito.
    """
    try:
        carrito_crud = CarritoCRUD(db)
        item_existente = carrito_crud.obtener_item_carrito(id_carrito)
        if not item_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item del carrito no encontrado",
            )

        eliminado = carrito_crud.eliminar_item_carrito(id_carrito)
        if not eliminado:
            # Esto no debería ocurrir si la comprobación anterior pasó
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo eliminar el item del carrito.",
            )

        return {"mensaje": "Item eliminado del carrito exitosamente."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el item del carrito: {str(e)}",
        )


@router.delete("/{id_cliente}", status_code=status.HTTP_200_OK)
async def vaciar_carrito(id_cliente: str, db: Session = Depends(get_db)):
    """
    Elimina todos los items del carrito de un cliente.
    """
    try:
        carrito_crud = CarritoCRUD(db)
        num_eliminados = carrito_crud.vaciar_carrito_cliente(id_cliente)
        return {
            "mensaje": f"Carrito vaciado exitosamente. Se eliminaron {num_eliminados} items."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al vaciar el carrito: {str(e)}",
        )