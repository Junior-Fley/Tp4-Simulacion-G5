from pydantic import BaseModel, Field

class SimularRequest(BaseModel):
    x_tiempo: float = Field(..., gt=0, description="Tiempo de simulación en minutos (>0)")
    i_iteraciones: int = Field(..., gt=0, description="Cantidad de iteraciones (>0)")
    j_hora_inicio: float = Field(600, description="Hora inicio en minutos (default 600 = 10:00)")

    # Parámetros de distribuciones
    media_llegada: float = Field(45, gt=0, description="Media de llegadas (distribución exponencial) en minutos")
    min_atencion: float = Field(10, ge=0, description="Tiempo mínimo de atención al cliente en minutos")
    max_atencion: float = Field(20, ge=0, description="Tiempo máximo de atención al cliente en minutos")
    media_reparacion: float = Field(90, gt=0, description="Media de reparación (distribución exponencial) en minutos")
