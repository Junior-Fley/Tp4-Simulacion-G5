from app.domain.models.EstadoEquipo import EstadoEquipo
from datetime import datetime

class Equipo:
    def __init__(self, estado: EstadoEquipo, hora_ingreso_taller:datetime, horario_inicio_reparacion: datetime,
                 horario_fin_reparacion: datetime, tiempo_de_reparacion: float, tiempo_acumulado_reparacion: float):
        self.estado: EstadoEquipo = estado
        self.hora_ingreso_taller: datetime= hora_ingreso_taller
        self.horario_inicio_reparacion: datetime = horario_inicio_reparacion
        self.horario_fin_reparacion: datetime = horario_fin_reparacion
        self.tiempo_de_reparacion: float = tiempo_de_reparacion
        self.tiempo_acumulado_reparacion: float = tiempo_acumulado_reparacion
