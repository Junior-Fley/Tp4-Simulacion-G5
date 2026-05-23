from collections import deque
from dataclasses import dataclass, field

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.models.Cliente import Cliente
    from domain.models.Equipo import Equipo


@dataclass
class ColaFIFO:
    elementos: deque = field(default_factory=deque)

    def agregar(self, elemento):
        self.elementos.append(elemento)

    def retirar(self):
        if self.esta_vacia():
            return None

        return self.elementos.popleft()

    def primero(self) -> Cliente | Equipo | None:
        if self.esta_vacia():
            return None

        return self.elementos[0]

    def modificar_primero(self, nuevo_elemento):
        if self.esta_vacia():
            return None

        self.elementos[0] = nuevo_elemento
        return self.elementos[0]

    def esta_vacia(self):
        return len(self.elementos) == 0

    def cantidad(self):
        return len(self.elementos)

    def vaciar(self):
        self.elementos.clear()