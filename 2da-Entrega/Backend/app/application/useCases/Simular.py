import math
import random



from app.domain.models.ColaFIFO import ColaFIFO
from app.domain.models.event.Evento import Evento
from app.domain.models.Tecnico import Tecnico
from app.domain.models.EstadoTecnico import EstadoTecnico
from app.domain.models.event.LlegaCliente import LlegaCliente
from app.application.ports.Simulacion_repository import ISimulacionRepository
from app.infrastructure.database.unit_of_work.unit_of_work_impl import UowFactory
from app.infrastructure.database.unit_of_work.unit_of_work import IUnitOfWork

from app.domain.models.event.AbreTienda import AbreTienda
from app.domain.models.event.FinReparacion import FinReparacion


class Simular:
    def __init__(self, uow_factory: UowFactory, x_tiempo: float, i_iteraciones: int, j_hora_inicio: float = 600, repo_override: ISimulacionRepository|None = None): #600 == 10:00 AM

        self.id_coleccion: int = -1
        self.repo_override: ISimulacionRepository = repo_override
        self.uow_factory: UowFactory = uow_factory

        self.n_cantidad_iteraciones: int = 0 ## máximo de 100_000 iteraciones
        self.x_tiempo: float = x_tiempo # representa el tiempo en float, debe convertirse a minutos para el reporte final
        self.i_iteraciones: int = i_iteraciones
        self.j_hora_inicio: float = j_hora_inicio

        self.media_llegada: float = 45 # representa el tiempo de media en minutos entre llegadas de clientes
        self.min_atencion: int = 10 # representa el tiempo mínimo en minutos para atender un cliente
        self.max_atencion: int = 20 # representa el tiempo máximo en minutos para atender un cliente
        self.media_reparacion: float = 90 # representa el tiempo de media en minutos para reparar un equipo

        self.clientes_no_atendidos: int = 0
        self.presupuesto: str = ''
        self.rnd_reparacion: float = 0
        self.rnd_presupuesto: float = 0
        self.rnd_llegada: float = 0
        self.rnd_atencion: float = 0
        self.rnd_acepta: float = 0
        self.hora_proxima_llegada: float = 0
        self.hora_proximo_fin_atencion: float= 0
        self.hora_actual: float = 0
        self.tiempo_hasta_proxima_llegada: float= 0
        self.tiempo_hasta_fin_de_atencion: float= 0
        self.tiempo_hasta_reparacion: float= 0
        self.acepto: bool | None = None

        self.evento: Evento | None = None
        self.proximo_evento: Evento|None = None
        self.tecnico: Tecnico| None = None
        self.cierre: bool = False
        self.cola_equipos: ColaFIFO = ColaFIFO()
        self.cola_clientes: ColaFIFO = ColaFIFO()

        self.hora_apertura = 600
        self.hora_cierre = 1080
        self.local_abierto = True

    def abrir_tienda(self):
        self.local_abierto = True
        self.hora_actual = self.hora_apertura
        self.tecnico.estado = EstadoTecnico.LIBRE
        self.rnd_llegada = random.random()
        self.tiempo_hasta_proxima_llegada = self.exponencial_negativa(self.media_llegada, self.rnd_llegada)
        self.hora_proxima_llegada = self.hora_actual + self.tiempo_hasta_proxima_llegada

    def cerrar_tienda(self):
        self.local_abierto = False

    def programar_reapertura(self):
        self.evento = AbreTienda()
        self.proximo_evento = AbreTienda()

    @staticmethod
    def exponencial_negativa(media: float, rnd: float) -> float:
        return -media * (math.log(1 - rnd))

    @staticmethod
    def uniforme(rnd: float, a: int, b: int) -> float:
        return a + (b - a) * rnd

    @staticmethod
    def float_a_hora(minutos: float) -> str:
        total_segundos = round(minutos * 60) % 86400  # 86400 = 24 * 3600, hace que el reloj "dé la vuelta"

        horas = total_segundos // 3600
        minutos_restantes = (total_segundos % 3600) // 60
        segundos = total_segundos % 60

        return f"{horas:02d}:{minutos_restantes:02d}:{segundos:02d}"


    def guardar_fila_reparacion(self, uow: IUnitOfWork):
        if self.cola_equipos.cantidad() == 0:
            uow.simu_repo.guardar_fin_reparacion_no_hay_equipos(self.id_coleccion, self.float_a_hora(self.hora_actual),
                                                                self.evento.nombre,
                                                                self.float_a_hora(self.hora_proxima_llegada),
                                                                self.tecnico.estado.value,
                                                                self.cola_clientes.cantidad(),
                                                                self.cola_equipos.cantidad(),
                                                                self.float_a_hora(self.tecnico.acum_atencion),
                                                                self.float_a_hora(self.tecnico.acum_reparacion),
                                                                self.clientes_no_atendidos,
                                                                self.cola_clientes,
                                                                self.cola_equipos)
        elif self.cola_equipos.cantidad() > 0:
            uow.simu_repo.guardar_fin_reparacion_hay_equipos(self.id_coleccion, self.float_a_hora(self.hora_actual),
                                                             self.evento.nombre,
                                                             self.float_a_hora(self.hora_proxima_llegada),
                                                             self.tecnico.estado.value,
                                                             round(self.rnd_reparacion,3),
                                                             self.float_a_hora(self.tiempo_hasta_reparacion),
                                                             self.cola_clientes.cantidad(),
                                                             self.cola_equipos.cantidad(),
                                                             self.float_a_hora(self.tecnico.acum_atencion),
                                                             self.float_a_hora(self.tecnico.acum_reparacion),
                                                             self.clientes_no_atendidos,
                                                             self.cola_clientes,
                                                             self.cola_equipos)

    def guardar_fila_atencion(self, uow: IUnitOfWork):
        if self.cola_clientes.cantidad() == 0 and self.cola_equipos.cantidad() == 0:
            # si el cliente que atendí era el último en la cola, entonces no hay un próximo cliente para atender, por lo tanto no se le calcula el tiempo de atención al próximo cliente, y se guarda la fila en la BDD, sin tiempo de atención
            uow.simu_repo.guardar_fin_atencion_no_hay_clientes(self.id_coleccion, self.float_a_hora(self.hora_actual),
                                                               self.evento.nombre,
                                                               self.float_a_hora(self.hora_proxima_llegada),
                                                               self.tecnico.estado.value,
                                                               round(self.rnd_atencion,3),
                                                               self.presupuesto,
                                                               round(self.rnd_acepta,3),
                                                               self.acepto,
                                                               self.cola_clientes.cantidad(),
                                                               self.cola_equipos.cantidad(),
                                                               self.float_a_hora(self.tecnico.acum_atencion),
                                                               self.float_a_hora(self.tecnico.acum_reparacion),
                                                               self.clientes_no_atendidos,
                                                               self.cola_clientes,
                                                               self.cola_equipos)
        elif self.cola_clientes.cantidad() > 0:
            # si el cliente que atendí no era el último en la cola, entonces hay un próximo cliente para atender, por lo tanto se le calcula el tiempo de atención al próximo cliente, y se guarda la fila en la BDD, con tiempo de atención
            uow.simu_repo.guardar_fin_atencion_hay_clientes(self.id_coleccion, self.float_a_hora(self.hora_actual),
                                                            self.evento.nombre,
                                                            self.float_a_hora(self.hora_proxima_llegada),
                                                            self.tecnico.estado.value,
                                                            round(self.rnd_atencion,3),
                                                            self.float_a_hora(self.tiempo_hasta_fin_de_atencion),
                                                            self.float_a_hora(self.hora_proximo_fin_atencion),
                                                            round(self.rnd_atencion,3),
                                                            self.presupuesto,
                                                            round(self.rnd_acepta,3),
                                                            self.acepto,
                                                            self.cola_clientes.cantidad(),
                                                            self.cola_equipos.cantidad(),
                                                            self.float_a_hora(self.tecnico.acum_atencion),
                                                            self.float_a_hora(self.tecnico.acum_reparacion),
                                                            self.clientes_no_atendidos, self.cola_clientes,
                                                            self.cola_equipos)


        elif self.cola_clientes.cantidad() == 0 and self.cola_equipos.cantidad() > 0:
            # si el cliente que atendí era el último en la cola, pero hay equipos en la cola de reparación, entonces no hay un próximo cliente para atender, por lo tanto no se le calcula el tiempo de atención al próximo cliente, y se guarda la fila en la BDD, sin tiempo de atención
            # pero el próximo evento es la reparación de un equipo, entonces se le calcula el tiempo de reparación al próximo equipo, y se guarda la fila en la BDD, con tiempo de reparación
            uow.simu_repo.guardar_fin_atencion_hay_equipos(self.id_coleccion, self.float_a_hora(self.hora_actual),
                                                           self.evento.nombre,
                                                           self.float_a_hora(self.hora_proxima_llegada),
                                                           self.tecnico.estado.value,
                                                           round(self.rnd_presupuesto,3),
                                                           self.presupuesto,
                                                           round(self.rnd_acepta,3),
                                                           self.acepto,
                                                           round(self.rnd_reparacion,3),
                                                           self.float_a_hora(self.tiempo_hasta_reparacion) if self.tiempo_hasta_reparacion else None,
                                                           self.cola_clientes.cantidad(),
                                                           self.cola_equipos.cantidad(),
                                                           self.float_a_hora(self.tecnico.acum_atencion),
                                                           self.float_a_hora(self.tecnico.acum_reparacion),
                                                           self.clientes_no_atendidos, self.cola_clientes,
                                                           self.cola_equipos)

    def guardar_fila_llega_cliente(self, uow: IUnitOfWork):

        if self.hora_actual > self.hora_cierre and self.cola_equipos.cantidad() > 0:
            uow.simu_repo.guardar_llega_cliente_repara(self.id_coleccion, self.float_a_hora(self.hora_actual),
                                                       self.evento.nombre,
                                                       round(self.rnd_llegada,3),
                                                       self.float_a_hora(self.tiempo_hasta_proxima_llegada),
                                                       self.float_a_hora(self.hora_proxima_llegada),
                                                       self.tecnico.estado.value,
                                                       round(self.rnd_reparacion,3),
                                                       self.float_a_hora(self.cola_equipos.primero().tiempo_reparacion_restante),
                                                       self.cola_clientes.cantidad(),
                                                       self.cola_equipos.cantidad(),
                                                       self.float_a_hora(self.tecnico.acum_atencion),
                                                       self.float_a_hora(self.tecnico.acum_reparacion),
                                                       self.clientes_no_atendidos,
                                                       self.cola_clientes,
                                                       self.cola_equipos)
            return
        elif self.hora_actual > self.hora_cierre and self.cola_equipos.cantidad() == 0:
            uow.simu_repo.guardar_llega_cliente_repara(self.id_coleccion, self.float_a_hora(self.hora_actual),
                                                       self.evento.nombre,
                                                       round(self.rnd_llegada, 3),
                                                       self.float_a_hora(self.tiempo_hasta_proxima_llegada),
                                                       self.float_a_hora(self.hora_proxima_llegada),
                                                       self.tecnico.estado.value,
                                                       round(self.rnd_reparacion, 3),
                                                       '',
                                                       self.cola_clientes.cantidad(),
                                                       self.cola_equipos.cantidad(),
                                                       self.float_a_hora(self.tecnico.acum_atencion),
                                                       self.float_a_hora(self.tecnico.acum_reparacion),
                                                       self.clientes_no_atendidos,
                                                       self.cola_clientes,
                                                       self.cola_equipos)
            return


        if self.cola_clientes.cantidad() == 1:
            # si el cliente que acaba de llegar es el único en la cola, entonces se atiende inmediatamente, se le calcula el tiempo de atención, y se guarda la fila en la BDD, con tiempo de atención
            uow.simu_repo.guardar_llega_cliente_atiende(self.id_coleccion, self.float_a_hora(self.hora_actual),
                                                        self.evento.nombre,
                                                        round(self.rnd_llegada,3),
                                                        self.float_a_hora(self.tiempo_hasta_proxima_llegada),
                                                        self.float_a_hora(self.hora_proxima_llegada),
                                                        self.tecnico.estado.value,
                                                        round(self.rnd_atencion,3),
                                                        self.float_a_hora(self.tiempo_hasta_fin_de_atencion),
                                                        self.float_a_hora(self.hora_proximo_fin_atencion),
                                                        self.cola_clientes.cantidad(),
                                                        self.cola_equipos.cantidad(),
                                                        self.float_a_hora(self.tecnico.acum_atencion),
                                                        self.float_a_hora(self.tecnico.acum_reparacion),
                                                        self.clientes_no_atendidos,
                                                        self.cola_clientes,
                                                        self.cola_equipos)
        else:
            # si el cliente no es el primero en la cola, entonces no se atiende inmediatamente, no se le calcula el tiempo de atención, y se guarda la fila en la BDD, sin tiempo de atención
            uow.simu_repo.guardar_llega_cliente_no_atiende(self.id_coleccion, self.float_a_hora(self.hora_actual),
                                                           self.evento.nombre,
                                                           round(self.rnd_llegada,3),
                                                           self.float_a_hora(self.tiempo_hasta_proxima_llegada),
                                                           self.float_a_hora(self.hora_proxima_llegada),
                                                           self.tecnico.estado.value,
                                                           self.float_a_hora(self.hora_proximo_fin_atencion),
                                                           self.cola_clientes.cantidad(),
                                                           self.cola_equipos.cantidad(),
                                                           self.float_a_hora(self.tecnico.acum_atencion),
                                                           self.float_a_hora(self.tecnico.acum_reparacion),
                                                           self.clientes_no_atendidos,
                                                           self.cola_clientes,
                                                           self.cola_equipos)

    def ejecutar_simulacion(self) -> int:
        # creamos la nueva colección de simulaciones en la bdd
        with self.uow_factory() as uow:
            self.id_coleccion = uow.colec_repo.guardar_coleccion()

        # al iniciar una nueva simulación inicializo las colas, para asegurarme que están vacías
        self.cola_equipos = ColaFIFO()
        self.cola_clientes = ColaFIFO()

        # generación de la fila 0 de la tabla de simulación
        self.hora_actual = self.j_hora_inicio
        self.local_abierto = True

        self.tecnico = Tecnico(estado=EstadoTecnico.LIBRE, equipo_asignado=None, acum_atencion=0, acum_reparacion=0)

        self.rnd_llegada = random.random()
        self.tiempo_hasta_proxima_llegada = self.exponencial_negativa(self.media_llegada, self.rnd_llegada)
        self.hora_proxima_llegada = self.hora_actual + self.tiempo_hasta_proxima_llegada

        # Guardar fila 0 en la BDD
        with self.uow_factory() as uow:
            if self.repo_override is not None:
                uow.simu_repo = self.repo_override

            uow.simu_repo.guardar_fila(
                self.id_coleccion, self.float_a_hora(self.hora_actual),
                'Abre Tienda',
                round(self.rnd_llegada, 3),
                self.float_a_hora(self.tiempo_hasta_proxima_llegada),
                self.float_a_hora(self.hora_proxima_llegada),
                self.tecnico.estado.value,
                -1,
                '', '',
                -1,
                '', -1, None,
                -1,
                '', 0, 0,
                '', '', 0,
                self.cola_clientes,
                self.cola_equipos
            )

        self.evento = LlegaCliente()

        for i in range(self.i_iteraciones):
            if self.local_abierto:
                self.evento.ejecutar_accion(self)

                with self.uow_factory() as uow:
                    if self.repo_override is not None:
                        uow.simu_repo = self.repo_override

                    match self.evento.nombre:
                        case "Llega_Cliente":
                            self.guardar_fila_llega_cliente(uow)
                        case "Fin_Atención":
                            self.guardar_fila_atencion(uow)
                        case "Fin_Reparación":
                            self.guardar_fila_reparacion(uow)
                        case "Abre_Tienda":
                            pass

                self.evento = self.proximo_evento

                if self.hora_actual >= self.hora_cierre:
                    self.local_abierto = False
                    self.evento = FinReparacion() if self.cola_equipos.cantidad() > 0 else AbreTienda()
                    self.proximo_evento = self.evento

            else:
                if self.cola_equipos.cantidad() > 0:
                    self.evento.ejecutar_accion(self)

                    with self.uow_factory() as uow:
                        if self.repo_override is not None:
                            uow.simu_repo = self.repo_override

                        self.guardar_fila_reparacion(uow)

                    self.evento = self.proximo_evento
                else:
                    self.evento = AbreTienda()
                    self.evento.ejecutar_accion(self)
                    self.proximo_evento = LlegaCliente()

                    with self.uow_factory() as uow:
                        if self.repo_override is not None:
                            uow.simu_repo = self.repo_override

                        uow.simu_repo.guardar_fila(
                            self.id_coleccion,
                            self.float_a_hora(self.hora_actual),
                            self.evento.nombre,
                            round(self.rnd_llegada, 3),
                            self.float_a_hora(self.tiempo_hasta_proxima_llegada),
                            self.float_a_hora(self.hora_proxima_llegada),
                            self.tecnico.estado.value,
                            -1,
                            '',
                            '',
                            -1,
                            '',
                            -1,
                            None,
                            -1,
                            '',
                            0,
                            0,
                            '',
                            '',
                            0,
                            self.cola_clientes,
                            self.cola_equipos
                        )

                    self.evento = self.proximo_evento

        return self.id_coleccion


