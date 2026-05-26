from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base


class AcumEquiposORM(Base):
    __tablename__ = 'acum_equipos'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    acumulador: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    contador: Mapped[float] = mapped_column(
        Integer,
        nullable=True
    )

    coleccion_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('coleccion_simulaciones.id'),
        nullable=False
    )

    coleccion = relationship(
        "ColeccionORM",
        back_populates="acumuladores"
    )