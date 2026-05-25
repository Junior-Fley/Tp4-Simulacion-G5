from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base


class ColeccionORM(Base):
    __tablename__ = 'coleccion_simulaciones'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    simulaciones = relationship(
        "SimulacionORM",
        back_populates="coleccion"
    )