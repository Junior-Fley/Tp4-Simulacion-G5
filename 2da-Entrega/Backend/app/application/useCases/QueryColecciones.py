from app.infrastructure.database.unit_of_work.unit_of_work import UowFactory


class QueryColecciones:
    def __init__(self, uow_factory: UowFactory):
        self.uow_factory = uow_factory

    def listar_ids(self) -> list[int]:
        with self.uow_factory() as uow:
            return uow.colec_repo.listar_ids()

