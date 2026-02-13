#importaciones
from fastapi import FastAPI
import asyncio


#Instancia del servidor
app= FastAPI()

#Endpoints
@app.get("/")
async def holamundo():
    return {"message": "Hola Mundo FastAPI"}

#Endpoint con parametro obligatorio
@app.get("/usuarios/{usuario_id}")
async def obtener_usuario(usuario_id: int):
    return {"usuario_id": usuario_id, "mensaje": "Usuario encontrado"}

#Endpoint con parametro opcional
@app.get("/buscar")
async def buscar_producto(nombre: str = "Todos"):
    return {"criterio": nombre, "resultado": "Lista de productos"}

@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje":"bienvenido a FastAPI",
        "estatus":"200"
    }