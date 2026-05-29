import cProfile
import pstats
from pstats import SortKey

from app.application.useCases.QuerySimulaciones import QuerySimulaciones
from app.infrastructure.database.unit_of_work.uow_factory import uow_factory


def main() -> None:

    query = QuerySimulaciones(uow_factory=uow_factory)


    query.get_simulaciones_filtradas(1, "12:00:00", 10000)


if __name__ == "__main__":
    profiler = cProfile.Profile()

    profiler.enable()
    main()
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats(SortKey.CUMULATIVE)
    stats.print_stats(40)