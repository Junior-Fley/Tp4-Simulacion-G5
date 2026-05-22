from sqlalchemy.orm import Session
from app.application.ports.Simulacion_repository import ISimulacionRepository
from app.domain.models.ColaFIFO import ColaFIFO
from app.infrastructure.database.models.Simulacion_ORM import SimulacionORM

class SimulacionRepositoryImpl(ISimulacionRepository):
    def __init__(self, session: Session):
        self.session = session

    def guardar_fila(self, hora: str, evento: str, rnd_llegada: float, tiempo_hasta_llegada: str,
                     hora_proxima_llegada: str, estado_tecnico: str, rnd_atencion: float, proximo_fin_atencion: str,
                     rnd_presupuesto: float, presupuesto: str, acepta_reparar: bool | None,
                     deja_para_reparar: bool | None, rnd_reparacion: float, duracion_reparacion: str,
                     cola_atencion_cantidad: int, cola_equipos_cantidad: int, clientes_no_atendidos_por_cierre: int,
                     cola_clientes: ColaFIFO, cola_equipos: ColaFIFO) -> None:
        #TODO ACÁ HAY ALGO MAL CON LO DEL PROXIMO FIN DE ATENCIÓN, DE MOMENTO GUARDO 2 VECES EL MISMO DATO PARA VER SI ANDA LA BDD
        # también está mal el tema de los tiempos acumulados, pero eso lo voy a corregir después, por ahora quiero ver si se guardan los datos en la BDD

        simulacion = SimulacionORM(horario=hora, evento=evento, rnd_llegada=rnd_llegada,
                                   tiempo_entre_llegadas=tiempo_hasta_llegada,
                                   proxima_llegada=hora_proxima_llegada, estado_tecnico=estado_tecnico,
                                   rnd_atencion=rnd_atencion, tiempo_de_atencion=proximo_fin_atencion,
                                   proximo_fin_atencion=proximo_fin_atencion, rnd_presupuesto=rnd_presupuesto,
                                   presupuesto=presupuesto, rnd_deja_equipo=acepta_reparar,
                                   deja_equipo=deja_para_reparar, rnd_reparacion=rnd_reparacion,
                                   duracion_reparacion=duracion_reparacion, fila_clientes=cola_atencion_cantidad,
                                   fila_equipos=cola_equipos_cantidad,
                                   tiempo_de_atencion_total='CALCULAR TIEMPOS ACUMULADOS',
                                   tiempo_de_reparacion_total='CALCULAR TIEMPOS ACUMULADOS',
                                   clientes_no_atendidos=clientes_no_atendidos_por_cierre)

        self.session.add(simulacion)
        self.session.flush()



    #region Métodos específicos para cada tipo de evento (para no repetir argumentos innecesarios)
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

    #endregion