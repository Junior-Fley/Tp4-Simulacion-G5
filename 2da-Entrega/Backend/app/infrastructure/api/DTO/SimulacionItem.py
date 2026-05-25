# python
from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.domain.models.Simulacion import Simulacion

class SimulacionItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hora: Optional[str] = None
    evento: Optional[str] = None
    rnd_llegada: Optional[float] = None
    tiempo_entre_llegadas: Optional[str] = None
    proxima_llegada: Optional[str] = None
    estado_tecnico: Optional[str] = None
    rnd_duracion_atencion: Optional[float] = None
    duracion_atencion: Optional[str] = None
    proximo_fin_atencion: Optional[str] = None
    rnd_presupuesto: Optional[float] = None
    presupuesto: Optional[str] = None
    rnd_deja_equipo: Optional[float] = None
    deja_equipo: Optional[bool] = None
    rnd_duracion_reparacion: Optional[float] = None
    duracion_reparacion: Optional[str] = None
    fila_atencion_cantidad: Optional[int] = None
    fila_equipos_cantidad: Optional[int] = None
    tiempo_de_atencion_total: Optional[str] = None
    tiempo_de_reparacion_total: Optional[str] = None
    clientes_no_atendidos: Optional[int] = None
    clientes: Optional[list] = None
    equipos: Optional[list] = None

    @classmethod
    def from_domain(cls, simu_domain: Simulacion) -> "SimulacionItem":
        return cls(
            id=getattr(simu_domain, "id", None),
            hora=getattr(simu_domain, "hora", None),
            evento=getattr(simu_domain, "evento", None),
            rnd_llegada=getattr(simu_domain, "rnd_llegada", None),
            tiempo_entre_llegadas=getattr(simu_domain, "tiempo_entre_llegadas", None),
            proxima_llegada=getattr(simu_domain, "proxima_llegada", None),
            estado_tecnico=getattr(simu_domain, "estado_tecnico", None),
            rnd_duracion_atencion=getattr(simu_domain, "rnd_duracion_atencion", None),
            duracion_atencion=getattr(simu_domain, "duracion_atencion", None),
            proximo_fin_atencion=getattr(simu_domain, "proximo_fin_atencion", None),
            rnd_presupuesto=getattr(simu_domain, "rnd_presupuesto", None),
            presupuesto=getattr(simu_domain, "presupuesto", None),
            rnd_deja_equipo=getattr(simu_domain, "rnd_deja_equipo", None),
            deja_equipo=getattr(simu_domain, "deja_equipo", None),
            rnd_duracion_reparacion=getattr(simu_domain, "rnd_duracion_reparacion", None),
            duracion_reparacion=getattr(simu_domain, "duracion_reparacion", None),
            fila_atencion_cantidad=getattr(simu_domain, "fila_atencion_cantidad", None),
            fila_equipos_cantidad=getattr(simu_domain, "fila_equipos_cantidad", None),
            tiempo_de_atencion_total=getattr(simu_domain, "tiempo_de_atencion_total", None),
            tiempo_de_reparacion_total=getattr(simu_domain, "tiempo_de_reparacion_total", None),
            clientes_no_atendidos=getattr(simu_domain, "clientes_no_atendidos", None),
            clientes=getattr(simu_domain, "clientes", None),
            equipos=getattr(simu_domain, "equipos", None),
        )
