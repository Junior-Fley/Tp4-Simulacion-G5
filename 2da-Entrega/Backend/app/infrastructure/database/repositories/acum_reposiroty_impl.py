from sqlalchemy.orm import Session

from app.application.ports.acumulador_repository import IAcumuladorRepository
from app.infrastructure.database.models.acum_orm import AcumEquiposORM


class AcumEquiposRepositoryImpl(IAcumuladorRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def guardar_acumulador(self,coleccion_id: int,acumulador: float) -> int:
        acum_equipos_orm = AcumEquiposORM(
            coleccion_id=coleccion_id,
            acumulador=acumulador
        )

        self.session.add(acum_equipos_orm)
        self.session.flush()

        return acum_equipos_orm.id

    def obtener_acumulador(self, coleccion_id: int) -> float | None:

        acumulador_orm = (self.session.query(AcumEquiposORM).filter(AcumEquiposORM.coleccion_id == coleccion_id).first())

        if acumulador_orm is None:
            return None

        return float(acumulador_orm.acumulador) # type: ignore[arg-type]