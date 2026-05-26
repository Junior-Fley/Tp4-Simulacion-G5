from abc import ABC, abstractmethod


class IAcumuladorRepository(ABC):
    @abstractmethod
    def guardar_acumulador(self, coleccion_id: int, acumulador: float, contador: int) -> int:
        raise NotImplementedError("Este método debe ser implementado por la clase que herede de IAcumuladorRepository")
    @abstractmethod
    def obtener_acumulador(self, coleccion_id: int) -> float | None:
        raise NotImplementedError("Este método debe ser implementado por la clase que herede de IAcumuladorRepository")

