import random

from app.domain.models.event.Evento import Evento
from app.domain.models.EstadoTecnico import EstadoTecnico

from typing import TYPE_CHECKING

from domain.models.EstadoCliente import EstadoCliente

if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular


class AbreTienda(Evento):
    def __init__(self):
        super().__init__("Abre_Tienda")

    def ejecutar_accion(self, simulacion: Simular):
        simulacion.hora_proximo_fin_atencion = None
        print(f'Iteracion de AbreTienda')
        simulacion.clientes_no_atendidos += simulacion.cola_clientes.cantidad()
        for cliente in simulacion.cola_clientes.elementos:
            cliente.estado = EstadoCliente.NO_ATENDIDO_POR_CIERRE.value
        simulacion.cola_clientes.marcar_dirty()
        simulacion.cola_clientes.serialize()
        simulacion.cola_clientes.vaciar()
        #TODO Al vaciar, cambio el estado de los clientes por "no_atendido_por_cierre"
        # y los pateo a todos fuera de mi negocio

        simulacion.hora_actual = simulacion.hora_apertura
        simulacion.local_abierto = True
        simulacion.tecnico.estado = EstadoTecnico.LIBRE

        simulacion.rnd_llegada = random.random()
        simulacion.tiempo_hasta_proxima_llegada = simulacion.exponencial_negativa(
            simulacion.media_llegada,
            simulacion.rnd_llegada
        )
        simulacion.hora_proxima_llegada = simulacion.hora_actual + simulacion.tiempo_hasta_proxima_llegada

        from app.domain.models.event.LlegaCliente import LlegaCliente
        simulacion.proximo_evento = LlegaCliente()