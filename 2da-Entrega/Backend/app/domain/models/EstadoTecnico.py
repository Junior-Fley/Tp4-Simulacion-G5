from enum import Enum


class EstadoTecnico(Enum):
    LIBRE = "libre"
    ATENDIENDO_CLIENTE = "atendiendo_cliente"
    REPARANDO = "reparando"