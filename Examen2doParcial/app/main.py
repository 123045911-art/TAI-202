#importaciones
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import Optional
from pydantic import BaseModel,Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#Instancia del servidor
app= FastAPI(
    title= "Exámen 2do Parcial",
    description= "Ali Daniel Flores García",
    version="1.0"
)

security = HTTPBasic()

def varificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuario_correcto= secrets.compare_digest(credentials.username,"admin")
    contrasena_correcta= secrets.compare_digest(credentials.password,"rest123")

    if not (usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas",
        )
    return credentials.username

#Modelo de datos
class crear_reserva(BaseModel):
    id:int
    nombre:str=Field(..., min_length=6, example="José")
    cantidad_personas:int=Field(..., gt=1, le=10, example=4)
    dia:str=Field(..., example="lunes 10 de octubre de 2026")
    hora_registro:str=Field(..., time_format="%H:%M", example="19:30")
    estado:str=Field(..., example="pendiente")

#Base de datos simulada
reservas= [
    {"id":1,"nombre":"Ana","cantidad_personas":4,"dia":"lunes","hora_registro":"19:30","estado":"pendiente"},
    {"id":2,"nombre":"Luis","cantidad_personas":2,"dia":"martes","hora_registro":"20:00","estado":"confirmada"},
    {"id":3,"nombre":"María","cantidad_personas":6,"dia":"miércoles","hora_registro":"18:00","estado":"cancelada"}
]

#ENDPOINTS
@app.get("/reservas/",tags=['HTTP CRUD'])
async def consulta_reservas(usuarioAuth: str= Depends(varificar_peticion)):
    return {
        "total_reservas": len(reservas),
        "reservas": reservas,
        "status": "200"
    }

@app.post("/reservas/",tags=['HTTP CRUD'])
async def agregar_reservas(reserva:crear_reserva):
    for rsv in reservas:
        if rsv["id"] == reserva.id:
            raise HTTPException(
                status_code=400,
                detail="La reserva con este ID ya existe"
            )
        if rsv["nombre"] == reserva.nombre:
            raise HTTPException(
                status_code=400,
                detail="La reserva con este nombre ya existe"
            )
    if reserva.cantidad_personas < 1 or reserva.cantidad_personas > 10:
        raise HTTPException(
            status_code=400,
            detail="La cantidad de personas debe ser entre 1 y 10"
        )
    if reserva.hora_registro < "08:00" or reserva.hora_registro > "22:00":
        raise HTTPException(
            status_code=400,
            detail="La hora de registro debe ser entre 08:00 y 22:00"
        )
    if reserva.dia.lower() == "domingo":
        raise HTTPException(
            status_code=400,
            detail="No se admiten reservaciones los domingos"
        )
    if reserva.nombre.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="El nombre no puede estar vacío"
        )
    if reserva.nombre.isdigit():
        raise HTTPException(
            status_code=400,
            detail="El nombre no puede contener solo números"
        )
    reservas.append(reserva)
    return {
        "mensaje":"Reserva Agregada"
    }

@app.put("/reservas/{id}", tags=['HTTP CRUD'])
async def cancelar_citas(id: int, usuarioAuth: str = Depends(varificar_peticion)):
    for reserva in reservas:
        if reserva["id"] == id:
            if reserva["estado"] == "cancelada":
                raise HTTPException(status_code=400, detail="La reserva ya está cancelada")
            reserva["estado"] = "cancelada"
            return {
                "mensaje": "Reserva cancelada exitosamente",
                "reserva_actualizada": reserva
            }
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

@app.delete("/reservas/{id}", tags=['HTTP CRUD'])
async def eliminar_usuario(id: int):
    for index, usr in enumerate(reservas):
        if usr["id"] == id:
            usuario_eliminado = reservas.pop(index)
            return {
                "mensaje": "Reserva eliminada exitosamente",
                "usuario_eliminado": usuario_eliminado
            }
            
    raise HTTPException(status_code=404, detail="Reserva no encontrada")