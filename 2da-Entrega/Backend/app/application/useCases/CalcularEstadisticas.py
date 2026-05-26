from app.infrastructure.database.unit_of_work.unit_of_work_impl import UowFactory
from application.ports.Simulacion_repository import ISimulacionRepository


class CalcularEstadisticas:
    def __init__(self, coleccion_id: int, uow_factory: UowFactory, repo_override: ISimulacionRepository|None = None):
        self.coleccion_id = coleccion_id
        self.uow_factory = uow_factory
        self.repo_override = repo_override

    def calcular_estadisticas(self):
        pass