from app.domain.models.Cliente import Cliente
from app.domain.models.EstadoCliente import EstadoCliente
from app.domain.models.event.Evento import Evento

import random

from typing import TYPE_CHECKING

from app.domain.models.EstadoTecnico import EstadoTecnico

if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular

class LlegaCliente(Evento):
    def __init__(self):
        super().__init__("Llega_Cliente")

    def ejecutar_accion(self, simulacion: Simular):

        if not simulacion.local_abierto:
            simulacion.proximo_evento = None
            return

        if simulacion.tecnico.estado == EstadoTecnico.ATENDIENDO_CLIENTE:
            simulacion.tecnico.acum_atencion += simulacion.hora_proxima_llegada - simulacion.hora_actual
        elif simulacion.tecnico.estado == EstadoTecnico.REPARANDO:
            simulacion.tecnico.acum_reparacion += simulacion.hora_proxima_llegada - simulacion.hora_actual

        simulacion.hora_actual = simulacion.hora_proxima_llegada

        cliente = Cliente(EstadoCliente.EN_COLA, simulacion.hora_actual, None, None)
        simulacion.cola_clientes.agregar(cliente)

        simulacion.rnd_llegada = random.random()
        simulacion.tiempo_hasta_proxima_llegada = simulacion.exponencial_negativa(
            simulacion.media_llegada,
            simulacion.rnd_llegada
        )
        simulacion.hora_proxima_llegada = simulacion.hora_actual + simulacion.tiempo_hasta_proxima_llegada

        simulacion.tecnico.estado = EstadoTecnico.ATENDIENDO_CLIENTE

        if simulacion.cola_clientes.primero().estado == EstadoCliente.EN_COLA:
            simulacion.cola_clientes.primero().estado = EstadoCliente.SIENDO_ATENDIDO
            simulacion.rnd_atencion = random.random()
            simulacion.tiempo_hasta_fin_de_atencion = simulacion.uniforme(
                simulacion.rnd_atencion,
                simulacion.min_atencion,
                simulacion.max_atencion
            )
            simulacion.hora_proximo_fin_atencion = simulacion.hora_actual + simulacion.tiempo_hasta_fin_de_atencion

        if simulacion.hora_proxima_llegada > simulacion.hora_proximo_fin_atencion:
            from app.domain.models.event.FinAtencion import FinAtencion
            simulacion.proximo_evento = FinAtencion()
        else:
            simulacion.proximo_evento = LlegaCliente()