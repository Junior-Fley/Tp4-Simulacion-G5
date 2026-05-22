import math
import random

from app.domain.models.Cliente import Cliente
from app.domain.models.ColaFIFO import ColaFIFO
from app.domain.models.EstadoCliente import EstadoCliente
from app.domain.models.event.AbreTienda import AbreTienda
from app.domain.models.event.Evento import Evento
from app.domain.models.Tecnico import Tecnico
from app.domain.models.EstadoTecnico import EstadoTecnico
from app.domain.models.event.LlegaCliente import LlegaCliente


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


        self.presupuesto: str = ''
        self.rnd_reparacion: float = 0
        self.rnd_presupuesto: float = 0
        self.rnd_llegada: float = 0
        self.rnd_atencion: float = 0
        self.rnd_acepta: float = 0
        self.hora_proxima_llegada: float = 0
        self.hora_actual: float = 0
        self.tiempo_hasta_proxima_llegada: float= 0
        self.tiempo_hasta_fin_de_atencion: float= 0
        self.tiempo_hasta_reparacion: float= 0
        self.acepto: bool | None = None

        self.evento: Evento | None = None
        self.proximo_evento: Evento|None = None
        self.tecnico: Tecnico| None = None
        self.cola_equipos: ColaFIFO = ColaFIFO()
        self.cola_clientes: ColaFIFO = ColaFIFO()

    @staticmethod
    def exponencial_negativa(media: float, rnd: float) -> float:
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

    def ejecutar_simulacion(self):

        self.cola_equipos = ColaFIFO()
        self.cola_clientes = ColaFIFO()

        # generación de la fila 0 de la tabla de simulación
        self.hora_actual = self.j_hora_inicio

        self.tecnico = Tecnico(estado= EstadoTecnico.LIBRE, equipo_asignado=None, acum_recepcion=0, acum_reparacion=0)

        self.rnd_llegada = random.random() # se genera un número uniforme entre 0 y 0.99

        self.tiempo_hasta_proxima_llegada = self.exponencial_negativa(self.media_llegada, self.rnd_llegada)

        self.hora_proxima_llegada = self.hora_actual + self.tiempo_hasta_proxima_llegada
        # fin generación de la fila 0 de la tabla de simulación

        self.cola_clientes.agregar(Cliente(EstadoCliente.EN_COLA, self.hora_proxima_llegada, None, None))

        #TODO guardar la información de la fila 1 en la BDD

        self.evento = LlegaCliente()


        for i in range(self.i_iteraciones):
            if self.hora_actual < self.hora_final:
                self.evento.ejecutar_accion(self)

                # TODO CAPAZ ACÁ DEBERÍA IR LO DE GUARDAR LA FILA EN LA BDD, NO LO TENGO DEL TODO CLARO, DEBERÍA EMPEZAR A PROBAR COMO FUNCIONA ESTO
                #  SEGURO VIENDO EL RESULTADO QUE SE PRINTEA Y COMPARANDO CON EL EXCEL YA ME QUEDA MÁS CLARO

                self.evento = self.proximo_evento

                #todo ------------------------------------ TODO ----------------------------
                #TODO CREAR ALGÚN MÉTODO QUE EJECUTE LA SIMULACIÓN CON PARÁMETROS HARDCODEADOS O INGRESADOS POR CONSOLA Y
                # DESPUÉS PRINTEÉ POR CONSOLA EL RESULTADO, ESTO CON LA FINALIDAD DE PROBAR QUE LA SIMULACIÓN FUNCIONA BIEN,
                # Y QUE LOS RESULTADOS QUE SE OBTIENEN SON LOS ESPERADOS, COMPARANDO CON EL EXCEL DE PRUEBA QUE HICIMOS EN LA PRIMERA ENTREGA







