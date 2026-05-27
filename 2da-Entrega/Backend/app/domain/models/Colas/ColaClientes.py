from app.domain.models.Colas.ColaFIFO import ColaFIFO


class ColaClientes(ColaFIFO):
    def __init__(self):
        super().__init__()
        self._cache = []
        self._dirty = True

    def marcar_dirty(self):
        self._dirty = True
        # si volví a marcar dirty, entonces mi caché ya no está bien que persista una vuelta extra

    def marcar_dirty_segunda(self):
        raise NotImplementedError("NO EXISTE MOTIVO POR EL CUAL LA FILA CLIENTES DEBERÍA LLAMAR A ESTE MÉTODO \n"
                                  "REVISEN QUE JORACA ESTÁN HACIENDO CON LA LÓGICA PORQUE ESTO NO ESTÁ BIEN")

    def serialize(self):
        # si el caché no representa el estado actual lo recalculamos
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