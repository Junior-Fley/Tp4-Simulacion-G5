from app.application.ports.Simulacion_repository import ISimulacionRepository
from app.domain.models.ColaFIFO import ColaFIFO


class ConsoleTestRepo(ISimulacionRepository):
    def __init__(self):
        pass

    def guardar_fila(self, hora: str, evento: str, rnd_llegada: float, tiempo_entre_llegadas: str,
                     hora_proxima_llegada: str, estado_tecnico: str, rnd_atencion: float, duracion_atencion: str,
                     proximo_fin_atencion: str, rnd_presupuesto: float, presupuesto: str, rnd_acepta_reparar: float,
                     deja_para_reparar: bool|None, rnd_reparacion: float, duracion_reparacion: str,
                     cola_atencion_cantidad: int, cola_equipos_cantidad: int, tiempo_atencion_acum: str, tiempo_reparacion_acum: str,
                     clientes_no_atendidos_por_cierre: int, cola_clientes: ColaFIFO, cola_equipos: ColaFIFO) -> None:
        headers = [
            "hora", "evento", "rnd_llegada", "tiempo_entre_llegadas", "próxima_llegada",
            "estado_técnico", "rnd_duración_atención", "Duración atención", "proximo_fin_atención", "rnd_presupuesto",
            "presupuesto", "rnd_deja_para_reparar", "deja_para_reparar", "rnd_duración_reparación", "duración_reparación",
            "cola_atención_cantidad", "cola_equipos_cantidad", "Tiempo_de_Atención", "Tiempo_de_reparación",
            "clientes_no_atendidos_por_cierre", "cola_clientes", "cola_equipos"
        ]

        values = [
            hora, evento, rnd_llegada, tiempo_entre_llegadas, hora_proxima_llegada, estado_tecnico,
            rnd_atencion, duracion_atencion, proximo_fin_atencion, rnd_presupuesto, presupuesto,
            rnd_acepta_reparar, deja_para_reparar, rnd_reparacion, duracion_reparacion,
            cola_atencion_cantidad, cola_equipos_cantidad, tiempo_atencion_acum, tiempo_reparacion_acum,
            clientes_no_atendidos_por_cierre, cola_clientes, cola_equipos
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


    # region Métodos específicos para cada tipo de(para no repetir argumentos evento innecesarios)

    def guardar_llega_cliente_atiende(self, hora: str, evento: str, rnd_llegada: float, tiempo_hasta_llegada: str,
                                      proxima_llegada: str, estado_tecnico: str, rnd_atencion: float,
                                      duracion_atencion: str, proximo_fin_atencion: str,
                                      cola_atencion_cantidad: int, cola_equipos_cantidad: int, tiempo_atencion_acum,
                                      tiempo_reparacion_acum,
                                      clientes_no_atendidos_por_cierre: int, cola_clientes: ColaFIFO,
                                      cola_equipos: ColaFIFO) -> None:
        self.guardar_fila(hora, evento, rnd_llegada, tiempo_hasta_llegada, proxima_llegada, estado_tecnico,
                          rnd_atencion, duracion_atencion, proximo_fin_atencion, -1, '', -1,
                          None, -1, '', cola_atencion_cantidad, cola_equipos_cantidad,
                          tiempo_atencion_acum, tiempo_reparacion_acum, clientes_no_atendidos_por_cierre,
                          cola_clientes, cola_equipos)

    def guardar_llega_cliente_no_atiende(self, hora: str, evento: str, rnd_llegada: float, tiempo_hasta_llegada: str,
                                         proxima_llegada: str, estado_tecnico: str, proximo_fin_atencion: str,
                                         cola_atencion_cantidad: int,
                                         cola_equipos_cantidad: int, tiempo_atencion_acum, tiempo_reparacion_acum,
                                         clientes_no_atendidos_por_cierre: int, cola_clientes: ColaFIFO,
                                         cola_equipos: ColaFIFO) -> None:
        self.guardar_fila(hora, evento, rnd_llegada, tiempo_hasta_llegada, proxima_llegada, estado_tecnico,
                          -1, '', proximo_fin_atencion, -1, '', -1,
                          None, -1, '', cola_atencion_cantidad, cola_equipos_cantidad,
                          tiempo_atencion_acum, tiempo_reparacion_acum, clientes_no_atendidos_por_cierre,
                          cola_clientes, cola_equipos)

    def guardar_fin_atencion_hay_clientes(self, hora: str, evento: str, hora_proxima_llegada: str, estado_tecnico: str,
                                          rnd_atencion: float, duracion_atencion, proximo_fin_atencion: str,
                                          rnd_presupuesto: float, presupuesto: str,
                                          acepta_reparar: float, deja_para_reparar: bool | None,
                                          cola_atencion_cantidad: int,
                                          cola_equipos_cantidad: int, tiempo_atencion_acum, tiempo_reparacion_acum,
                                          clientes_no_atendidos_por_cierre: int, cola_clientes: ColaFIFO,
                                          cola_equipos: ColaFIFO) -> None:
        self.guardar_fila(hora, evento, -1,
                          '', hora_proxima_llegada,
                          estado_tecnico, rnd_atencion, duracion_atencion,
                          proximo_fin_atencion, rnd_presupuesto,
                          presupuesto, acepta_reparar, deja_para_reparar, -1, '',
                          cola_atencion_cantidad, cola_equipos_cantidad,
                          tiempo_atencion_acum, tiempo_reparacion_acum, clientes_no_atendidos_por_cierre,
                          cola_clientes, cola_equipos)

    def guardar_fin_atencion_no_hay_clientes(self, hora: str, evento: str,
                                             hora_proxima_llegada: str, estado_tecnico: str, rnd_presupuesto: float,
                                             presupuesto: str, acepta_reparar: bool | None,
                                             deja_para_reparar: bool | None, cola_atencion_cantidad: int,
                                             cola_equipos_cantidad: int,
                                             tiempo_atencion_acum, tiempo_reparacion_acum,
                                             clientes_no_atendidos_por_cierre: int, cola_clientes: ColaFIFO,
                                             cola_equipos: ColaFIFO) -> None:
        self.guardar_fila(hora, evento, -1,
                          '', hora_proxima_llegada,
                          estado_tecnico, -1, '', '', rnd_presupuesto,
                          presupuesto, acepta_reparar, deja_para_reparar, -1, '',
                          cola_atencion_cantidad, cola_equipos_cantidad,
                          tiempo_atencion_acum, tiempo_reparacion_acum, clientes_no_atendidos_por_cierre,
                          cola_clientes, cola_equipos)

    def guardar_fin_atencion_hay_equipos(self, hora: str, evento: str, hora_proxima_llegada: str, estado_tecnico: str,
                                         rnd_presupuesto: float, presupuesto: str, acepta_reparar: bool | None,
                                         deja_para_reparar: bool | None, rnd_reparacion: float,
                                         duracion_reparacion: str,
                                         cola_atencion_cantidad: int, cola_equipos_cantidad: int, tiempo_atencion_acum,
                                         tiempo_reparacion_acum,
                                         clientes_no_atendidos_por_cierre: int, cola_clientes: ColaFIFO,
                                         cola_equipos: ColaFIFO) -> None:
        self.guardar_fila(hora, evento, -1, '',
                          hora_proxima_llegada,
                          estado_tecnico, -1, '', '', rnd_presupuesto, presupuesto,
                          acepta_reparar,
                          deja_para_reparar,
                          rnd_reparacion, duracion_reparacion,
                          cola_atencion_cantidad, cola_equipos_cantidad,
                          tiempo_atencion_acum, tiempo_reparacion_acum, clientes_no_atendidos_por_cierre,
                          cola_clientes, cola_equipos)

    def guardar_fin_reparacion_no_hay_equipos(self, hora: str, evento: str, hora_proxima_llegada: str,
                                              estado_tecnico: str,
                                              cola_atencion_cantidad: int, cola_equipos_cantidad: int,
                                              tiempo_atencion_acum, tiempo_reparacion_acum,
                                              clientes_no_atendidos_por_cierre: int, cola_clientes: ColaFIFO,
                                              cola_equipos: ColaFIFO) -> None:
        self.guardar_fila(hora, evento, -1,
                          '', hora_proxima_llegada,
                          estado_tecnico, -1, '', '', -1,
                          '', -1, None, -1, '',
                          cola_atencion_cantidad, cola_equipos_cantidad,
                          tiempo_atencion_acum, tiempo_reparacion_acum, clientes_no_atendidos_por_cierre,
                          cola_clientes, cola_equipos)

    def guardar_fin_reparacion_hay_equipos(self, hora: str, evento: str,
                                           hora_proxima_llegada: str, estado_tecnico: str,
                                           rnd_reparacion: float, duracion_reparacion: str,
                                           cola_atencion_cantidad: int, cola_equipos_cantidad: int,
                                           tiempo_atencion_acum, tiempo_reparacion_acum,
                                           clientes_no_atendidos_por_cierre: int, cola_clientes: ColaFIFO,
                                           cola_equipos: ColaFIFO) -> None:
        self.guardar_fila(hora, evento, -1,
                          '', hora_proxima_llegada,
                          estado_tecnico, -1, '', '', -1,
                          '', -1, None, rnd_reparacion, duracion_reparacion,
                          cola_atencion_cantidad, cola_equipos_cantidad,
                          tiempo_atencion_acum, tiempo_reparacion_acum, clientes_no_atendidos_por_cierre,
                          cola_clientes, cola_equipos)

    # endregion