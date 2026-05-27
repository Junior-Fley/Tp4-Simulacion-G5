from enum import Enum


class EstadoEquipo(Enum):
    # En diagnóstico, En cola reparación, En reparación, Reparación interrumpida, Reparado
    EN_COLA_REPARACION = "en_cola_reparacion"
    EN_REPARACION = "en_reparacion"
    REPARACION_INTERRUPIDA = "reparacion_interrumpida"
    REPARADO = "reparado"

