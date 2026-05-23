from app.domain.models.Cliente import Cliente
from app.domain.models.EstadoCliente import EstadoCliente
from app.domain.models.event.Evento import Evento

import random

from typing import TYPE_CHECKING

from domain.models.EstadoTecnico import EstadoTecnico


if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular
    from app.domain.models.Equipo import Equipo

class LlegaCliente(Evento):
    def __init__(self):
        super().__init__("Llega_Cliente")

    def ejecutar_accion(self, simulacion: Simular):
        # 1 - Actualizo la hora
        simulacion.hora_actual = simulacion.hora_proxima_llegada

        if simulacion.hora_actual >= simulacion.hora_final:
            simulacion.clientes_no_atendidos = simulacion.cola_clientes.cantidad()
            simulacion.cola_clientes.vaciar()

        # 2 - Creo el nuevo cliente que acaba de llegar, lo agrego a la cola de clientes
        cliente = Cliente(EstadoCliente.EN_COLA, simulacion.hora_actual, None, None)
        simulacion.cola_clientes.agregar(cliente)

        # 3- Calculo la próxima llegada de un cliente
        simulacion.rnd_llegada = round(random.random(), 3)
        simulacion.tiempo_hasta_proxima_llegada = simulacion.exponencial_negativa(simulacion.media_llegada, simulacion.rnd_llegada)
        simulacion.hora_proxima_llegada = simulacion.hora_actual + simulacion.tiempo_hasta_proxima_llegada

        # 4 - Actualizo el estado del tecnico
        simulacion.tecnico.estado = EstadoTecnico.ATENDIENDO_CLIENTE

        # 5 - Se calcula el tiempo de atencion del cliente si no hay nadie delante y no empecé a atenderlo.
        if simulacion.cola_clientes.primero().estado == EstadoCliente.EN_COLA:
            simulacion.cola_clientes.primero().estado = EstadoCliente.SIENDO_ATENDIDO
            simulacion.rnd_atencion = round(random.random(), 3)
            simulacion.tiempo_hasta_fin_de_atencion = simulacion.uniforme(simulacion.rnd_atencion, simulacion.min_atencion, simulacion.max_atencion)
            simulacion.hora_proximo_fin_atencion = simulacion.hora_actual + simulacion.tiempo_hasta_fin_de_atencion

        #------------------------------------------ fin generación de la fila de la simulación ------------------------------------------
        # para este punto ya se generó toda la fila de la simulación, entonces ahora se debe decidir cuál va a ser el próximo evento que se va a ejecutar


        # asumo que llega el proximo cliente antes del fin de la atención, entonces no hace falta cambiar el evento de la simulación (sigue siendo LLegaCliente)
        # si finaliza la atención antes de la llegada del próximo cliente entonces cambio el evento de la simulación a FinAtención
        if self.comprobar_hora_final(simulacion):
            return

        if simulacion.hora_proxima_llegada > simulacion.hora_proximo_fin_atencion:
            from app.domain.models.event.FinAtencion import FinAtencion
            simulacion.proximo_evento = FinAtencion()
        else:
            simulacion.proximo_evento = LlegaCliente()
            # No hace falta revisar si es que el siguiente evento es reparación, pues si acaba de llegar un cliente, lo debo atender si o si
            # excepto que ya este atendiendo a otro cliente, por lo cual solo debo revisar si la proxima acción es el fin de atencion del cliente actual
            # lo que implica que paso a atender a este cliente, o si, en cambio, es la llegada de otro cliente, lo que implica que sigo atendiendo al cliente actual, y el nuevo cliente se queda en la cola
