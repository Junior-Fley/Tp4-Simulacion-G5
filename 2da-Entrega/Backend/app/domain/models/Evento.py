from abc import ABC
from enum import Enum


class Evento(Enum):
    ABRE_TIENDA = "Abre tienda"
    LLEGA_CLIENTE = "Llega cliente"
    FIN_ATENCION_CL = "Fin atención cl"
    FIN_REPARACION_CL = "Fin reparación cl"
    CIERRA_TIENDA = "Cierra tienda"