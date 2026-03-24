from sys import prefix
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import varificar_peticion
from sqlalchemy.orm import Session, query
from app.data.db import get_db
from app.data.usuario import Usuario as dbUsuario

router = APIRouter(
    prefix = "/v1/usuarios",
    tags = ["HTTP CRUD"]
)

@router.get("/")
async def leer_usuarios(db:Session=Depends(get_db)):
    queryUsuarios=db.query(dbUsuario).all()
    return {
        "status":"200",
        "total":len(queryUsuarios),
        "usuarios":queryUsuarios
    }

@router.post("/",status_code=status.HTTP_201_CREATED)
async def agregar_usuarios(usuarioP:crear_usuario,db:Session=Depends(get_db)):
    nuevoU= dbUsuario(nombre=usuarioP.nombre,edad=usuarioP.edad)
    db.add(nuevoU)
    db.commit()
    db.refresh(nuevoU)

    return {
        "mensaje":"Usuario Agregado",
        "Datos nuevos":usuarioP
    }

@router.put("/{id}",status_code=status.HTTP_200_OK)
async def actualizar_usuario_completo(id: int, usuario_actualizado: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_actualizado["id"] = id 
            usuarios[index] = usuario_actualizado
            return {"mensaje": "Usuario actualizado por completo", "datos": usuarios[index]}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.patch("/{id}",status_code=status.HTTP_200_OK)
async def actualizar_usuario_parcial(id: int, campos: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr.update(campos)
            return {"mensaje": "Usuario actualizado parcialmente", "usuario": usr}
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.delete("/{id}",status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, usuarioAuth: str= Depends(varificar_peticion)): #<-- Requiere autenticación para eliminar

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por {usuarioAuth}", #<-- Muestra quién eliminó al usuario
                "usuario_eliminado": usuario_eliminado
            }
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")