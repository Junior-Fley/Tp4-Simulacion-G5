from typing import Iterable, Tuple

from app.application.ports.Simulacion_repository import ISimulacionRepository
from app.domain.models.ColaFIFO import ColaFIFO


class FakeRepo(ISimulacionRepository):
    def __init__(self):
        pass

    def guardar_fila(self,coleccion_id, hora: str, evento: str, rnd_llegada: float, tiempo_entre_llegadas: str,
                     hora_proxima_llegada: str, estado_tecnico: str, rnd_atencion: float, duracion_atencion: str,
                     proximo_fin_atencion: str, rnd_presupuesto: float, presupuesto: str, rnd_acepta_reparar: float,
                     deja_para_reparar: bool|None, rnd_reparacion: float, duracion_reparacion: str,
                     cola_atencion_cantidad: int, cola_equipos_cantidad: int, tiempo_atencion_acum: str, tiempo_reparacion_acum: str,
                     clientes_no_atendidos_por_cierre: int, cola_clientes: ColaFIFO, cola_equipos: ColaFIFO) -> None:
        pass

    def guardar_filas_bulk(self, filas: Iterable[Tuple[int, str, str, float, str, str, str, float, str, str,
    float, str, float, bool | None, float, str, int, int, str, str, int, any, any]]
                           ) -> None:
        pass