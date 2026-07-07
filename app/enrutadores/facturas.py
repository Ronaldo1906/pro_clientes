from fastapi import APIRouter, HTTPException, status
from sqlmodel import SQLModel
from modelos.facturas import Factura, FacturaCrear, FacturaEditar, FacturaLeer, FacturaLeerCompuesta
from modelos.clientes import Cliente
from listas import lista_Clientes, lista_facturas
from conexion_bd import Sesion_dependencia
from sqlmodel import select

rutas_facturas = APIRouter()


#lista_facturas:list[Factura] = []

# end point para listar las facturas de un cliente en especifico
@rutas_facturas.get("/facturas", response_model=list[FacturaLeerCompuesta])
async def Listar_Facturas_Cliente(sesion: Sesion_dependencia):
    #select * from factura
    consulta = select(Factura)
    lista_facturas = sesion.exec(consulta).all()
    return lista_facturas


# end point para obtener una sola factura por su id
@rutas_facturas.get("/facturas/{id_factura}", response_model=FacturaLeerCompuesta)
async def Listar_Factura(id_factura: int, sesion: Sesion_dependencia):
    factura_encontrada = sesion.get(Factura, id_factura)
    if not factura_encontrada:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"La factura con id {id_factura}, no existe")
    return factura_encontrada
 
 
@rutas_facturas.post("/facturas/{Cliente_id}", response_model=Factura)
async def Crear_Factura(Cliente_id: int, datos_factura: FacturaCrear, sesion: Sesion_dependencia):
    cliente_encontrado = sesion.get(Cliente, Cliente_id)
    if not cliente_encontrado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El cliente con id {Cliente_id}, no existe")
    #validar datos de la factura-json, pasar dict
    factura_dict = datos_factura.model_dump()
    factura_dict["id_cliente"] = Cliente_id   # <- corregido: coincide con el nombre real del campo
    factura_val = Factura.model_validate(factura_dict)
    #guardar en bd
    sesion.add(factura_val)
    sesion.commit()
    sesion.refresh(factura_val)
    return factura_val



