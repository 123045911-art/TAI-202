from fastapi import status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#Seguridad HTTP Básica
security = HTTPBasic()

def varificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuario_correcto= secrets.compare_digest(credentials.username,"alidaniel")
    contrasena_correcta= secrets.compare_digest(credentials.password,"123456")

    if not (usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas",
        )
    return credentials.username