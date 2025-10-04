"""
API de Productos - Endpoints para gestión de productos
"""

from typing import List

from crud.crud_producto import ProductoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ProductoCreate, ProductoResponse, ProductoUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(
    producto_data: ProductoCreate, db: Session = Depends(get_db)
):
    """
    Crea un nuevo producto.
    """
    try:
        producto_crud = ProductoCRUD(db)
        nuevo_producto = producto_crud.crear_producto(producto_data)
        return nuevo_producto
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el producto: {str(e)}",
        )


@router.get("/", response_model=List[ProductoResponse])
async def obtener_productos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtiene una lista de todos los productos.
    """
    producto_crud = ProductoCRUD(db)
    productos = producto_crud.obtener_productos(skip=skip, limit=limit)
    return productos


@router.get("/{producto_id}", response_model=ProductoResponse)
async def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un producto por su ID.
    """
    producto_crud = ProductoCRUD(db)
    producto = producto_crud.obtener_producto(producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return producto


@router.get("/buscar/", response_model=List[ProductoResponse])
async def buscar_productos_por_nombre(nombre: str, db: Session = Depends(get_db)):
    """
    Busca productos por su nombre.
    """
    producto_crud = ProductoCRUD(db)
    productos = producto_crud.buscar_productos_por_nombre(nombre)
    return productos


@router.put("/{producto_id}", response_model=ProductoResponse)
async def actualizar_producto(
    producto_id: int, producto_data: ProductoUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza un producto existente.
    """
    producto_crud = ProductoCRUD(db)
    try:
        producto_actualizado = producto_crud.actualizar_producto(
            producto_id, producto_data
        )
        if not producto_actualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )
        return producto_actualizado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el producto: {str(e)}",
        )


@router.delete("/{producto_id}", status_code=status.HTTP_200_OK)
async def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Elimina un producto por su ID.
    """
    producto_crud = ProductoCRUD(db)
    # Verificar si el producto existe antes de intentar eliminar
    if not producto_crud.obtener_producto(producto_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )

    eliminado = producto_crud.eliminar_producto(producto_id)
    if not eliminado:
        # Este caso es poco probable si la verificación anterior pasó,
        # pero es bueno tenerlo por si acaso.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar el producto.",
        )

    return {"mensaje": "Producto eliminado exitosamente."}