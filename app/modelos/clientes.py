from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship



#crear el modelo clientes(id, nombre, email, descripcion)
class ClienteBase(SQLModel): 
    nombre: str = Field(default=None)
    email: str
    descripcion: str | None = Field(default=None)


class ClienteCrear(ClienteBase):
    pass


class ClienteEditar(ClienteBase):
    pass


class Cliente(ClienteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    #relacion virtual con factura
    factura: list["Factura"] = Relationship(back_populates="cliente")

class ClienteLeer(ClienteBase):
    id: int