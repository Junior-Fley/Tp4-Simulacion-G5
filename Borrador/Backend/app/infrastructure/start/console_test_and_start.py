from app.application.useCases.Simular import Simular
from app.infrastructure.start.console_test_repo import ConsoleTestRepo
from app.infrastructure.database.unit_of_work.uow_factory import uow_factory

repo_test = ConsoleTestRepo()

simulacion = Simular(uow_factory, 900_000, 1000, 600, repo_test)


simulacion.ejecutar_simulacion()