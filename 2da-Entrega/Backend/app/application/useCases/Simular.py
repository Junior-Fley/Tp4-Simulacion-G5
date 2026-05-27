import math
import random
from typing import List, Tuple, Any
from app.domain.models.Colas.ColaFIFO import ColaFIFO
from app.domain.models.event.Evento import Evento
from app.domain.models.Tecnico import Tecnico
from app.domain.models.EstadoTecnico import EstadoTecnico
from app.domain.models.event.LlegaCliente import LlegaCliente
from app.application.ports.Simulacion_repository import ISimulacionRepository
from app.infrastructure.database.unit_of_work.unit_of_work_impl import UowFactory
from app.domain.models.Colas.ColaClientes import ColaClientes
from app.domain.models.Colas.ColaEquipos import ColaEquipos
from app.domain.services.truncar_service import truncar_a_decimales

class Simular:
    def __init__(self, uow_factory: UowFactory, x_tiempo: float, i_iteraciones: int, j_hora_inicio: float = 600,
                 media_llegada: float = 45, min_atencion: float = 10, max_atencion: float = 20, media_reparacion: float = 90,
                 repo_override: ISimulacionRepository|None = None, batch_size: int = 10_000): #600 == 10:00 AM


        self.id_coleccion: int = -1
        self.repo_override: ISimulacionRepository = repo_override
        self.uow_factory: UowFactory = uow_factory

        # vector para guardar filas en memoria antes de mandar a guardar a la bdd
        self.filas_a_guardar: List[Tuple[int,str,str,float,str,str,str,float,str,
        str,float,str,float,bool|None,float,str,int,int,str,str,int,Any,Any]] = []
        self.batch_size: int = batch_size

        self.n_cantidad_iteraciones: int = 0 ## máximo de 100_000 iteraciones
        self.x_tiempo: float = x_tiempo # representa el tiempo en float, debe convertirse a minutos para el reporte final
        self.i_iteraciones: int = i_iteraciones
        self.j_hora_inicio: float = j_hora_inicio

        self.media_llegada: float = media_llegada # representa el tiempo de media en minutos entre llegadas de clientes
        self.min_atencion: float = min_atencion # representa el tiempo mínimo en minutos para atender un cliente
        self.max_atencion: float = max_atencion # representa el tiempo máximo en minutos para atender un cliente
        self.media_reparacion: float = media_reparacion # representa el tiempo de media en minutos para reparar un equipo

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
        self.cola_equipos: ColaFIFO = ColaEquipos()
        self.cola_clientes: ColaFIFO = ColaClientes()

        self.hora_apertura = self.j_hora_inicio
        self.hora_cierre = 1080
        self.local_abierto = True

        self.contador_clientes: int = 0
        self.contador_equipos: int = 0
        self.acum_tiempo_equipos: float = 0

    def abrir_tienda(self):
        self.local_abierto = True
        self.hora_actual = self.hora_apertura
        self.tecnico.estado = EstadoTecnico.LIBRE
        self.rnd_llegada = random.random()
        self.tiempo_hasta_proxima_llegada = self.exponencial_negativa(self.media_llegada, self.rnd_llegada)
        self.hora_proxima_llegada = self.hora_actual + self.tiempo_hasta_proxima_llegada

    def cerrar_tienda(self):
        self.local_abierto = False


    @staticmethod
    def exponencial_negativa(media: float, rnd: float) -> float:
        return -media * (math.log(1 - rnd))

    @staticmethod
    def uniforme(rnd: float, a: float, b: float) -> float:
        return a + (b - a) * rnd

    @staticmethod
    def float_a_hora(minutos: float) -> str:
        total_segundos = round(minutos * 60) % 86400  # 86400 = 24 * 3600, hace que el reloj "dé la vuelta"

        horas = total_segundos // 3600
        minutos_restantes = (total_segundos % 3600) // 60
        segundos = total_segundos % 60

        return f"{horas:02d}:{minutos_restantes:02d}:{segundos:02d}"

    def guardar_fila_reparacion(self,):
        if self.cola_equipos.cantidad() == 0:
            self.filas_a_guardar.append((self.id_coleccion, self.float_a_hora(self.hora_actual), self.evento.nombre, -1,
                               '', self.float_a_hora(self.hora_proxima_llegada),
                               self.tecnico.estado, -1, '','', -1,
                               '', -1, None, -1, '',
                               self.cola_clientes.cantidad(), self.cola_equipos.cantidad(),
                               self.float_a_hora(self.tecnico.acum_atencion), self.float_a_hora(self.tecnico.acum_reparacion),
                               self.clientes_no_atendidos, self.cola_clientes.serialize(), self.cola_equipos.serialize()))


        elif self.cola_equipos.cantidad() > 0:
            self.filas_a_guardar.append((self.id_coleccion, self.float_a_hora(self.hora_actual), self.evento.nombre, -1,
                               '', self.float_a_hora(self.hora_proxima_llegada),
                               self.tecnico.estado, -1, '','', -1,
                               '', -1, None, truncar_a_decimales(self.rnd_reparacion), self.float_a_hora(self.tiempo_hasta_reparacion),
                               self.cola_clientes.cantidad(), self.cola_equipos.cantidad(),
                               self.float_a_hora(self.tecnico.acum_atencion), self.float_a_hora(self.tecnico.acum_reparacion),
                               self.clientes_no_atendidos,
                               self.cola_clientes.serialize(), self.cola_equipos.serialize()))

    def guardar_fila_atencion(self):
        if self.cola_clientes.cantidad() == 0 and self.cola_equipos.cantidad() == 0:
            # si el cliente que atendí era el último en la cola, entonces no hay un próximo cliente para atender, por lo tanto no se le calcula el tiempo de atención al próximo cliente, y se guarda la fila en la BDD, sin tiempo de atención
            self.filas_a_guardar.append((self.id_coleccion, self.float_a_hora(self.hora_actual), self.evento.nombre, -1,
                               '', self.float_a_hora(self.hora_proxima_llegada),
                               self.tecnico.estado, -1, '', '', truncar_a_decimales(self.rnd_presupuesto,3),
                               self.presupuesto, truncar_a_decimales(self.rnd_acepta,3), self.acepto, -1, '',
                               self.cola_clientes.cantidad(), self.cola_equipos.cantidad(),
                               self.float_a_hora(self.tecnico.acum_atencion),
                               self.float_a_hora(self.tecnico.acum_reparacion),
                               self.clientes_no_atendidos,
                               self.cola_clientes.serialize(), self.cola_equipos.serialize()))
        elif self.cola_clientes.cantidad() > 0:
            # si el cliente que atendí no era el último en la cola, entonces hay un próximo cliente para atender, por lo tanto se le calcula el tiempo de atención al próximo cliente, y se guarda la fila en la BDD, con tiempo de atención
            self.filas_a_guardar.append((self.id_coleccion, self.float_a_hora(self.hora_actual), self.evento.nombre, -1,
                               '', self.float_a_hora(self.hora_proxima_llegada),
                               self.tecnico.estado, truncar_a_decimales(self.rnd_atencion,3), self.float_a_hora(self.tiempo_hasta_fin_de_atencion),
                               self.float_a_hora(self.hora_proximo_fin_atencion), truncar_a_decimales(self.rnd_presupuesto,3),
                               self.presupuesto, truncar_a_decimales(self.rnd_acepta,3), self.acepto, -1, '',
                               self.cola_clientes.cantidad(), self.cola_equipos.cantidad(),
                               self.float_a_hora(self.tecnico.acum_atencion),
                               self.float_a_hora(self.tecnico.acum_reparacion),
                               self.clientes_no_atendidos,
                               self.cola_clientes.serialize(), self.cola_equipos.serialize()))

        elif self.cola_clientes.cantidad() == 0 and self.cola_equipos.cantidad() > 0:
            # si el cliente que atendí era el último en la cola, pero hay equipos en la cola de reparación, entonces no hay un próximo cliente para atender, por lo tanto no se le calcula el tiempo de atención al próximo cliente, y se guarda la fila en la BDD, sin tiempo de atención
            # pero el próximo evento es la reparación de un equipo, entonces se le calcula el tiempo de reparación al próximo equipo, y se guarda la fila en la BDD, con tiempo de reparación
            self.filas_a_guardar.append((self.id_coleccion, self.float_a_hora(self.hora_actual), self.evento.nombre, -1, '',
                               self.float_a_hora(self.hora_proxima_llegada),
                               self.tecnico.estado, -1, '', '', truncar_a_decimales(self.rnd_presupuesto,3), self.presupuesto,
                               truncar_a_decimales(self.rnd_acepta,3),
                               self.acepto,
                               truncar_a_decimales(self.rnd_reparacion,3), self.float_a_hora(self.tiempo_hasta_reparacion),
                               self.cola_clientes.cantidad(), self.cola_equipos.cantidad(),
                               self.float_a_hora(self.tecnico.acum_atencion),
                               self.float_a_hora(self.tecnico.acum_reparacion),
                               self.clientes_no_atendidos,
                               self.cola_clientes.serialize(), self.cola_equipos.serialize()))

    def guardar_fila_llega_cliente(self):

        if self.hora_actual > self.hora_cierre and self.cola_equipos.cantidad() > 0:
            self.filas_a_guardar.append((self.id_coleccion, self.float_a_hora(self.hora_actual), self.evento.nombre,
                                         truncar_a_decimales(self.rnd_llegada,3), self.float_a_hora(self.tiempo_hasta_proxima_llegada),
                                         self.float_a_hora(self.hora_proxima_llegada), self.tecnico.estado,
                                         -1, '', '', -1, '', -1,
                                         None, truncar_a_decimales(self.rnd_reparacion,3), self.float_a_hora(self.tiempo_hasta_reparacion),
                                         self.cola_clientes.cantidad(), self.cola_equipos.cantidad(),
                                         self.float_a_hora(self.tecnico.acum_atencion),
                                         self.float_a_hora(self.tecnico.acum_reparacion),
                                         self.clientes_no_atendidos,
                                         self.cola_clientes.serialize(), self.cola_equipos.serialize()))
            return

        elif self.hora_actual > self.hora_cierre and self.cola_equipos.cantidad() == 0:
            self.filas_a_guardar.append((self.id_coleccion, self.float_a_hora(self.hora_actual), self.evento.nombre,
                                         truncar_a_decimales(self.rnd_llegada,3), self.float_a_hora(self.tiempo_hasta_proxima_llegada),
                                         self.float_a_hora(self.hora_proxima_llegada), self.tecnico.estado,
                                         -1, '', '', -1, '', -1,
                                         None, truncar_a_decimales(self.rnd_reparacion,3), '',
                                         self.cola_clientes.cantidad(), self.cola_equipos.cantidad(),
                                         self.float_a_hora(self.tecnico.acum_atencion),
                                         self.float_a_hora(self.tecnico.acum_reparacion),
                                         self.clientes_no_atendidos,
                                         self.cola_clientes.serialize(), self.cola_equipos.serialize()))
            return


        if self.cola_clientes.cantidad() == 1:
            # si el cliente que acaba de llegar es el único en la cola, entonces se atiende inmediatamente, se le calcula el tiempo de atención, y se guarda la fila en la BDD, con tiempo de atención
            self.filas_a_guardar.append((self.id_coleccion, self.float_a_hora(self.hora_actual), self.evento.nombre,
                                         truncar_a_decimales(self.rnd_llegada,3), self.float_a_hora(self.tiempo_hasta_proxima_llegada),
                                         self.float_a_hora(self.hora_proxima_llegada), self.tecnico.estado,
                                         truncar_a_decimales(self.rnd_atencion,3), self.float_a_hora(self.tiempo_hasta_fin_de_atencion),
                                         self.float_a_hora(self.hora_proximo_fin_atencion), -1,'', -1, None, -1, '',
                                         self.cola_clientes.cantidad(), self.cola_equipos.cantidad(),
                                         self.float_a_hora(self.tecnico.acum_atencion),
                                         self.float_a_hora(self.tecnico.acum_reparacion),
                                         self.clientes_no_atendidos,
                                         self.cola_clientes.serialize(), self.cola_equipos.serialize()))
        else:
            # si el cliente no es el primero en la cola, entonces no se atiende inmediatamente, no se le calcula el tiempo de atención, y se guarda la fila en la BDD, sin tiempo de atención
            self.filas_a_guardar.append((self.id_coleccion, self.float_a_hora(self.hora_actual), self.evento.nombre,
                                         truncar_a_decimales(self.rnd_llegada,3), self.float_a_hora(self.tiempo_hasta_proxima_llegada),
                                         self.float_a_hora(self.hora_proxima_llegada), self.tecnico.estado,
                                         -1, '', self.float_a_hora(self.hora_proximo_fin_atencion), -1, '', -1,
                                         None, -1, '', self.cola_clientes.cantidad(),
                                         self.cola_equipos.cantidad(),
                                         self.float_a_hora(self.tecnico.acum_atencion),
                                         self.float_a_hora(self.tecnico.acum_reparacion),
                                         self.clientes_no_atendidos,
                                         self.cola_clientes.serialize(), self.cola_equipos.serialize()))

    def guarda_fila_abre_tienda(self):
        self.filas_a_guardar.append((
                self.id_coleccion, self.float_a_hora(self.hora_actual),
                self.evento.nombre,
                truncar_a_decimales(self.rnd_llegada, 3),
                self.float_a_hora(self.tiempo_hasta_proxima_llegada),
                self.float_a_hora(self.hora_proxima_llegada),
                self.tecnico.estado,
                -1,
                '', '',
                -1,
                '', -1, None,
                -1,
                '', 0, 0,
                '', '', 0,
                self.cola_clientes.serialize(),
                self.cola_equipos.serialize()
            ))

    def ejecutar_simulacion(self) -> int:
        # creamos la nueva colección de simulaciones en la bdd
        with self.uow_factory() as uow:
            self.id_coleccion = uow.colec_repo.guardar_coleccion()

        # al iniciar una nueva simulación inicializo las colas, para asegurarme que están vacías
        self.cola_equipos = ColaEquipos()
        self.cola_clientes = ColaClientes()

        #region FILA 0

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
                truncar_a_decimales(self.rnd_llegada, 3),
                self.float_a_hora(self.tiempo_hasta_proxima_llegada),
                self.float_a_hora(self.hora_proxima_llegada),
                self.tecnico.estado,
                -1,
                '', '',
                -1,
                '', -1, None,
                -1,
                '', 0, 0,
                '', '', 0,
                self.cola_clientes.serialize(),
                self.cola_equipos.serialize()
            )

        # endregion FILA 0

        self.evento = LlegaCliente()

        for i in range(self.i_iteraciones):

            #Hay que cortar el bucle si se llegó a la hora de cierre x_tiempo
            if self.hora_actual < self.x_tiempo:
                # region guardado en bulk de filas
                # si mi cantidad de filas en mi vector de filas a guardar es mayor o igual al tamaño definido para commit
                # a la bdd, entonces guardo las filas y limpio el vector de filas a guardar.
                if len(self.filas_a_guardar) >= self.batch_size:
                    with self.uow_factory() as uow:
                        if self.repo_override is not None:
                            uow.simu_repo = self.repo_override
                        uow.simu_repo.guardar_filas_bulk(self.filas_a_guardar)

                    self.filas_a_guardar = []


                #endregion guardado en bulk de filas

                # ejecutar la accion correspondiente al evento actual, esto debería ser autosuficiente y encargarse
                # de gestionar las transiciones a otros eventos mientras la tienda este abierta y también cuando cierre o
                # vaya a reabrir
                self.evento.ejecutar_accion(self)

                # definir que datos corresponden guardar en esta fila y guardarlos en el vector de filas
                # para después guardar en BDD
                match self.evento.nombre:
                    case "Llega_Cliente":
                        self.guardar_fila_llega_cliente()
                    case "Fin_Atención":
                        self.guardar_fila_atencion()
                    case "Fin_Reparación":
                        self.guardar_fila_reparacion()
                    case "Abre_Tienda":
                        self.guarda_fila_abre_tienda()

                self.evento = self.proximo_evento



        # si ya terminó la ejecución de la simulación, pero aún tengo filas en mi vector de filas a guardar, entonces guardo las filas restantes en la bdd

        with self.uow_factory() as uow:
            if self.repo_override is not None:
                uow.simu_repo = self.repo_override
            uow.simu_repo.guardar_filas_bulk(self.filas_a_guardar)
            uow.acum_repo.guardar_acumulador(self.id_coleccion, self.acum_tiempo_equipos, self.contador_equipos)
            self.filas_a_guardar = []

        return self.id_coleccion


