from sqlalchemy.orm import Session

from app.application.ports.Coleccion_repository import IColeccionRepository
from app.infrastructure.database.models.Coleccion_orm import ColeccionORM


class ColeccionRepositoryImpl(IColeccionRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def guardar_coleccion(self) -> int:
        coleccion_orm = ColeccionORM()
        self.session.add(coleccion_orm)
        self.session.flush()

        return coleccion_orm.id

    def listar_ids(self) -> list[int]:
        ids = self.session.query(ColeccionORM.id).order_by(ColeccionORM.id).all()
        return [row[0] for row in ids]
