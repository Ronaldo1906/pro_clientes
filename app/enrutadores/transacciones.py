from fastapi import APIRouter, HTTPException, status
from modelos.transacciones import Transacciones, TransaccionesCrear, TransaccionesEditar
from modelos.facturas import Factura
from listas import lista_transacciones, lista_facturas
from conexion_bd import Sesion_dependencia
from sqlmodel import select

rutas_transacciones = APIRouter()
#lista_transacciones:list[Transacciones] = []





@rutas_transacciones.get("/transacciones/cliente/{cliente_id}", response_model=list[Transacciones])
async def Listar_Transacciones_Cliente(sesion: Sesion_dependencia):
    #consulta =select(Transacciones)
    #lista_transacciones = sesion.exec(consulta).all()
    #return lista_transacciones
    return sesion.exec(select(Transacciones)).all()

@rutas_transacciones.get("/transacciones", response_model=list[Transacciones])
async def Listar_Transacciones(transacciones_id: int):
    for i, obj_transacciones in enumerate(lista_transacciones):
        if obj_transacciones.id == transacciones_id:
            return  obj_transacciones
 
#end point para listar una sola transaccion de un cliente en especifico
@rutas_transacciones.post("/transacciones/{factura_id}", response_model=Transacciones)
async def Crear_Transacciones(factura_id: int, datos_transacciones: TransaccionesCrear, sesion: Sesion_dependencia):
    factura_encontrada = sesion.get(Factura, factura_id)
    if not factura_encontrada:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"La factura con id {factura_id}, no existe")

    transaccion_dict = datos_transacciones.model_dump()
    transaccion_dict["id_factura"] = factura_id   
    transaccion_val = Transacciones.model_validate(transaccion_dict)
    sesion.add(transaccion_val)
    sesion.commit()
    sesion.refresh(transaccion_val)
    return transaccion_val

#@rutas_transacciones.patch(
   # "/transacciones/{id_transacciones}", response_model=Transacciones)

#async def editar_transaccion(id_transacciones: int, datos_transacciones: Transacciones):

@rutas_transacciones.delete("/transacciones/{transaccion_id}", response_model=Transacciones)
async def eliminar_transaccion(transaccion_id: int, mi_sesion: Sesion_dependencia):
    transaccion_bd = mi_sesion.get(Transacciones, transaccion_id)
    if not transaccion_bd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"La transacción con id {transaccion_id}, no existe")
    mi_sesion.delete(transaccion_bd)
    mi_sesion.commit()
    #retornar un mensaje, debe quitar el response_model
    return transaccion_bd