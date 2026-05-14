from enum import Enum


class EstadoCliente(Enum):
    # en cola, atendido, se fue sin reparar, dejo equipo para reparar, no atendido por cierre
    EN_COLA = "en_cola"
    ATENDIDO = "atendido"
    SE_FUE_SIN_REPARAR = "se_fue_sin_reparar"
    DEJO_EQUIPO_PARA_REPARAR = "dejo_equipo_para_reparar"
    NO_ATENDIDO_POR_CIERRE = "no_atendido_por_cierre"
    