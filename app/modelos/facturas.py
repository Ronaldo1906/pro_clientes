from pydantic import computed_field
from sqlmodel import SQLModel, Field, Relationship
from modelos.transacciones import Transacciones
from modelos.clientes import Cliente, ClienteLeer
from datetime import datetime


class FacturaBase(SQLModel):
    fecha: str = Field(default=datetime.now())


class FacturaCrear(FacturaBase):
    id_cliente: int  # el cliente al que pertenece la factura, se envía al crear


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_cliente: int | None = Field(default=None, foreign_key="cliente.id")  # <- FK que faltaba
    transacciones: list["Transacciones"] = Relationship(back_populates="factura")
    cliente: Cliente | None = Relationship(back_populates="factura")
class FacturaLeer(FacturaBase):
    id: int
    cliente: ClienteLeer


class FacturaLeerCompuesta(FacturaLeer):
    transacciones: list[Transacciones] = []

    @computed_field
    @property
    def vr_total(self) -> float:
        total_factura = 0.0
        for transaccion in self.transacciones:
            total_factura += transaccion.vr_unitario * transaccion.cantidad
        return total_factura

