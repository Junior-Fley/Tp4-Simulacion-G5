from __future__ import annotations
from app.domain.models.Cliente import Cliente
from app.domain.models.EstadoCliente import EstadoCliente
from app.domain.models.event.Evento import Evento

import random

from typing import TYPE_CHECKING

from app.domain.models.EstadoTecnico import EstadoTecnico

if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular

class CierraTienda(Evento):
    def __init__(self):
        super().__init__("Cierra_tienda")

    def ejecutar_accion(self, simulacion: Simular):

        #todo revisar

        if simulacion.tecnico.estado == EstadoTecnico.ATENDIENDO_CLIENTE:
            simulacion.tecnico.acum_atencion += simulacion.hora_proxima_llegada - simulacion.hora_actual
        elif simulacion.tecnico.estado == EstadoTecnico.REPARANDO:
            simulacion.tecnico.acum_reparacion += simulacion.hora_proxima_llegada - simulacion.hora_actual

        # la hora actual es la hora de cierre
        simulacion.hora_actual = simulacion.hora_cierre

        # si cerré debo vaciar la cola de clientes, excepto el 1er cliente si este está siendo atendido
        primer_cliente = simulacion.cola_clientes.primero()


        #vació la cola de clientes
        simulacion.cola_clientes.vaciar()

        # si había un primer cliente
        if primer_cliente is not None:
            # si el primer cliente estaba siendo atendido vuelve a la cola
            if primer_cliente.estado == EstadoCliente.SIENDO_ATENDIDO.value:
                simulacion.cola_clientes.agregar(primer_cliente)

        # no debo modificar el evento siguiente, asigno el evento_2
        simulacion.proximo_evento = simulacion.proximo_evento_2

        # si mi proximo evento era una llegada de cliente, se descarta
        if simulacion.proximo_evento.nombre == "Llega_Cliente":
            if simulacion.cola_clientes.cantidad() > 0 and simulacion.cola_clientes.primero().estado == EstadoCliente.SIENDO_ATENDIDO.value:
                # si es así, entonces lo termino de atender completamente a puertas cerradas si hace falta
                from app.domain.models.event.FinAtencion import FinAtencion
                simulacion.proximo_evento = FinAtencion()
                # si no hay clientes en la cola, pero si hay equipos para reparar en la cola, entonces reparo.
            elif simulacion.cola_equipos.cantidad() > 0:
                # Actualizo el estado del técnico
                simulacion.tecnico.estado = EstadoTecnico.REPARANDO
                self.calcular_tiempo_hasta_reparacion(simulacion)
                from app.domain.models.event.FinReparacion import FinReparacion
                simulacion.proximo_evento = FinReparacion()
                # si no hay clientes ni equipos en las colas, entonces mi técnico se puede ir a casa tranquilo
                # y la proxima acción será la apertura de la tienda del día siguiente
            else:
                from app.domain.models.event.AbreTienda import AbreTienda
                simulacion.tecnico.estado = EstadoTecnico.LIBRE
                simulacion.proximo_evento = AbreTienda()
            return



