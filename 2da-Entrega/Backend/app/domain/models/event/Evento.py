import random
from abc import ABC
from enum import Enum
from typing import TYPE_CHECKING
from domain.models.EstadoTecnico import EstadoTecnico


if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular
    from domain.models.Equipo import Equipo


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
    def comprobar_hora_final(simulacion: Simular) -> bool|None:
        if simulacion.hora_actual >= simulacion.hora_final:
            from domain.models.event.FinReparacion import FinReparacion

            # Actualizo el estado del técnico
            simulacion.tecnico.estado = EstadoTecnico.REPARANDO

            # si hay equipos en la cola, entonces debo calcular el tiempo de reparación del primer equipo de la cola, si este tiempo no fue calculado antes, es decir, si se está trabajando por primera vez con ese equipo
            primer_equipo: Equipo = simulacion.cola_equipos.primero()
            if primer_equipo is not None:
                if primer_equipo.tiempo_de_reparacion is None:

                    # es la primera vez que se trabaja con este equipo, debo calcular cuanto va a tardar en repararse

                    simulacion.rnd_reparacion = round(random.random(), 3)
                    simulacion.tiempo_hasta_reparacion = simulacion.exponencial_negativa(simulacion.media_reparacion,
                                                                                         simulacion.rnd_reparacion)

                    # le asigno al primer equipo el tiempo de reparación que acabo de calcular
                    primer_equipo.tiempo_de_reparacion = simulacion.tiempo_hasta_reparacion
                    primer_equipo.tiempo_reparacion_restante = simulacion.tiempo_hasta_reparacion

                else:
                    simulacion.tiempo_hasta_reparacion = primer_equipo.tiempo_reparacion_restante
                    # si ya se trabajó con este equipo, entonces el tiempo de reparación que falta es el
                    # tiempo de reparación restante que tiene el equipo, que se actualiza cada vez que se interrumpe la reparación

                simulacion.proximo_evento = FinReparacion()

            return simulacion.hora_actual >= simulacion.hora_final