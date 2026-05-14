from enum import Enum


class EstadoCliente(Enum):
    # en cola, atendido, se fue sin reparar, dejo equipo para reparar, no atendido por cierre
    EN_COLA = "en_cola"
    SIENDO_ATENDIDO = "siendo_atendido"
    NO_ATENDIDO_POR_CIERRE = "no_atendido_por_cierre"
    