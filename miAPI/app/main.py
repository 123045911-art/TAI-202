#importaciones
from fastapi import FastAPI
from app.router import usuario,misc

#Instancia del servidor
app= FastAPI(
    title= "Mi primer API",
    description= "Ali Daniel Flores García",
    version="1.0"
)

app.include_router(usuario.router)
app.include_router(misc.misc)