from pydantic import BaseModel,Field

#Agregamos validaciones Perzonalizadas
#Creamos el modelo de validación pydantic
class crear_usuario(BaseModel):
    nombre:str=Field(..., min_length=3, max_length=50, examples=["José"])
    edad:int=Field(..., gt=1, le=123, description="Edad válida entre 1 y 123")