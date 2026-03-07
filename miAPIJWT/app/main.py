# Importaciones necesarias
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm #Librerías para autenticación con OAuth2
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
import jwt # Importamos PyJWT para manejar tokens JWT
from datetime import datetime, timedelta, timezone # Importamos datetime para manejar la expiración de los tokens

# Configuraciones para la seguridad de los tokens
SECRET_KEY = "claveSegura123"  # Llave secreta para firmar los tokens
ALGORITHM = "HS256"            # Algoritmo de encriptación
Tiempo_de_expiracion = 1      # El token durará solo 1 minuto

# Instancia principal de la aplicación
app = FastAPI(
    title="Mi primer API protegida",
    description="Ali Daniel Flores García",
    version="1.0"
)

# Base de datos ficticia
usuarios = [
    {"id": 1, "nombre": "Fany", "edad": 21},
    {"id": 2, "nombre": "Ali", "edad": 21},
    {"id": 3, "nombre": "Dulce", "edad": 21},
]

# Esquema de seguridad que le dice a FastAPI dónde se piden los tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelo para validar los datos al crear un usuario
class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario") 
    nombre: str = Field(..., min_length=3, max_length=50, example="José")
    edad: int = Field(..., gt=1, le=123, description="Edad válida entre 1 y 123")


# Rutas de Autenticación
#se define quien es el usuario correcto y se le entrega un token, si no es correcto se le niega el acceso
@app.post("/token", tags=['Autenticación'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario_correcto = form_data.username == "alidaniel"
    contrasena_correcta = form_data.password == "123456"

    # Si es un intruso, le negamos el acceso
    if not (usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Calculo de la fecha de expiración del token (1 minuto a partir de ahora)
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=Tiempo_de_expiracion)
    
    # Creamos el token
    token_data = {"sub": form_data.username, "exp": expiracion}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    # Entregamos el token al usuario
    return {"access_token": token, "token_type": "bearer"}


# Esta función para proteger las rutas, se encarga de verificar que el token que nos da el usuario sea válido
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        # Intentamos desencriptar el token que nos da el usuario
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return username
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="El token ha expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


# Endpoints
@app.get("/")
async def holamundo():
    return {"mensaje": "Hola Mundo FastAPI"}

@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje": "Bienvenido a FastAPI",
        "estatus": "200",
    }

@app.get("/v1/parametroOb/{id}", tags=['Parametro Obligatorio'])
async def consultauno(id: int):
    return {"mensaje": "usuario encontrado", "usuario": id, "status": "200"}

@app.get("/v1/parametroOp/", tags=['Parametro Opcional'])
async def consultatodos(id: Optional[int] = None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuarioK}
        return {"mensaje": "usuario no encontrado", "status": "200"}
    else:
        return {"mensaje": "No se proporciono id", "status": "200"}
    
@app.get("/v1/usuarios/", tags=['HTTP CRUD'])
async def leer_usuarios():
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
    }

@app.post("/v1/usuarios/", tags=['HTTP CRUD'])
async def agregar_usuarios(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id: 
            raise HTTPException(
                status_code=400,
                detail="El usuario con este ID ya existe"
            )
    # Convertimos a diccionario para mantener la consistencia con la lista original
    usuarios.append(usuario.model_dump())
    return {
        "mensaje": "Usuario Agregado",
        "Datos nuevos": usuario
    }

# RUTA PROTEGIDA: Solo quien tenga el token puede actualizar
@app.put("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario_completo(id: int, usuario_actualizado: dict,usuarioAuth: str = Depends(verificar_token)):#<-Agregamos la dependencia para verificar el token
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_actualizado["id"] = id 
            usuarios[index] = usuario_actualizado
            return {"mensaje": f"Usuario actualizado por {usuarioAuth}", "datos": usuarios[index]}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.patch("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario_parcial(id: int, campos: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr.update(campos)
            return {"mensaje": "Usuario actualizado parcialmente", "usuario": usr}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# RUTA PROTEGIDA: Solo quien tenga el token puede eliminar
@app.delete("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_token)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por {usuarioAuth}",
                "usuario_eliminado": usuario_eliminado
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")