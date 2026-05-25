from app.application.useCases.Simular import Simular

from app.infrastructure.database.unit_of_work.uow_factory import uow_factory


simulacion = Simular(uow_factory, 900_000, 1000, 600)


simulacion.ejecutar_simulacion()