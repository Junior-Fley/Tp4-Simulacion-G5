from __future__ import annotations
import random

from app.domain.models.event.Evento import Evento
from app.domain.models.EstadoTecnico import EstadoTecnico

from typing import TYPE_CHECKING

from app.domain.models.EstadoCliente import EstadoCliente

if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular


class AbreTienda(Evento):
    def __init__(self):
        super().__init__("Abre_Tienda")

    def ejecutar_accion(self, simulacion: Simular):
        # dejar todas las filas como están al principio de una nueva simulación
        simulacion.hora_proximo_fin_atencion = 0
        simulacion.hora_proximo_fin_reparacion = None
        simulacion.tiempo_hasta_reparacion = 0
        simulacion.presupuesto = ''
        simulacion.rnd_reparacion = 0
        simulacion.rnd_presupuesto = 0
        simulacion.rnd_llegada = 0
        simulacion.rnd_atencion = 0
        simulacion.rnd_acepta = 0
        simulacion.hora_proxima_llegada = 0
        simulacion.hora_proximo_fin_atencion = 0
        simulacion.hora_actual = 0
        simulacion.tiempo_hasta_proxima_llegada = 0
        simulacion.tiempo_hasta_fin_de_atencion = 0
        simulacion.tiempo_hasta_reparacion = 0
        simulacion.acepto = None
        simulacion.cierre = False

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