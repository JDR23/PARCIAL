"""
API de Clientes - Endpoints para gestión de clientes
"""

from typing import List

from crud.crud_cliente import ClienteCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ClienteCreate, ClienteResponse, ClienteUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def crear_cliente(cliente_data: ClienteCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo cliente.
    """
    try:
        cliente_crud = ClienteCRUD(db)
        nuevo_cliente = cliente_crud.crear_cliente(cliente_data)
        return nuevo_cliente
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el cliente: {str(e)}",
        )


@router.get("/", response_model=List[ClienteResponse])
async def obtener_clientes(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtiene una lista de todos los clientes.
    """
    try:
        cliente_crud = ClienteCRUD(db)
        clientes = cliente_crud.obtener_clientes(skip=skip, limit=limit)
        return clientes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los clientes: {str(e)}",
        )


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un cliente por su ID.
    """
    cliente_crud = ClienteCRUD(db)
    cliente = cliente_crud.obtener_cliente_por_id(cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
        )
    return cliente


@router.put("/{cliente_id}", response_model=ClienteResponse)
async def actualizar_cliente(
    cliente_id: int, cliente_data: ClienteUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza la información de un cliente existente.
    """
    cliente_crud = ClienteCRUD(db)
    cliente_actualizado = cliente_crud.actualizar_cliente(cliente_id, cliente_data)
    if not cliente_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
        )
    return cliente_actualizado


@router.delete("/{cliente_id}", status_code=status.HTTP_200_OK)
async def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Elimina un cliente por su ID.
    """
    cliente_crud = ClienteCRUD(db)
    # Primero, verificar si el cliente existe
    if not cliente_crud.obtener_cliente_por_id(cliente_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
        )

    eliminado = cliente_crud.eliminar_cliente(cliente_id)
    if not eliminado:
        # Este caso podría darse si hay un problema de concurrencia
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar el cliente.",
        )

    return {"mensaje": "Cliente eliminado exitosamente."}