from typing import Iterable, Tuple, Any

from app.application.ports.Simulacion_repository import ISimulacionRepository
from app.domain.models.Colas.ColaFIFO import ColaFIFO


class ConsoleTestRepo(ISimulacionRepository):
    def __init__(self):
        pass

    def guardar_fila(self,coleccion_id, hora: str, evento: str, rnd_llegada: float, tiempo_entre_llegadas: str,
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

    def guardar_filas_bulk(
            self,
            filas: Iterable[
                Tuple[
                    int, str, str, float, str, str, str, float, str, str,
                    float, str, float, bool | None, float, str, int, int,
                    str, str, int, Any, Any
                ]
            ]
    ) -> None:
        headers = [
            "hora", "evento", "rnd_llegada", "tiempo_entre_llegadas", "próxima_llegada",
            "estado_técnico", "rnd_duración_atención", "Duración atención", "proximo_fin_atención",
            "rnd_presupuesto", "presupuesto", "rnd_deja_para_reparar", "deja_para_reparar",
            "rnd_duración_reparación", "duración_reparación", "cola_atención_cantidad",
            "cola_equipos_cantidad", "Tiempo_de_Atención", "Tiempo_de_reparación",
            "clientes_no_atendidos_por_cierre", "cola_clientes", "cola_equipos"
        ]

        filas_materializadas = list(filas)

        if not filas_materializadas:
            print()
            print("No hay filas para guardar en bulk.")
            print()
            return

        filas_str = []

        for fila in filas_materializadas:
            (
                coleccion_id,
                hora,
                evento,
                rnd_llegada,
                tiempo_entre_llegadas,
                hora_proxima_llegada,
                estado_tecnico,
                rnd_atencion,
                duracion_atencion,
                proximo_fin_atencion,
                rnd_presupuesto,
                presupuesto,
                rnd_acepta_reparar,
                deja_para_reparar,
                rnd_reparacion,
                duracion_reparacion,
                cola_atencion_cantidad,
                cola_equipos_cantidad,
                tiempo_atencion_acum,
                tiempo_reparacion_acum,
                clientes_no_atendidos_por_cierre,
                cola_clientes,
                cola_equipos,
            ) = fila

            values = [
                hora,
                evento,
                rnd_llegada,
                tiempo_entre_llegadas,
                hora_proxima_llegada,
                estado_tecnico,
                rnd_atencion,
                duracion_atencion,
                proximo_fin_atencion,
                rnd_presupuesto,
                presupuesto,
                rnd_acepta_reparar,
                deja_para_reparar,
                rnd_reparacion,
                duracion_reparacion,
                cola_atencion_cantidad,
                cola_equipos_cantidad,
                tiempo_atencion_acum,
                tiempo_reparacion_acum,
                clientes_no_atendidos_por_cierre,
                cola_clientes,
                cola_equipos,
            ]

            str_values = ["" if value is None else str(value) for value in values]
            filas_str.append(str_values)

        widths = [
            max(len(header), *(len(fila[i]) for fila in filas_str))
            for i, header in enumerate(headers)
        ]

        def build_separator() -> str:
            return "+" + "+".join("-" * (width + 2) for width in widths) + "+"

        def build_row(items: list[str]) -> str:
            cells = [
                f" {item}{' ' * (width - len(item))} "
                for item, width in zip(items, widths)
            ]
            return "|" + "|".join(cells) + "|"

        print()
        print(f"Guardando {len(filas_str)} filas en bulk:")
        print(build_separator())
        print(build_row(headers))
        print(build_separator())

        for fila_str in filas_str:
            print(build_row(fila_str))

        print(build_separator())
        print()