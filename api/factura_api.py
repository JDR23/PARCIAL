from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import crud_factura
from schemas import FacturaCreate, FacturaUpdate, FacturaOut

router = APIRouter(prefix="/facturas", tags=["Facturas"])


@router.post("/", response_model=FacturaOut)
def crear_factura(factura: FacturaCreate, db: Session = Depends(get_db)):
    return crud_factura.crear_factura(db, factura)


@router.get("/", response_model=list[FacturaOut])
def obtener_facturas(db: Session = Depends(get_db)):
    return crud_factura.obtener_facturas(db)


@router.get("/{factura_id}", response_model=FacturaOut)
def obtener_factura(factura_id: int, db: Session = Depends(get_db)):
    factura = crud_factura.obtener_factura(db, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura


@router.put("/{factura_id}", response_model=FacturaOut)
def actualizar_factura(
    factura_id: int, datos: FacturaUpdate, db: Session = Depends(get_db)
):
    factura = crud_factura.actualizar_factura(db, factura_id, datos)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura


@router.delete("/{factura_id}")
def eliminar_factura(factura_id: int, db: Session = Depends(get_db)):
    eliminado = crud_factura.eliminar_factura(db, factura_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return {"mensaje": "Factura eliminada correctamente"}
