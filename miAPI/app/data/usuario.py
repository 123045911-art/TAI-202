from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.data.db import Base

class Usuario(Base):
    __tablename__ = "tb-usuarios"
    id = mapped_column(Integer, primary_key=True, index=True)
    nombre = mapped_column(String)
    edad = mapped_column(Integer)