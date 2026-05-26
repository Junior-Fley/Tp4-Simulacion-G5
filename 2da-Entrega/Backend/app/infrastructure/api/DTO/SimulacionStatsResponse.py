from pydantic import BaseModel


class SimulacionStatsResponse(BaseModel):
    clientes_no_atendidos: int
    promedio_permanencia_equipo: str
    porcentaje_tiempo_recepcion: float
    porcentaje_tiempo_reparacion: float
