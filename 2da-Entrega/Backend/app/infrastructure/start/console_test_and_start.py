from app.application.useCases.Simular import Simular
from app.infrastructure.start.console_test_repo import ConsoleTestRepo

repo_test = ConsoleTestRepo()

simulacion = Simular(repo_test, 900_000, 1000, 600)


simulacion.ejecutar_simulacion()