from sqlalchemy import Integer, String, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base


class SimulacionORM(Base):
    __tablename__ = 'simulacion'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    coleccion_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('coleccion_simulaciones.id'),
        nullable=False
    )

    coleccion = relationship(
        "ColeccionORM",
        back_populates="simulaciones"
    )

    hora: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    evento: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    rnd_llegada: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    tiempo_entre_llegadas: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    proxima_llegada: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    estado_tecnico: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    rnd_duracion_atencion: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    duracion_atencion: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    proximo_fin_atencion: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    rnd_presupuesto: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    presupuesto: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    rnd_deja_equipo: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    deja_equipo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True
    )

    rnd_duracion_reparacion: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    duracion_reparacion: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    fila_atencion_cantidad: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    fila_equipos_cantidad: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    tiempo_de_atencion_total: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    tiempo_de_reparacion_total: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    clientes_no_atendidos: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    clientes: Mapped[list[dict]] = mapped_column(
        JSON,
        nullable=True
    )

    equipos: Mapped[list[dict]] = mapped_column(
        JSON,
        nullable=True
    )