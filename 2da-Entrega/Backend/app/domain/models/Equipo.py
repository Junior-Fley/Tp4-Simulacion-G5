

class Equipo:
    def __init__(self, estado, hora_ingreso_taller, horario_inicio_reparacion, horario_fin_reparacion,
                 tipo_de_reparacion, tiempo_acumulado_reparacion):
        self.estado = estado
        self.hora_ingreso_taller = hora_ingreso_taller
        self.horario_inicio_reparacion = horario_inicio_reparacion
        self.horario_fin_reparacion = horario_fin_reparacion
        self.tipo_de_reparacion = tipo_de_reparacion
        self.tiempo_acumulado_reparacion = tiempo_acumulado_reparacion
    