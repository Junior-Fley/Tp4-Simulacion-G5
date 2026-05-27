from app.domain.models.Colas.ColaFIFO import ColaFIFO
from app.domain.services.float_a_hora_service import float_a_hora

class ColaEquipos(ColaFIFO):
    def __init__(self):
        super().__init__()
        self._cache = []
        self._dirty = True
        self._dirty_segunda = False

    def marcar_dirty(self):
        self._dirty = True
        # si volví a marcar dirty, entonces mi caché ya no está bien que persista una vuelta extra
        self._dirty_segunda = False

    def marcar_dirty_segunda(self):
        self._dirty_segunda = True

    def serialize(self):
        # esto indica que el caché está bien para el primer serialize que ocurra, pero no para el segundo
        if self._dirty_segunda:
            # me aseguro que la siguiente vuelta no entre a este if, sino al de abajo
            self._dirty_segunda = False
            self._dirty = True

        # si el caché no representa el estado actual lo recalculamos
        elif self._dirty:
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