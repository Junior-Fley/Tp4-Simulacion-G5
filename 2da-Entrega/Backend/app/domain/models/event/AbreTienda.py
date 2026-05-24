import random

from app.domain.models.event.Evento import Evento
from app.domain.models.EstadoTecnico import EstadoTecnico

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular


class AbreTienda(Evento):
    def __init__(self):
        super().__init__("Abre_Tienda")

    def ejecutar_accion(self, simulacion: Simular):
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