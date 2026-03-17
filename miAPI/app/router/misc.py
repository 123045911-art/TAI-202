import asyncio
from typing import Optional
from app.data.database import usuarios
from fastapi import APIRouter

misc = APIRouter(tags = ["Varios"])

#Endpoints
@misc.get("/")
async def holamundo():
    return {"mensaje":"Hola Mundo FastAPI"}

@misc.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje":"Bienvenido a FastAPI",
        "estatus":"200",
        }

@misc.get("/v1/parametroOb/{id}",tags=['Parametro Obligatorio'])
async def consultauno(id:int):
    return {"mensaje":"usuario encontrado",
            "usuario":id,
            "status":"200" }

@misc.get("/v1/parametroOp/",tags=['Parametro Opcional'])
async def consultatodos(id:Optional[int]=None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return{"mensaje":"usuario encontrado","usuario":usuarioK}
        return{"mensaje":"usuario no encontrado","status":"200"}
    else:
        return {"mensaje":"No se proporciono id","status":"200"}