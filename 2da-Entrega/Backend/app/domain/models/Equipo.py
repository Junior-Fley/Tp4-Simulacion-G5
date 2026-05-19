from app.domain.models.EstadoEquipo import EstadoEquipo
from datetime import datetime

class Equipo:
    def __init__(self, estado: EstadoEquipo, hora_ingreso_taller:float, horario_inicio_reparacion: float|None,
                 horario_fin_reparacion: float|None, tiempo_de_reparacion: float, tiempo_acumulado_reparacion: float):
        self.estado: EstadoEquipo = estado
        self.hora_ingreso_taller: float= hora_ingreso_taller
        self.horario_inicio_reparacion: float = horario_inicio_reparacion
        self.horario_fin_reparacion: float = horario_fin_reparacion
        self.tiempo_de_reparacion: float = tiempo_de_reparacion
        self.tiempo_acumulado_reparacion: float = tiempo_acumulado_reparacion
        self.tiempo_reparacion_restante: float = tiempo_de_reparacion
