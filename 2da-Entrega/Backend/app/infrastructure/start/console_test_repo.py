from app.application.ports.Simular_repository import ISimulacionRepository
from app.domain.models.ColaFIFO import ColaFIFO


class ConsoleTestRepo(ISimulacionRepository):
    def __init__(self):
        pass

    def guardar_fila(self, hora: str, evento: str, rnd_llegada: float, tiempo_hasta_llegada: str,
                     hora_proxima_llegada: str, estado_tecnico: str, rnd_atencion: float, proximo_fin_atencion: str,
                     rnd_presupuesto: float, presupuesto: str, acepta_reparar: bool | None,
                     deja_para_reparar: bool | None, rnd_reparacion: float, duracion_reparacion: str,
                     cola_atencion_cantidad: int, cola_equipos_cantidad: int, clientes_no_atendidos_por_cierre: int,
                     cola_clientes: ColaFIFO, cola_equipos: ColaFIFO) -> None:
        headers = [
            "hora", "evento", "rnd_llegada", "tiempo_hasta_llegada", "hora_proxima_llegada",
            "estado_tecnico", "rnd_atencion", "proximo_fin_atencion", "rnd_presupuesto", "presupuesto",
            "acepta_reparar", "deja_para_reparar", "rnd_reparacion", "duracion_reparacion",
            "cola_atencion_cantidad", "cola_equipos_cantidad", "clientes_no_atendidos_por_cierre",
            "cola_clientes", "cola_equipos"
        ]

        values = [
            hora, evento, rnd_llegada, tiempo_hasta_llegada, hora_proxima_llegada, estado_tecnico,
            rnd_atencion, proximo_fin_atencion, rnd_presupuesto, presupuesto, acepta_reparar,
            deja_para_reparar, rnd_reparacion, duracion_reparacion, cola_atencion_cantidad,
            cola_equipos_cantidad, clientes_no_atendidos_por_cierre, cola_clientes, cola_equipos
        ]

        str_values = ["" if v is None else str(v) for v in values]
        widths = [max(len(h), len(v)) for h, v in zip(headers, str_values)]

        def build_separator() -> str:
            return "+" + "+".join("-" * (w + 2) for w in widths) + "+"

        def build_row(items) -> str:
            cells = [f" {item}{' ' * (w - len(item))} " for item, w in zip(items, widths)]
            return "|" + "|".join(cells) + "|"

        print()
        print(build_separator())
        print(build_row(headers))
        print(build_separator())
        print(build_row(str_values))
        print(build_separator())
        print()





        """print(f"Hora: {hora}, Evento: {evento}, RND Llegada: {rnd_llegada}, Tiempo hasta llegada: {tiempo_hasta_llegada}, "
              f"Hora próxima llegada: {hora_proxima_llegada}, Estado técnico: {estado_tecnico}, RND Atención: {rnd_atencion}, Próximo fin atención: {proximo_fin_atencion}, "
              f"RND Presupuesto: {rnd_presupuesto}, Presupuesto: {presupuesto}, Acepta reparar: {acepta_reparar}, Deja para reparar: {deja_para_reparar}, RND Reparación: {rnd_reparacion}, Duración reparación: {duracion_reparacion}, "
              f"Cantidad en cola de atención: {cola_atencion_cantidad}, Cantidad en cola de equipos: {cola_equipos_cantidad}, Clientes no atendidos por cierre: {clientes_no_atendidos_por_cierre}, "
              f"Cola de clientes: {cola_clientes}, Cola de equipos: {cola_equipos}")"""





    def guardar_llega_cliente_atiende(self, hora: str, evento: str, rnd_llegada: float, tiempo_hasta_llegada: str,
                     proxima_llegada: str, estado_tecnico: str, rnd_atencion: float, proximo_fin_atencion: str,
                     cola_atencion_cantidad: int, cola_equipos_cantidad: int, clientes_no_atendidos_por_cierre: int,
                     cola_clientes: ColaFIFO, cola_equipos: ColaFIFO) -> None:

        self.guardar_fila(hora, evento, rnd_llegada, tiempo_hasta_llegada, proxima_llegada, estado_tecnico,
                          rnd_atencion, proximo_fin_atencion, -1,'', None,
                          None, -1, '', cola_atencion_cantidad, cola_equipos_cantidad,
                          clientes_no_atendidos_por_cierre,
                          cola_clientes, cola_equipos)


    def guardar_llega_cliente_no_atiende(self, hora: str, evento: str, rnd_llegada: float, tiempo_hasta_llegada: str,
                                      proxima_llegada: str, estado_tecnico: str, cola_atencion_cantidad: int,
                                      cola_equipos_cantidad: int, clientes_no_atendidos_por_cierre: int,
                                      cola_clientes: ColaFIFO, cola_equipos: ColaFIFO) -> None:

        self.guardar_fila(hora, evento, rnd_llegada, tiempo_hasta_llegada, proxima_llegada, estado_tecnico,
                          -1, '', -1, '', None,
                          None, -1, '', cola_atencion_cantidad, cola_equipos_cantidad,
                          clientes_no_atendidos_por_cierre,
                          cola_clientes, cola_equipos)



    def guardar_fin_atencion_hay_clientes(self, hora: str, evento: str, hora_proxima_llegada: str, estado_tecnico: str,
                     rnd_atencion: float, proximo_fin_atencion: str, rnd_presupuesto: float, presupuesto: str,
                     acepta_reparar: bool|None, deja_para_reparar: bool|None, cola_atencion_cantidad: int,
                     cola_equipos_cantidad: int, clientes_no_atendidos_por_cierre: int,
                     cola_clientes: ColaFIFO, cola_equipos: ColaFIFO) -> None:
        self.guardar_fila(hora, evento, -1,
                               '', hora_proxima_llegada,
                               estado_tecnico, rnd_atencion,
                               proximo_fin_atencion, rnd_presupuesto,
                               presupuesto, acepta_reparar, deja_para_reparar, -1, '',
                               cola_atencion_cantidad, cola_equipos_cantidad, clientes_no_atendidos_por_cierre,
                               cola_clientes, cola_equipos)


    def guardar_fin_atencion_no_hay_clientes(self, hora: str, evento: str,
                     hora_proxima_llegada: str, estado_tecnico: str, rnd_presupuesto: float, presupuesto: str, acepta_reparar: bool|None,
                     deja_para_reparar: bool|None, cola_atencion_cantidad: int, cola_equipos_cantidad: int,
                     clientes_no_atendidos_por_cierre: int, cola_clientes: ColaFIFO, cola_equipos: ColaFIFO) -> None:
        self.guardar_fila(hora, evento, -1,
                               '', hora_proxima_llegada,
                               estado_tecnico, -1, '', rnd_presupuesto,
                               presupuesto, acepta_reparar, deja_para_reparar, -1, '',
                               cola_atencion_cantidad, cola_equipos_cantidad, clientes_no_atendidos_por_cierre,
                               cola_clientes, cola_equipos)


    def guardar_fin_atencion_hay_equipos(self, hora: str, evento: str, hora_proxima_llegada: str, estado_tecnico: str,
                     rnd_presupuesto: float, presupuesto: str, acepta_reparar: bool|None,
                     deja_para_reparar: bool|None, rnd_reparacion: float, duracion_reparacion: str,
                     cola_atencion_cantidad: int, cola_equipos_cantidad: int, clientes_no_atendidos_por_cierre: int,
                     cola_clientes: ColaFIFO, cola_equipos: ColaFIFO) -> None:

        self.guardar_fila(hora, evento, -1, '',
                               hora_proxima_llegada,
                               estado_tecnico, -1, '', rnd_presupuesto, presupuesto, acepta_reparar,
                               deja_para_reparar,
                               rnd_reparacion, duracion_reparacion,
                               cola_atencion_cantidad, cola_equipos_cantidad,
                               clientes_no_atendidos_por_cierre, cola_clientes,
                               cola_equipos)


    def guardar_fin_reparacion_no_hay_equipos(self, hora: str, evento: str, hora_proxima_llegada: str, estado_tecnico: str,
                     cola_atencion_cantidad: int, cola_equipos_cantidad: int, clientes_no_atendidos_por_cierre: int,
                     cola_clientes: ColaFIFO, cola_equipos: ColaFIFO) -> None:
        self.guardar_fila(hora, evento, -1,
                               '', hora_proxima_llegada,
                               estado_tecnico, -1, '', -1,
                               '', None, None, -1, '',
                               cola_atencion_cantidad, cola_equipos_cantidad, clientes_no_atendidos_por_cierre,
                               cola_clientes, cola_equipos)


    def guardar_fin_reparacion_hay_equipos(self, hora: str, evento: str,
                     hora_proxima_llegada: str, estado_tecnico: str,
                     rnd_reparacion: float, duracion_reparacion: str,
                     cola_atencion_cantidad: int, cola_equipos_cantidad: int, clientes_no_atendidos_por_cierre: int,
                     cola_clientes: ColaFIFO, cola_equipos: ColaFIFO) -> None:
        self.guardar_fila(hora, evento, -1,
                               '', hora_proxima_llegada,
                               estado_tecnico, -1, '', -1,
                               '', None, None, rnd_reparacion, duracion_reparacion,
                               cola_atencion_cantidad, cola_equipos_cantidad, clientes_no_atendidos_por_cierre,
                               cola_clientes, cola_equipos)