from app.domain.models.EstadoEquipo import EstadoEquipo

class Equipo:
    def __init__(self, id_equipo: int, estado: EstadoEquipo, hora_ingreso_taller:float, horario_inicio_reparacion: float|None,
                 horario_fin_reparacion: float|None, tiempo_de_reparacion: float| None, tiempo_acumulado_reparacion: float):
        self.id_equipo: int = id_equipo
        self.estado: str = estado.value
        self.hora_ingreso_taller: float= hora_ingreso_taller
        self.horario_inicio_reparacion: float = horario_inicio_reparacion
        self.horario_fin_reparacion: float = horario_fin_reparacion
        self.tiempo_de_reparacion: float = tiempo_de_reparacion
        self.tiempo_acumulado_reparacion: float = tiempo_acumulado_reparacion
        self.tiempo_reparacion_restante: float = tiempo_de_reparacion
