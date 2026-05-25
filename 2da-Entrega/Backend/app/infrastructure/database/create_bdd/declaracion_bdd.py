from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class ColeccionSimulaciones(Base):
    __tablename__ = 'coleccion_simulaciones'

    id = Column(Integer, primary_key=True)

    simulaciones = relationship(
        "Simulacion",
        back_populates="coleccion",
        cascade="all, delete-orphan"
    )


class Simulacion(Base):
    __tablename__ = 'simulacion'

    id = Column(Integer, primary_key=True)
    coleccion_id = Column(Integer, ForeignKey('coleccion_simulaciones.id'), nullable=False)

    coleccion = relationship(
        "ColeccionSimulaciones",
        back_populates="simulaciones"
    )
    hora = Column(String)
    evento = Column(String)
    rnd_llegada = Column(Float)
    tiempo_entre_llegadas = Column(String)
    proxima_llegada = Column(String)
    estado_tecnico = Column(String)
    rnd_duracion_atencion = Column(Float)
    duracion_atencion = Column(String)
    proximo_fin_atencion = Column(String)
    rnd_presupuesto = Column(Float)
    presupuesto = Column(String)
    rnd_deja_equipo = Column(Float)
    deja_equipo = Column(Boolean)
    rnd_duracion_reparacion = Column(Float)
    duracion_reparacion = Column(String)
    fila_atencion_cantidad = Column(Integer)
    fila_equipos_cantidad = Column(Integer)
    tiempo_de_atencion_total = Column(String)
    tiempo_de_reparacion_total = Column(String)
    clientes_no_atendidos = Column(Integer)
    clientes = Column(JSON)
    equipos = Column(JSON)


class Clientes(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    estado = Column(String)
    hora_llegada = Column(Float)
    hora_inicio_atencion = Column(Float)
    hora_fin_atencion = Column(Float)

class Equipos(Base):
    __tablename__ = 'equipos'

    id = Column(Integer, primary_key=True)
    estado = Column(String)
    hora_ingreso_taller = Column(Float)
    hora_inicio_reparacion = Column(Float)
    hora_fin_reparacion = Column(Float)
    tiempo_de_reparacion = Column(Float)
    tiempo_de_reparacion_acumulado = Column(Float)
    tiempo_de_reparacion_restantes = Column(Float)