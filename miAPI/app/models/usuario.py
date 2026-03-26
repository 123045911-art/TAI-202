from pydantic import BaseModel,Field
from typing import Optional

#Agregamos validaciones Perzonalizadas
#Creamos el modelo de validación pydantic
class crear_usuario(BaseModel):
    nombre:str=Field(..., min_length=3, max_length=50, examples=["José"])
    edad:int=Field(..., gt=1, le=123, description="Edad válida entre 1 y 123")

class actualiza_usuario(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=3, max_length=50, examples=["José"])
    edad: Optional[int] = Field(default=None, gt=1, le=123, description="Edad válida entre 1 y 123")