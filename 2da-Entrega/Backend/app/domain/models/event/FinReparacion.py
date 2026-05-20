from app.domain.models.event.Evento import Evento


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular

class FinReparacion(Evento):
    def __init__(self):
        super().__init__("Llega_Cliente")

    def ejecutar_accion(self, simulacion: Simular):
        pass