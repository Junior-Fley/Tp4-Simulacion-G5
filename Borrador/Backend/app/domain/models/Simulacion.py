# python
from typing import Optional

class Simulacion:
    def __init__(
        self,
        simu_id: Optional[int] = None,
        hora: Optional[str] = None,
        evento: Optional[str] = None,
        rnd_llegada: Optional[float] = None,
        tiempo_entre_llegadas: Optional[str] = None,
        proxima_llegada: Optional[str] = None,
        estado_tecnico: Optional[str] = None,
        rnd_duracion_atencion: Optional[float] = None,
        duracion_atencion: Optional[str] = None,
        proximo_fin_atencion: Optional[str] = None,
        rnd_presupuesto: Optional[float] = None,
        presupuesto: Optional[str] = None,
        rnd_deja_equipo: Optional[float] = None,
        deja_equipo: Optional[bool] = None,
        rnd_duracion_reparacion: Optional[float] = None,
        duracion_reparacion: Optional[str] = None,
        fila_atencion_cantidad: Optional[int] = None,
        fila_equipos_cantidad: Optional[int] = None,
        tiempo_de_atencion_total: Optional[str] = None,
        tiempo_de_reparacion_total: Optional[str] = None,
        clientes_no_atendidos: Optional[int] = None,
    ) -> None:
        
        self.id = simu_id
        self.hora = hora
        self.evento = evento
        self.rnd_llegada = rnd_llegada
        self.tiempo_entre_llegadas = tiempo_entre_llegadas
        self.proxima_llegada = proxima_llegada
        self.estado_tecnico = estado_tecnico
        self.rnd_duracion_atencion = rnd_duracion_atencion
        self.duracion_atencion = duracion_atencion
        self.proximo_fin_atencion = proximo_fin_atencion
        self.rnd_presupuesto = rnd_presupuesto
        self.presupuesto = presupuesto
        self.rnd_deja_equipo = rnd_deja_equipo
        self.deja_equipo = deja_equipo
        self.rnd_duracion_reparacion = rnd_duracion_reparacion
        self.duracion_reparacion = duracion_reparacion
        self.fila_atencion_cantidad = fila_atencion_cantidad
        self.fila_equipos_cantidad = fila_equipos_cantidad
        self.tiempo_de_atencion_total = tiempo_de_atencion_total
        self.tiempo_de_reparacion_total = tiempo_de_reparacion_total
        self.clientes_no_atendidos = clientes_no_atendidos

    def __repr__(self) -> str:
        return f"Simulacion(id={self.id}, hora={self.hora}, evento={self.evento})"
