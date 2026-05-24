from typing import Callable, Protocol
from sqlalchemy.orm import Session

from app.application.ports.Simulacion_repository import ISimulacionRepository
from application.ports.Coleccion_repository import IColeccionRepository

SessionFactory = Callable[[], Session]

class IUnitOfWork(Protocol):

    simu_repo: ISimulacionRepository
    colec_repo: IColeccionRepository
    session: Session | None

    def __enter__(self) -> 'IUnitOfWork':
        pass

    def __exit__(self, exc_type, exc, tb) -> None:
        pass


    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

UowFactory = Callable[[], IUnitOfWork]