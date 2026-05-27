from abc import ABC, abstractmethod


class IColeccionRepository(ABC):

    @abstractmethod
    def guardar_coleccion(self) -> int:
        pass

    @abstractmethod
    def listar_ids(self) -> list[int]:
        pass