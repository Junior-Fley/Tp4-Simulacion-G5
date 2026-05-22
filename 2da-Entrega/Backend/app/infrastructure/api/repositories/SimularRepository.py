from typing import List, Dict, Any, Optional
from app.application.ports.Simular_repository import ISimulacionRepository

class SimularRepository(ISimulacionRepository):
    """
    Repositorio en memoria para una sola simulación.
    La idea es instanciar una instancia por simulación y guardarla en un dict global en el controller.
    """

    def __init__(self):
        self.rows: List[Dict[str, Any]] = []

    def _append(self, **kwargs) -> None:
        # Este mét-odo normaliza qué campos guardamos. Podés ampliarlo según lo que necesites.
        row = {
            "hora": kwargs.get("hora"),
            "evento": kwargs.get("evento"),
            "estado_tecnico": kwargs.get("estado_tecnico"),
            "rnd_llegada": kwargs.get("rnd_llegada"),
            "rnd_atencion": kwargs.get("rnd_atencion"),
            "rnd_presupuesto": kwargs.get("rnd_presupuesto"),
            "rnd_reparacion": kwargs.get("rnd_reparacion"),
            "cola_atencion_cantidad": kwargs.get("cola_atencion_cantidad"),
            "cola_equipos_cantidad": kwargs.get("cola_equipos_cantidad"),
        }
        self.rows.append(row)

    # Implementación de los métodos definidos en ISimulacionRepository
    def guardar_fila(self, hora: str, evento: str, rnd_llegada: float, tiempo_hasta_llegada: str,
                     hora_proxima_llegada: str, estado_tecnico: str, rnd_atencion: float,
                     proximo_fin_atencion: str, rnd_presupuesto: float, presupuesto: str, acepta_reparar: Optional[bool],
                     deja_para_reparar: Optional[bool], rnd_reparacion: float, duracion_reparacion: str,
                     cola_atencion_cantidad: int, cola_equipos_cantidad: int, clientes_no_atendidos_por_cierre: int,
                     cola_clientes, cola_equipos) -> None:
        self._append(hora=hora, evento=evento, estado_tecnico=estado_tecnico,
                     rnd_llegada=rnd_llegada, rnd_atencion=rnd_atencion,
                     rnd_presupuesto=rnd_presupuesto, rnd_reparacion=rnd_reparacion,
                     cola_atencion_cantidad=cola_atencion_cantidad, cola_equipos_cantidad=cola_equipos_cantidad)

    def guardar_llega_cliente_atiende(self, hora: str, evento: str, rnd_llegada: float, tiempo_hasta_llegada: str,
                                      proxima_llegada: str, estado_tecnico: str, rnd_atencion: float, proximo_fin_atencion: str,
                                      cola_atencion_cantidad: int, cola_equipos_cantidad: int, clientes_no_atendidos_por_cierre: int,
                                      cola_clientes, cola_equipos) -> None:
        self._append(hora=hora, evento=evento, estado_tecnico=estado_tecnico,
                     rnd_llegada=rnd_llegada, rnd_atencion=rnd_atencion,
                     cola_atencion_cantidad=cola_atencion_cantidad, cola_equipos_cantidad=cola_equipos_cantidad)

    def guardar_llega_cliente_no_atiende(self, hora: str, evento: str, rnd_llegada: float, tiempo_hasta_llegada: str,
                                         proxima_llegada: str, estado_tecnico: str, cola_atencion_cantidad: int,
                                         cola_equipos_cantidad: int, clientes_no_atendidos_por_cierre: int,
                                         cola_clientes, cola_equipos) -> None:
        self._append(hora=hora, evento=evento, estado_tecnico=estado_tecnico,
                     rnd_llegada=rnd_llegada, cola_atencion_cantidad=cola_atencion_cantidad,
                     cola_equipos_cantidad=cola_equipos_cantidad)

    def guardar_fin_atencion_hay_clientes(self, hora: str, evento: str, hora_proxima_llegada: str, estado_tecnico: str,
                                          rnd_atencion: float, proximo_fin_atencion: str, rnd_presupuesto: float, presupuesto: str,
                                          acepta_reparar: Optional[bool], deja_para_reparar: Optional[bool], cola_atencion_cantidad: int,
                                          cola_equipos_cantidad: int, clientes_no_atendidos_por_cierre: int,
                                          cola_clientes, cola_equipos) -> None:
        self._append(hora=hora, evento=evento, estado_tecnico=estado_tecnico,
                     rnd_atencion=rnd_atencion, rnd_presupuesto=rnd_presupuesto,
                     cola_atencion_cantidad=cola_atencion_cantidad, cola_equipos_cantidad=cola_equipos_cantidad)

    def guardar_fin_atencion_no_hay_clientes(self, hora: str, evento: str,
                                             hora_proxima_llegada: str, estado_tecnico: str, rnd_presupuesto: float, presupuesto: str, acepta_reparar: Optional[bool],
                                             deja_para_reparar: Optional[bool], cola_atencion_cantidad: int, cola_equipos_cantidad: int,
                                             clientes_no_atendidos_por_cierre: int, cola_clientes, cola_equipos) -> None:
        self._append(hora=hora, evento=evento, estado_tecnico=estado_tecnico,
                     rnd_presupuesto=rnd_presupuesto, cola_atencion_cantidad=cola_atencion_cantidad,
                     cola_equipos_cantidad=cola_equipos_cantidad)

    def guardar_fin_atencion_hay_equipos(self, hora: str, evento: str, hora_proxima_llegada: str, estado_tecnico: str,
                                         rnd_presupuesto: float, presupuesto: str, acepta_reparar: Optional[bool],
                                         deja_para_reparar: Optional[bool], rnd_reparacion: float, duracion_reparacion: str,
                                         cola_atencion_cantidad: int, cola_equipos_cantidad: int, clientes_no_atendidos_por_cierre: int,
                                         cola_clientes, cola_equipos) -> None:
        self._append(hora=hora, evento=evento, estado_tecnico=estado_tecnico,
                     rnd_presupuesto=rnd_presupuesto, rnd_reparacion=rnd_reparacion,
                     cola_atencion_cantidad=cola_atencion_cantidad, cola_equipos_cantidad=cola_equipos_cantidad)

    def guardar_fin_reparacion_no_hay_equipos(self, hora: str, evento: str, hora_proxima_llegada: str, estado_tecnico: str,
                                             cola_atencion_cantidad: int, cola_equipos_cantidad: int, clientes_no_atendidos_por_cierre: int,
                                             cola_clientes, cola_equipos) -> None:
        self._append(hora=hora, evento=evento, estado_tecnico=estado_tecnico,
                     cola_atencion_cantidad=cola_atencion_cantidad, cola_equipos_cantidad=cola_equipos_cantidad)

    def guardar_fin_reparacion_hay_equipos(self, hora: str, evento: str,
                                           hora_proxima_llegada: str, estado_tecnico: str,
                                           rnd_reparacion: float, duracion_reparacion: str,
                                           cola_atencion_cantidad: int, cola_equipos_cantidad: int, clientes_no_atendidos_por_cierre: int,
                                           cola_clientes, cola_equipos) -> None:
        self._append(hora=hora, evento=evento, estado_tecnico=estado_tecnico,
                     rnd_reparacion=rnd_reparacion, cola_atencion_cantidad=cola_atencion_cantidad,
                     cola_equipos_cantidad=cola_equipos_cantidad)

    # Helpers para paginación y consulta
    def total_rows(self) -> int:
        return len(self.rows)

    def get_page(self, page: int, size: int) -> List[Dict[str, Any]]:
        start = (page - 1) * size
        end = start + size
        return self.rows[start:end]