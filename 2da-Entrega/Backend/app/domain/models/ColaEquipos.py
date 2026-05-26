from domain.models.ColaFIFO import ColaFIFO
from app.domain.services.float_a_hora_service import float_a_hora


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
                    "hora_dejado": float_a_hora(elemento.hora_ingreso_taller) if elemento.hora_ingreso_taller is not None else '',
                    "hora_fin": float_a_hora(elemento.horario_fin_reparacion) if elemento.horario_fin_reparacion is not None else '',
                    "tiempo": float_a_hora(elemento.tiempo_de_reparacion) if elemento.tiempo_de_reparacion is not None else '',
                }
                for elemento in self.elementos
            ]
            self._dirty = False

        return list(self._cache)