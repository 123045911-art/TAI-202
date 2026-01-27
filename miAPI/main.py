#importaciones
from fastapi import FastAPI
import asyncio


#Instancia del servidor
app= FastAPI()

#Endpoints
@app.get("/")
async def holamundo():
    return {"message": "Hola Mundo FastAPI"}

@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje":"bienvenido a FastAPI",
        "estatus":"200"
    }