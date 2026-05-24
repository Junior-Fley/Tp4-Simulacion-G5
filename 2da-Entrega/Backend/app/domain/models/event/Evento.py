import random
from abc import ABC
from enum import Enum
from typing import TYPE_CHECKING
from app.domain.models.EstadoTecnico import EstadoTecnico

if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular
    from app.domain.models.Equipo import Equipo


class EventoEnum(Enum):
    ABRE_TIENDA = "Abre tienda"
    LLEGA_CLIENTE = "Llega cliente"
    FIN_ATENCION_CL = "Fin atención cl"
    FIN_REPARACION_CL = "Fin reparación cl"
    CIERRA_TIENDA = "Cierra tienda"

class Evento(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre

    def ejecutar_accion(self, simulacion: Simular):
        print("no deberías ver esto nunca, todas las subclases de Evento deberían implementar este método")
        raise NotImplementedError()

    @staticmethod
    def comprobar_hora_final(simulacion: Simular) -> bool:
        """
        Cuando llegamos al cierre (hora_cierre), preparamos la transición al modo nocturno.
        Retorna True si hemos pasado el horario de cierre.
        """
        if simulacion.hora_actual >= simulacion.hora_cierre:
            from app.domain.models.event.FinReparacion import FinReparacion

            # Si hay equipos en la cola, el próximo evento es la reparación
            if simulacion.cola_equipos.cantidad() > 0:
                primer_equipo: Equipo = simulacion.cola_equipos.primero()

                # Si el equipo no tiene tiempo de reparación calculado, lo calculamos ahora
                if primer_equipo.tiempo_de_reparacion is None:
                    simulacion.rnd_reparacion = random.random()
                    simulacion.tiempo_hasta_reparacion = simulacion.exponencial_negativa(
                        simulacion.media_reparacion,
                        simulacion.rnd_reparacion
                    )
                    primer_equipo.tiempo_de_reparacion = simulacion.tiempo_hasta_reparacion
                    primer_equipo.tiempo_reparacion_restante = simulacion.tiempo_hasta_reparacion

                simulacion.tecnico.estado = EstadoTecnico.REPARANDO
                simulacion.proximo_evento = FinReparacion()
            else:
                # Si no hay equipos, el técnico se va a casa y espera la reapertura
                simulacion.tecnico.estado = EstadoTecnico.LIBRE
                from app.domain.models.event.AbreTienda import AbreTienda
                simulacion.proximo_evento = AbreTienda()

            return True

        return False