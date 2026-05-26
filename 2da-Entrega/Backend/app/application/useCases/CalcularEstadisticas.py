from app.infrastructure.database.unit_of_work.unit_of_work_impl import UowFactory
from app.application.ports.Simulacion_repository import ISimulacionRepository
from app.domain.services.float_a_hora_service import float_a_hora
from app.domain.services.truncar_service import truncar_a_decimales


class CalcularEstadisticas:
    def __init__(self, coleccion_id: int, uow_factory: UowFactory, repo_override: ISimulacionRepository | None = None):
        self.coleccion_id = coleccion_id
        self.uow_factory = uow_factory
        self.repo_override = repo_override
        self.tiempo_atencion_total = ''
        self.tiempo_reparacion_total = ''

    def calcular_estadisticas(self) -> dict:
        with self.uow_factory() as uow:
            if self.repo_override is not None:
                uow.simu_repo = self.repo_override

            ultima_fila = uow.simu_repo.obtener_ultima_fila_simulacion(self.coleccion_id)
            if ultima_fila is None:
                raise ValueError(f"Simulación id {self.coleccion_id} no encontrada")

            acumulador_data = uow.acum_repo.obtener_acumulador(self.coleccion_id)

            clientes_no_atendidos = int(ultima_fila.clientes_no_atendidos or 0)
            self.tiempo_atencion_total = ultima_fila.tiempo_de_atencion_total
            self.tiempo_reparacion_total = ultima_fila.tiempo_de_reparacion_total


        promedio_permanencia_minutos = 0.0
        if acumulador_data is not None:
            acumulador, contador = acumulador_data
            if contador > 0:
                promedio_permanencia_minutos = acumulador / contador

        promedio_permanencia = float_a_hora(promedio_permanencia_minutos)

        tiempo_atencion_total = self._hora_a_minutos(self.tiempo_atencion_total)
        tiempo_reparacion_total = self._hora_a_minutos(self.tiempo_reparacion_total)
        total_tecnico = tiempo_atencion_total + tiempo_reparacion_total

        porcentaje_recepcion = 0.0
        porcentaje_reparacion = 0.0
        if total_tecnico > 0:
            porcentaje_recepcion = (tiempo_atencion_total / total_tecnico) * 100
            porcentaje_reparacion = (tiempo_reparacion_total / total_tecnico) * 100

        return {
            "clientes_no_atendidos": clientes_no_atendidos,
            "promedio_permanencia_equipo": promedio_permanencia,
            "porcentaje_tiempo_recepcion": truncar_a_decimales(porcentaje_recepcion, 2),
            "porcentaje_tiempo_reparacion": truncar_a_decimales(porcentaje_reparacion, 2),
        }

    @staticmethod
    def _hora_a_minutos(valor: str | None) -> float:
        if not valor:
            return 0.0

        partes = valor.split(":")
        if len(partes) != 3:
            return 0.0

        horas, minutos, segundos = partes
        try:
            return int(horas) * 60 + int(minutos) + int(segundos) / 60.0
        except ValueError:
            return 0.0
