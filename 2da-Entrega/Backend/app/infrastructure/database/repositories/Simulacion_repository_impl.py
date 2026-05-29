from sqlalchemy.orm import Session
from app.application.ports.Simulacion_repository import ISimulacionRepository
from app.infrastructure.database.models.Simulacion_ORM import SimulacionORM
from sqlalchemy import insert

class SimulacionRepositoryImpl(ISimulacionRepository):
    def __init__(self, session: Session):
        self.session = session

    def guardar_fila(self, coleccion_id: int, hora: str, evento: str, rnd_llegada: float, tiempo_entre_llegadas: str,
                     hora_proxima_llegada: str, estado_tecnico: str, rnd_atencion: float, duracion_atencion: str,
                     proximo_fin_atencion: str, rnd_presupuesto: float, presupuesto: str, rnd_acepta_reparar: float,
                     deja_para_reparar: bool|None, rnd_reparacion: float, duracion_reparacion: str,
                     cola_atencion_cantidad: int, cola_equipos_cantidad: int, tiempo_atencion_acum: str, tiempo_reparacion_acum: str,
                     clientes_no_atendidos_por_cierre: int, cola_clientes: list[dict], cola_equipos: list[dict]) -> None:

        simulacion = SimulacionORM(coleccion_id=coleccion_id,
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
                                   clientes=cola_clientes,
                                   equipos=cola_equipos)

        self.session.add(simulacion)

    def obtener_filas_simulacion(self, coleccion_id: int, page: int, size: int):
        query = self.session.query(SimulacionORM).filter_by(coleccion_id=coleccion_id)
        total = query.count()
        items = query.order_by(SimulacionORM.id).offset((page - 1) * size).limit(size).all()
        return items, total

    def obtener_filas_simulacion_filtradas(self, coleccion_id: int, hora_min: str, page: int, size: int):
        query = (
            self.session.query(SimulacionORM)
            .filter(
                SimulacionORM.coleccion_id == coleccion_id,
                SimulacionORM.hora > hora_min,
            )
        )
        total = query.count()
        items = query.order_by(SimulacionORM.id).offset((page - 1) * size).limit(size).all()
        return items, total

    def obtener_ultima_fila_simulacion(self, coleccion_id: int):
        return (
            self.session.query(SimulacionORM)
            .filter_by(coleccion_id=coleccion_id)
            .order_by(SimulacionORM.id.desc())
            .first()
        )

    def guardar_filas_bulk(self, filas) -> None:
        filas_dict = [
            {
                "coleccion_id": f[0],
                "hora": f[1],
                "evento": f[2],
                "rnd_llegada": f[3],
                "tiempo_entre_llegadas": f[4],
                "proxima_llegada": f[5],
                "estado_tecnico": f[6],
                "rnd_duracion_atencion": f[7],
                "duracion_atencion": f[8],
                "proximo_fin_atencion": f[9],
                "rnd_presupuesto": f[10],
                "presupuesto": f[11],
                "rnd_deja_equipo": f[12],
                "deja_equipo": f[13],
                "rnd_duracion_reparacion": f[14],
                "duracion_reparacion": f[15],
                "fila_atencion_cantidad": f[16],
                "fila_equipos_cantidad": f[17],
                "tiempo_de_atencion_total": f[18],
                "tiempo_de_reparacion_total": f[19],
                "clientes_no_atendidos": f[20],
                "clientes": f[21],
                "equipos": f[22],
            }
            for f in filas
        ]

        if not filas_dict:
            return

        self.session.execute(
            insert(SimulacionORM.__table__),
            filas_dict
        )