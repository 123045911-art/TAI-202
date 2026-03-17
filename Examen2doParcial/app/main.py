from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import re
from datetime import date

app = FastAPI(
    title="Exámen 2do Parcial",
    description="Ali Daniel Flores García",
    version="1.0"
)

security = HTTPBasic()

def varificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuario_correcto = secrets.compare_digest(credentials.username, "admin")
    contrasena_correcta = secrets.compare_digest(credentials.password, "rest123")

    if not (usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Modelo de datos
class crear_reserva(BaseModel):
    id: int
    nombre: str = Field(..., min_length=6, example="José Martinez")
    cantidad_personas: int = Field(..., ge=1, le=10, example=4)
    fecha: date = Field(..., example="2026-10-15")
    hora_registro: str = Field(..., example="19:30")
    estado: str = Field(default="pendiente", example="pendiente")

# Base de datos simulada
reservas = [
    {"id": 1, "nombre": "Ana Torres", "cantidad_personas": 4, "fecha": "2026-10-12", "hora_registro": "19:30", "estado": "pendiente"},
    {"id": 2, "nombre": "Luis Miguel", "cantidad_personas": 2, "fecha": "2026-10-13", "hora_registro": "20:00", "estado": "confirmada"},
    {"id": 3, "nombre": "María José", "cantidad_personas": 6, "fecha": "2026-10-14", "hora_registro": "18:00", "estado": "cancelada"}
]

# ENDPOINTS
@app.get("/reservas/", tags=['HTTP CRUD'])
async def consulta_reservas():
    return {
        "total_reservas": len(reservas),
        "reservas": reservas,
        "status": "200"
    }

@app.get("/reservas/{id}", tags=['HTTP CRUD'])
async def Buscar_por_id(id: int):
    reserva_encontrada = next((r for r in reservas if r["id"] == id), None)
    if not reserva_encontrada:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    return {
        "mensaje": "reserva encontrada",
        "reserva": reserva_encontrada,
        "status": "200"
    }

@app.post("/reservas/", tags=['HTTP CRUD'], status_code=201)
async def agregar_reservas(reserva: crear_reserva):
    if any(r["id"] == reserva.id for r in reservas):
        raise HTTPException(status_code=400, detail="La reserva con este ID ya existe")

    if any(str(r["nombre"]).lower() == str(reserva.nombre).lower() for r in reservas):
        raise HTTPException(status_code=400, detail="La reserva con este nombre ya existe")

    año_actual = date.today().year
    if reserva.fecha.year != año_actual:
        raise HTTPException(status_code=400, detail=f"Solo se permiten reservaciones para el año en curso ({año_actual})")

    if reserva.fecha < date.today():
        raise HTTPException(status_code=400, detail="No se permiten reservaciones en fechas pasadas")

    if reserva.fecha.weekday() == 6:
        raise HTTPException(status_code=400, detail="No se admiten reservaciones los domingos")

    if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", reserva.hora_registro):
        raise HTTPException(status_code=400, detail="La hora debe tener formato HH:MM (ej. 08:30)")

    if not ("08:00" <= reserva.hora_registro <= "22:00"):
        raise HTTPException(status_code=400, detail="La hora de registro debe ser entre 08:00 y 22:00")

    estados_validos = ["pendiente", "confirmada", "cancelada"]
    if reserva.estado not in estados_validos:
        raise HTTPException(status_code=400, detail="El estado debe ser: pendiente, confirmada o cancelada")

    nombre_str = str(reserva.nombre)
    if nombre_str.strip() == "" or nombre_str.replace(" ", "").isdigit():
        raise HTTPException(status_code=400, detail="El nombre es inválido (vacío o puros números)")

    reservas.append(reserva.model_dump())
    return {"mensaje": "Reserva Agregada", "nueva_reserva": reserva}

@app.put("/reservas/{id}", tags=['HTTP CRUD'])
async def cancelar_reservacion(id: int, usuarioAuth: str = Depends(varificar_peticion)):
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

@app.put("/reservas/{id}/aceptar", tags=['HTTP CRUD'])
async def aceptar_reservacion(id: int, usuarioAuth: str = Depends(varificar_peticion)):
    for reserva in reservas:
        if reserva["id"] == id:
            if reserva["estado"] == "confirmada":
                raise HTTPException(status_code=400, detail="La reserva ya se encuentra confirmada")
            if reserva["estado"] == "cancelada":
                raise HTTPException(status_code=400, detail="No se puede aceptar una reserva que fue cancelada")
            reserva["estado"] = "confirmada"
            return {
                "mensaje": "Reserva aceptada y confirmada exitosamente",
                "reserva_actualizada": reserva
            }
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

@app.delete("/reservas/{id}", tags=['HTTP CRUD'])
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(varificar_peticion)):
    for index, rsv in enumerate(reservas):
        if rsv["id"] == id:
            reserva_eliminada = reservas.pop(index)
            return {
                "mensaje": "Reserva eliminada exitosamente",
                "reserva_eliminada": reserva_eliminada
            }
    raise HTTPException(status_code=404, detail="Reserva no encontrada")