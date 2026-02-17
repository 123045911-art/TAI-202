#importaciones
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional

#Instancia del servidor
app= FastAPI(
    title= "Mi primer API",
    description= "Ivan Isay Guerra L",
    version="1.0"
)

#TB ficticia
usuarios=[
    {"id":1,"nombre":"Fany","edad":21},
    {"id":2,"nombre":"Aly","edad":21},
    {"id":3,"nombre":"Dulce","edad":21},
]

#Endpoints
@app.get("/")
async def holamundo():
    return {"mensaje":"Hola Mundo FastAPI"}

@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje":"Bienvenido a FastAPI",
        "estatus":"200",
        }

@app.get("/v1/parametroOb/{id}",tags=['Parametro Obligatorio'])
async def consultauno(id:int):
    return {"mensaje":"usuario encontrado",
            "usuario":id,
            "status":"200" }

@app.get("/v1/parametroOp/",tags=['Parametro Opcional'])
async def consultatodos(id:Optional[int]=None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return{"mensaje":"usuario encontrado","usuario":usuarioK}
        return{"mensaje":"usuario no encontrado","status":"200"}
    else:
        return {"mensaje":"No se proporciono id","status":"200"}
    
@app.get("/v1/usuarios/",tags=['HTTP CRUD'])
async def leer_usuarios():
    return {
        "total":len(usuarios),
        "usuarios":usuarios,
        "status":"200"
    }

@app.post("/v1/usuarios/",tags=['HTTP CRUD'])
async def agregar_usuarios(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El usuario con este ID ya existe"
            )
    usuarios.append(usuario)
    return {
        "mensaje":"Usuario Agregado",
        "Datos nuevos":usuario
    }

@app.put("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario_completo(id: int, usuario_actualizado: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_actualizado["id"] = id 
            usuarios[index] = usuario_actualizado
            return {"mensaje": "Usuario actualizado por completo", "datos": usuarios[index]}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.patch("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario_parcial(id: int, campos: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr.update(campos)
            return {"mensaje": "Usuario actualizado parcialmente", "usuario": usr}
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def eliminar_usuario(id: int):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(index)
            return {
                "mensaje": "Usuario eliminado exitosamente",
                "usuario_eliminado": usuario_eliminado
            }
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")