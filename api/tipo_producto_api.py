from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import crud_tipo_producto
from schemas import TipoProductoCreate, TipoProductoUpdate, TipoProductoOut

router = APIRouter(prefix="/tipos_producto", tags=["Tipos de Producto"])


@router.post("/", response_model=TipoProductoOut)
def crear_tipo_producto(
    tipo_producto: TipoProductoCreate, db: Session = Depends(get_db)
):
    return crud_tipo_producto.crear_tipo_producto(db, tipo_producto)


@router.get("/", response_model=list[TipoProductoOut])
def obtener_tipos_producto(db: Session = Depends(get_db)):
    return crud_tipo_producto.obtener_tipos_producto(db)


@router.get("/{tipo_id}", response_model=TipoProductoOut)
def obtener_tipo_producto(tipo_id: int, db: Session = Depends(get_db)):
    tipo = crud_tipo_producto.obtener_tipo_producto(db, tipo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    return tipo


@router.put("/{tipo_id}", response_model=TipoProductoOut)
def actualizar_tipo_producto(
    tipo_id: int, datos: TipoProductoUpdate, db: Session = Depends(get_db)
):
    tipo = crud_tipo_producto.actualizar_tipo_producto(db, tipo_id, datos)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    return tipo


@router.delete("/{tipo_id}")
def eliminar_tipo_producto(tipo_id: int, db: Session = Depends(get_db)):
    eliminado = crud_tipo_producto.eliminar_tipo_producto(db, tipo_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    return {"mensaje": "Tipo de producto eliminado correctamente"}
