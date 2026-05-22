from app.domain.models.Cliente import Cliente
from app.domain.models.EstadoCliente import EstadoCliente
from app.domain.models.event.Evento import Evento

import random

from typing import TYPE_CHECKING

from app.domain.models.event.FinAtencion import FinAtencion

if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular

class LlegaCliente(Evento):
    def __init__(self):
        super().__init__("Llega_Cliente")

    def ejecutar_accion(self, simulacion: Simular):
        simulacion.hora_actual += simulacion.tiempo_hasta_proxima_llegada

        # creo el nuevo cliente que acaba de llegar, lo agrego a la cola de clientes
        cliente = Cliente(EstadoCliente.EN_COLA, simulacion.hora_actual, None, None)
        simulacion.cola_clientes.agregar(cliente)

        # si ya llegó un cliente, debo calcular cuando llega el próximo
        # se calcula la próxima llegada de un cliente
        simulacion.rnd_llegada = random.random()
        simulacion.tiempo_hasta_proxima_llegada = simulacion.exponencial_negativa(simulacion.media_llegada, simulacion.rnd_llegada)
        simulacion.hora_proxima_llegada = simulacion.hora_actual + simulacion.tiempo_hasta_proxima_llegada

        # se calcula el tiempo de atencion del cliente si corresponde

        if simulacion.cola_clientes.primero() == cliente: # si el cliente que acaba de llegar es el primero en la cola, entonces se atiende inmediatamente, se le calcula el tiempo de atención
            simulacion.rnd_atencion = random.random()
            simulacion.tiempo_hasta_fin_de_atencion = simulacion.uniforme(simulacion.rnd_atencion, simulacion.min_atencion, simulacion.max_atencion)
        # si no es el primero, entonces no le calculo el tiempo de atención, porque no se va a atender hasta que se atienda a los clientes que están antes que él en la cola,
        # entonces no hace falta calcular el tiempo de atención para este cliente ahora, porque se sigue trabajando con el tiempo de atención del cliente actual

        #------------------------------------------ fin generación de la fila de la simulación ------------------------------------------
        # para este punto ya se generó toda la fila de la simulación, entonces ahora se debe decidir cuál va a ser el próximo evento que se va a ejecutar


        # asumo que llega el proximo cliente antes del fin de la atención, entonces no hace falta cambiar el evento de la simulación (sigue siendo LLegaCliente)
        # si finaliza la atención antes de la llegada del próximo cliente entonces cambio el evento de la simulación a FinAtención
        if simulacion.tiempo_hasta_fin_de_atencion < simulacion.tiempo_hasta_proxima_llegada:
            simulacion.proximo_evento = FinAtencion()
        else:
            simulacion.proximo_evento = LlegaCliente()
            # No hace falta revisar si es que el siguiente evento es reparación, pues si acaba de llegar un cliente, lo debo atender si o si
            # excepto que ya este atendiendo a otro cliente, por lo cual solo debo revisar si la proxima acción es el fin de atencion del cliente actual
            # lo que implica que paso a atender a este cliente, o si, en cambio, es la llegada de otro cliente, lo que implica que sigo atendiendo al cliente actual, y el nuevo cliente se queda en la cola
