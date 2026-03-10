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

#Modelo de datos
class crear_reserva(BaseModel):
    id:int
    nombre:str=Field(..., min_length=6, example="José")
    cantidad_personas:int=Field(..., gt=1, le=10, example=4)
    fecha:str=Field(..., time_format="%Y-%m-%d", example="2024-06-30")
    hora_registro:str=Field(..., time_format="%H:%M", example="19:30")
    estado:str=Field(..., example="pendiente")

#Base de datos simulada
reservas= [
    {"id":1,"nombre":"Ana","cantidad_personas":4,"fecha":"2024-06-30","hora_registro":"19:30","estado":"pendiente"},
    {"id":2,"nombre":"Luis","cantidad_personas":2,"fecha":"2024-07-01","hora_registro":"20:00","estado":"confirmada"}
]

#ENDPOINTS
@app.get("/reservas/",tags=['HTTP CRUD'])
async def consulta_reservas():
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
    reservas.append(reserva)
    return {
        "mensaje":"Reserva Agregada",
        "Datos nuevos":reservas
    }



