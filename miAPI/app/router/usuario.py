from sys import prefix
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import varificar_peticion

router = APIRouter(
    prefix = "/v1/usuarios",
    tags = ["HTTP CRUD"]
)

@router.get("/")
async def leer_usuarios():
    return {
        "total":len(usuarios),
        "usuarios":usuarios,
        "status":"200"
    }

@router.post("/",status_code=status.HTTP_201_CREATED)
async def agregar_usuarios(usuario:crear_usuario): #<-- usamos el modelo
    for usr in usuarios:
        if usr["id"] == usuario.id: #<-- Se cambia porque ya no usamos dict
            raise HTTPException(
                status_code=400,
                detail="El usuario con este ID ya existe"
            )
    usuarios.append(usuario)
    return {
        "mensaje":"Usuario Agregado",
        "Datos nuevos":usuario
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