from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os

#1. Definimos la URL de conexión
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@localhost:5432/DB_miapi"
)

#2. Crear el motor de conexion
engine = create_engine(DATABASE_URL)

#3. Prepararmos el gestionador de sesiones
SessionLocal = sessionmaker(
    autocommit=False, # ninguna confirmacion a la base de datos es automátic
    autoflush=False, # ninguna modificación es automática
    bind=engine # definir motor en uso
)

#4. Base declarativa del modelo
Base = declarative_base()

#5. Obtener sesiones de cada peticion
def get_db():
    db = SessionLocal()
    try:
        yield db # cede el control a la sesion de cada petición
    finally:
        db.close()