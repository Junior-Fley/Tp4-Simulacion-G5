from typing import Callable, Protocol
from sqlalchemy.orm import Session

from app.application.ports.Simulacion_repository import ISimulacionRepository

SessionFactory = Callable[[], Session]

class IUnitOfWork(Protocol):

    simu_repo: ISimulacionRepository
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