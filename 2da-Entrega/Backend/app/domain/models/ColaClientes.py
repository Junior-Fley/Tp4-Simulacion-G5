from domain.models.ColaFIFO import ColaFIFO


class ColaClientes(ColaFIFO):
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
                    "id": elemento.id_cliente,
                    "estado": elemento.estado,
                }
                for elemento in self.elementos
            ]
            self._dirty = False

        return list(self._cache)