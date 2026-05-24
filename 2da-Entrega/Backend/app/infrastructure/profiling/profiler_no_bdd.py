import cProfile
import pstats
from pstats import SortKey

from app.application.useCases.Simular import Simular
from app.infrastructure.database.unit_of_work.uow_factory import uow_factory

from app.infrastructure.start.console_test_repo import ConsoleTestRepo

def main() -> None:

    simulador = Simular(
        uow_factory=uow_factory,
        x_tiempo=0,
        i_iteraciones=100_000,
        j_hora_inicio=600,
        repo_override=ConsoleTestRepo()
    )

    simulador.ejecutar_simulacion()


if __name__ == "__main__":
    profiler = cProfile.Profile()

    profiler.enable()
    main()
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats(SortKey.CUMULATIVE)
    stats.print_stats(40)