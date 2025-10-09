from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import crud_carrito
from schemas import CarritoCreate, CarritoUpdate, CarritoOut

router = APIRouter(prefix="/carritos", tags=["Carritos"])


@router.post("/", response_model=CarritoOut)
def crear_carrito(carrito: CarritoCreate, db: Session = Depends(get_db)):
    return crud_carrito.crear_carrito(db, carrito)


@router.get("/", response_model=list[CarritoOut])
def obtener_carritos(db: Session = Depends(get_db)):
    return crud_carrito.obtener_carritos(db)


@router.get("/{carrito_id}", response_model=CarritoOut)
def obtener_carrito(carrito_id: int, db: Session = Depends(get_db)):
    carrito = crud_carrito.obtener_carrito(db, carrito_id)
    if not carrito:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    return carrito


@router.put("/{carrito_id}", response_model=CarritoOut)
def actualizar_carrito(
    carrito_id: int, datos: CarritoUpdate, db: Session = Depends(get_db)
):
    carrito = crud_carrito.actualizar_carrito(db, carrito_id, datos)
    if not carrito:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    return carrito


@router.delete("/{carrito_id}")
def eliminar_carrito(carrito_id: int, db: Session = Depends(get_db)):
    eliminado = crud_carrito.eliminar_carrito(db, carrito_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    return {"mensaje": "Carrito eliminado correctamente"}
