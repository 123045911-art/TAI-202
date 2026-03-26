from sys import prefix
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario, actualiza_usuario
from app.data.database import usuarios
from app.security.auth import varificar_peticion
from sqlalchemy.orm import Session, query
from app.data.db import get_db
from app.data.usuario import Usuario as dbUsuario

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]
)

@router.get("/")
async def leer_usuarios(db: Session = Depends(get_db)):
    queryUsuarios = db.query(dbUsuario).all()
    return {"status": "200", 
    "total": len(queryUsuarios),
    "usuarios": queryUsuarios}

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def leer_usuario(id: int, db: Session = Depends(get_db)):
    queryUsuario = db.query(dbUsuario).filter(dbUsuario.id == id).first()
    if not queryUsuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return queryUsuario

@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuarios(usuarioP: crear_usuario, db: Session = Depends(get_db)):
    nuevoU = dbUsuario(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(nuevoU)
    db.commit()
    db.refresh(nuevoU)
    return {"mensaje": "Usuario Agregado", "Datos nuevos": usuarioP}

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario_completo(id: int, usuarioP: crear_usuario, db: Session = Depends(get_db)):
    queryUsuario = db.query(dbUsuario).filter(dbUsuario.id == id).first()
    if not queryUsuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    queryUsuario.nombre = usuarioP.nombre
    queryUsuario.edad = usuarioP.edad
    db.commit()
    db.refresh(queryUsuario)
    return {"mensaje": "Usuario actualizado por completo", "datos": queryUsuario}

@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario_parcial(id: int, usuarioP: actualiza_usuario, db: Session = Depends(get_db)):
    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    update_data = usuarioP.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(usuario_db, key, value)
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(varificar_peticion), db: Session = Depends(get_db)):
    queryUsuario = db.query(dbUsuario).filter(dbUsuario.id == id).first()
    if not queryUsuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(queryUsuario)
    db.commit()
    return {
        "mensaje": f"Usuario eliminado por {usuarioAuth}",  # <-- Muestra quién eliminó al usuario
        "usuario_eliminado": queryUsuario,
    }