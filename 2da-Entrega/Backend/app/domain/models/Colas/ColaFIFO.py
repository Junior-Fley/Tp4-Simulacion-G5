from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.models.Cliente import Cliente
    from app.domain.models.Equipo import Equipo


@dataclass
class ColaFIFO(ABC):
    elementos: deque = field(default_factory=deque)

    def agregar(self, elemento):
        self.elementos.append(elemento)

    def agregar_primero(self, elemento):
        """Inserta `elemento` al frente de la cola (como primer elemento).

        Usa deque.appendleft para que el elemento quede en la posición 0.
        """
        self.elementos.appendleft(elemento)

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

    @abstractmethod
    def serialize(self):
        #este método devuelve una lista con diccionarios conteniendo cada uno de los elementos de la cola
        pass

    @abstractmethod
    def marcar_dirty(self):
        pass
    
    @abstractmethod
    def marcar_dirty_segunda(self):
        pass