from pydantic import BaseModel, Field

class SimularRequest(BaseModel):
    x_tiempo: float = Field(..., gt=0, description="Tiempo de simulación en minutos (>0)")
    i_iteraciones: int = Field(..., gt=0, description="Cantidad de iteraciones (>0)")
    j_hora_inicio: float = Field(600, description="Hora inicio en minutos (default 600 = 10:00)")