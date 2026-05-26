from typing import List

from app.application.ports.Simulacion_repository import ISimulacionRepository
from app.infrastructure.database.unit_of_work.unit_of_work import UowFactory
from app.domain.models.Simulacion import Simulacion
from app.infrastructure.database.mappers.simulacion_mapper import SimulacionMapper


class QuerySimulaciones:
    def __init__(self, uow_factory: UowFactory, simu_repo: ISimulacionRepository = None):
        self.uow_factory = uow_factory
        self.simu_repo = simu_repo
        self.simu_mapper = SimulacionMapper()


    def get_simulaciones(self, simulacion_id: int, page: int, size: int) -> tuple[List[Simulacion], int]:
        with self.uow_factory() as uow:
            simulaciones_orm, total = uow.simu_repo.obtener_filas_simulacion(simulacion_id, page, size)

            simulaciones: List[Simulacion] = []

            for simulacion in simulaciones_orm:
                simu_domain = self.simu_mapper.convert_orm_to_domain(simulacion)
                simulaciones.append(simu_domain)

            return simulaciones, total
