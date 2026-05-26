from app.domain.models.ColaFIFO import ColaFIFO

class ColaEquipos(ColaFIFO):
    def __init__(self):
        super().__init__()
        self._cache = []
        self._dirty = True

    def marcar_dirty(self):
        self._dirty = True

    def serialize(self):
        if self._dirty:
            self._cache = [
                {
                    "id": elemento.id_equipo,
                    "estado": elemento.estado,
                    "hora_dejado": elemento.hora_ingreso_taller,
                    "hora_fin": elemento.horario_fin_reparacion,
                    "tiempo": elemento.tiempo_de_reparacion
                }
                for elemento in self.elementos
            ]
            self._dirty = False

        return list(self._cache)