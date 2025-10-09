from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_conn import get_db
from crud import crud_usuario
from schemas import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=ClienteResponse)
def crear_usuario(usuario: ClienteCreate, db: Session = Depends(get_db)):
    return crud_usuario.crear_cliente(db, usuario)


@router.get("/", response_model=list[ClienteResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return crud_usuario.listar_clientes(db)


@router.put("/{usuario_id}", response_model=ClienteResponse)
def actualizar_usuario(
    usuario_id: int, usuario: ClienteUpdate, db: Session = Depends(get_db)
):
    actualizado = crud_usuario.actualizar_cliente(db, usuario_id, usuario)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return actualizado


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    eliminado = crud_usuario.eliminar_cliente(db, usuario_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado correctamente"}
