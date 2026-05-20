from abc import ABC
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular


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