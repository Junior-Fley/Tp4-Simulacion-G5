from typing import Optional

from app.infrastructure.database.models.Simulacion_ORM import SimulacionORM
from app.domain.models.Simulacion import Simulacion


class SimulacionMapper:
    @staticmethod
    def convert_orm_to_domain(orm: Optional[SimulacionORM]) -> Optional[Simulacion]:
        if orm is None:
            return None

        return Simulacion(
            simu_id=orm.id,
            hora=orm.hora,
            evento=orm.evento,
            rnd_llegada=orm.rnd_llegada,
            tiempo_entre_llegadas=orm.tiempo_entre_llegadas,
            proxima_llegada=orm.proxima_llegada,
            estado_tecnico=orm.estado_tecnico,
            rnd_duracion_atencion=orm.rnd_duracion_atencion,
            duracion_atencion=orm.duracion_atencion,
            proximo_fin_atencion=orm.proximo_fin_atencion,
            rnd_presupuesto=orm.rnd_presupuesto,
            presupuesto=orm.presupuesto,
            rnd_deja_equipo=orm.rnd_deja_equipo,
            deja_equipo=orm.deja_equipo,
            rnd_duracion_reparacion=orm.rnd_duracion_reparacion,
            duracion_reparacion=orm.duracion_reparacion,
            fila_atencion_cantidad=orm.fila_atencion_cantidad,
            fila_equipos_cantidad=orm.fila_equipos_cantidad,
            tiempo_de_atencion_total=orm.tiempo_de_atencion_total,
            tiempo_de_reparacion_total=orm.tiempo_de_reparacion_total,
            clientes_no_atendidos=orm.clientes_no_atendidos,
        )
