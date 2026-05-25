from sqlalchemy.orm import Session
from app.application.ports.Simulacion_repository import ISimulacionRepository
from app.domain.models.ColaFIFO import ColaFIFO
from app.infrastructure.database.models.Simulacion_ORM import SimulacionORM

class SimulacionRepositoryImpl(ISimulacionRepository):
    def __init__(self, session: Session):
        self.session = session
        self._buffer: list[dict] = []  # acumulador en memoria

    def guardar_fila(self, coleccion_id: int, hora: str, evento: str, rnd_llegada: float, tiempo_entre_llegadas: str,
                     hora_proxima_llegada: str, estado_tecnico: str, rnd_atencion: float, duracion_atencion: str,
                     proximo_fin_atencion: str, rnd_presupuesto: float, presupuesto: str, rnd_acepta_reparar: float,
                     deja_para_reparar: bool|None, rnd_reparacion: float, duracion_reparacion: str,
                     cola_atencion_cantidad: int, cola_equipos_cantidad: int, tiempo_atencion_acum: str, tiempo_reparacion_acum: str,
                     clientes_no_atendidos_por_cierre: int, cola_clientes: ColaFIFO, cola_equipos: ColaFIFO) -> None:

        # simulacion = SimulacionORM(coleccion_id=coleccion_id,
        #                            hora=hora,
        #                            evento=evento,
        #                            rnd_llegada=rnd_llegada,
        #                            tiempo_entre_llegadas=tiempo_entre_llegadas,
        #                            proxima_llegada=hora_proxima_llegada,
        #                            estado_tecnico=estado_tecnico,
        #                            rnd_duracion_atencion=rnd_atencion,
        #                            duracion_atencion=duracion_atencion,
        #                            proximo_fin_atencion=proximo_fin_atencion,
        #                            rnd_presupuesto=rnd_presupuesto,
        #                            presupuesto=presupuesto,
        #                            rnd_deja_equipo=rnd_acepta_reparar,
        #                            deja_equipo=deja_para_reparar,
        #                            rnd_duracion_reparacion=rnd_reparacion,
        #                            duracion_reparacion=duracion_reparacion,
        #                            fila_atencion_cantidad=cola_atencion_cantidad,
        #                            fila_equipos_cantidad=cola_equipos_cantidad,
        #                            tiempo_de_atencion_total=tiempo_atencion_acum,
        #                            tiempo_de_reparacion_total=tiempo_reparacion_acum,
        #                            clientes_no_atendidos=clientes_no_atendidos_por_cierre)
        #
        # self.session.add(simulacion)
        # self.session.flush()
        # Solo acumula en memoria, no toca la base de datos

        self._buffer.append(dict(
            coleccion_id=coleccion_id,
            hora=hora,
            evento=evento,
            rnd_llegada=rnd_llegada,
            tiempo_entre_llegadas=tiempo_entre_llegadas,
            proxima_llegada=hora_proxima_llegada,
            estado_tecnico=estado_tecnico,
            rnd_duracion_atencion=rnd_atencion,
            duracion_atencion=duracion_atencion,
            proximo_fin_atencion=proximo_fin_atencion,
            rnd_presupuesto=rnd_presupuesto,
            presupuesto=presupuesto,
            rnd_deja_equipo=rnd_acepta_reparar,
            deja_equipo=deja_para_reparar,
            rnd_duracion_reparacion=rnd_reparacion,
            duracion_reparacion=duracion_reparacion,
            fila_atencion_cantidad=cola_atencion_cantidad,
            fila_equipos_cantidad=cola_equipos_cantidad,
            tiempo_de_atencion_total=tiempo_atencion_acum,
            tiempo_de_reparacion_total=tiempo_reparacion_acum,
            clientes_no_atendidos=clientes_no_atendidos_por_cierre,
        ))

    def flush_buffer(self) -> None:
        # Inserta todo de una sola vez y limpia el buffer
        if not self._buffer:
            return
        self.session.bulk_insert_mappings(SimulacionORM, self._buffer)
        self._buffer.clear()

    def obtener_filas_simulacion(self, coleccion_id: int, page: int, size: int):
        query = self.session.query(SimulacionORM).filter_by(coleccion_id=coleccion_id)
        total = query.count()
        items = query.order_by(SimulacionORM.id).offset((page - 1) * size).limit(size).all()
        return items, total
