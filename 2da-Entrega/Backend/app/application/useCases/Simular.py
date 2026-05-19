import math
import random

from app.domain.models.Cliente import Cliente
from app.domain.models.ColaFIFO import ColaFIFO
from app.domain.models.Equipo import Equipo
from app.domain.models.EstadoCliente import EstadoCliente
from app.domain.models.EstadoEquipo import EstadoEquipo
from app.domain.models.Evento import Evento
from app.domain.models.Tecnico import Tecnico
from app.domain.models.EstadoTecnico import EstadoTecnico

class Simular:
    def __init__(self, x_tiempo: float, i_iteraciones: int, j_hora_inicio: float = 600): #600 == 10:00 AM
        self.n_cantidad_iteraciones: int = 0 ## máximo de 100_000 iteraciones
        self.x_tiempo: float = x_tiempo # representa el tiempo en float, debe convertirse a minutos para el reporte final
        self.i_iteraciones: int = i_iteraciones
        self.j_hora_inicio: float = j_hora_inicio
        self.hora_final : float = 1080

        self.media_llegada: float = 45 # representa el tiempo de media en minutos entre llegadas de clientes
        self.min_atencion: int = 10 # representa el tiempo mínimo en minutos para atender un cliente
        self.max_atencion: int = 20 # representa el tiempo máximo en minutos para atender un cliente
        self.media_reparacion: float = 90 # representa el tiempo de media en minutos para reparar un equipo



    def ejecutar_simulacion(self):
        presupuesto: str
        continua: bool
        rnd_reparacion: float
        rnd_llegada: float
        hora_proxima_llegada: float
        tiempo_hasta_proxima_llegada: float|None
        tiempo_hasta_fin_de_atencion: float|None
        tiempo_hasta_reparacion: float|None

        evento: Evento
        proximo_evento: Evento
        tecnico: Tecnico
        cola_equipos: ColaFIFO
        cola_clientes: ColaFIFO

        cola_equipos = ColaFIFO()
        cola_clientes = ColaFIFO()

        # generación de la fila 0 de la tabla de simulación
        hora_actual: float = self.j_hora_inicio

        evento = Evento.ABRE_TIENDA #TODO REVISAR LO DE ABRE TIENDA

        tecnico = Tecnico(estado= EstadoTecnico.LIBRE, equipo_asignado=None, acum_recepcion=0, acum_reparacion=0)

        rnd_llegada = random.random() # se genera un número uniforme entre 0 y 0.99

        tiempo_hasta_proxima_llegada = self.exponencial_negativa(self.media_llegada, rnd_llegada)

        hora_proxima_llegada = hora_actual + tiempo_hasta_proxima_llegada
        # fin generación de la fila 0 de la tabla de simulación

        cola_clientes.agregar(Cliente(EstadoCliente.EN_COLA, hora_proxima_llegada, None, None))

        #TODO guardar la informacion de la fila 1 de alguna forma para enviarla al front

        evento = Evento.LLEGA_CLIENTE


        for i in range(self.i_iteraciones):
            if hora_actual < self.hora_final:

                if cola_clientes.cantidad() > 0: # si hay clientes en la cola, entonces los atiendo
                    tecnico.estado = EstadoTecnico.ATENDIENDO_CLIENTE
                    if evento == Evento.LLEGA_CLIENTE:
                        hora_actual += tiempo_hasta_proxima_llegada #TODO REVISAR ESTO, PRIMERO DEBERÍA REVISAR SI EL PROXIMO EVENTO ES UNA LLEGADA DE CLIENTE U OTRA COSA, DE MOMENTO ASUMO QUE ES LA LLEGADA DE CLIENTE

                        # si ya llegó un cliente, debo calcular cuando llega el próximo
                        # se calcula la próxima llegada de un cliente
                        rnd_llegada = random.random()
                        tiempo_hasta_proxima_llegada = self.exponencial_negativa(self.media_llegada, rnd_llegada)
                        hora_proxima_llegada = hora_actual + tiempo_hasta_proxima_llegada


                        # se calcula el tiempo de atencion al cliente actual
                        #TODO REVISAR ACÁ, PRIMERO DEBERÍA VER SI NO SE ESTÁ ATENDIENDO A UN CLIENTE ACTUALEMENTE
                        tiempo_hasta_fin_de_atencion = self.uniforme(random.random(), self.min_atencion, self.max_atencion)




                        # asumo el fin de atencion antes de que llegue el proximo cliente
                        evento = evento.FIN_ATENCION_CL

                        # si el proximo cliente llega antes del fin de atención, entonces corrijo el evento a LLEGA_CLIENTE, sino, dejo como estaba
                        if tiempo_hasta_proxima_llegada:
                            if tiempo_hasta_fin_de_atencion > tiempo_hasta_proxima_llegada:
                                evento= evento.LLEGA_CLIENTE

                    elif evento == Evento.FIN_ATENCION_CL:
                        hora_actual += tiempo_hasta_fin_de_atencion

                        # se calcula si el cliente acepta la reparación o no
                        rnd_presupuesto = random.random()
                        presupuesto = "Normal"
                        tiempo_hasta_reparacion = None
                        acepto = True
                        if rnd_presupuesto < 0.3:
                            presupuesto = "Elevado"
                            rnd_acepta = random.random()
                            if rnd_acepta < 0.5:
                                acepto = False

                        if acepto: #TODO MOVER ESTO, SE CALCULA CUANTO SE TARDA EN LA REPARACION CUANDO EMPEZAMOS A REPARAR, NO ANTES
                            # si llego hasta acá es porque su presupuesto no era elevado, o era elevado, pero
                            # aceptó la reparación, entonces se asigna el cliente al técnico

                            rnd_reparacion = random.random()
                            tiempo_hasta_reparacion = self.exponencial_negativa(self.media_reparacion, rnd_reparacion)

                            nuevo_equipo = Equipo(EstadoEquipo.EN_COLA_REPARACION, hora_actual, None,
                                                  None, tiempo_hasta_reparacion, 0)

                            cola_equipos.agregar(nuevo_equipo)

                        cola_clientes.retirar()

                    elif evento == evento.FIN_REPARACION_CL:
                        pass


















    @staticmethod
    def exponencial_negativa(media:float, rnd: float) -> float:
        return -media * (math.log(1 - rnd))

    @staticmethod
    def uniforme(rnd: float, a: int, b: int) -> float:
        return a + (b - a) * rnd

    @staticmethod
    def minutos_a_hora(minutos: float) -> str:
        total_segundos = round(minutos * 60)

        horas = total_segundos // 3600
        minutos_restantes = (total_segundos % 3600) // 60
        segundos = total_segundos % 60

        return f"{horas:02d}:{minutos_restantes:02d}:{segundos:02d}"