from app.domain.models.Equipo import Equipo
from app.domain.models.EstadoTecnico import EstadoTecnico


class Tecnico:
    def __init__(self, estado: EstadoTecnico, equipo_asignado: Equipo|None, acum_recepcion: float, acum_reparacion: float):
        self.estado: EstadoTecnico = estado
        self.equipo_asignado = equipo_asignado
        self.acum_recepcion: float = acum_recepcion # representa tiempo en decimal de minutos, debe convertirse a minutos para el reporte final
        self.acum_reparacion: float = acum_reparacion # representa tiempo en decimal de minutos, debe convertirse a minutos para el reporte final

    @staticmethod
    def _convertir_minutos_a_mmss(tiempo: float) -> str:
        # este mét-odo convierte un tiempo en minutos (con decimales) a formato MM:SS
        # así por ejemplo se pasa de 18.5 minutos a "18:30"

        minutos = int(tiempo)
        segundos = int((tiempo - minutos) * 60)

        return f"{minutos:02d}:{segundos:02d}"

    def obtener_tiempo_acumulado_reparacion(self):
        return self._convertir_minutos_a_mmss(self.acum_reparacion)

    def obtener_tiempo_acumulado_recepcion(self):
        return self._convertir_minutos_a_mmss(self.acum_recepcion)
