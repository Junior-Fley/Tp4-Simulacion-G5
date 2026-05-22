from collections import deque
from dataclasses import dataclass, field


@dataclass
class ColaFIFO:
    elementos: deque = field(default_factory=deque)

    def agregar(self, elemento):
        self.elementos.append(elemento)

    def retirar(self):
        if self.esta_vacia():
            return None

        return self.elementos.popleft()

    def primero(self):
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