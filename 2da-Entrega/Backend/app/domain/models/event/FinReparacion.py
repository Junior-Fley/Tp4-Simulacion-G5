import random

from app.domain.models.Equipo import Equipo
from app.domain.models.EstadoTecnico import EstadoTecnico
from app.domain.models.event.Evento import Evento
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular

class FinReparacion(Evento):
    def __init__(self):
            super().__init__("Fin_Reparación")

    def ejecutar_accion(self, simulacion: Simular):

        # Actualizo la hora actual con el tiempo restante de reparacion del equipo
        # que está primero en la cola de equipos
        simulacion.hora_actual += simulacion.cola_equipos.primero().tiempo_reparacion_restante

        # Retiro el equipo que se acaba de reparar de la cola de equipos
        simulacion.cola_equipos.retirar()

        # Ahora queda calcular cuál es el próximo evento a ejecutar

        if simulacion.cola_clientes.cantidad() > 0: # si hay clientes en la cola, entonces el próximo evento puede ser el fin de atención del próximo cliente, o la llegada de un nuevo cliente
            # si termine de atender a un cliente y hay clientes en la cola, entonces, debo comenzar la atención del siguiente cliente, entonces calculo el
            # tiempo de atención del siguiente cliente, y luego comparo si el próximo evento es la llegada de un nuevo cliente o el fin de atención del cliente actual

            simulacion.rnd_atencion = round(random.random(), 3)
            simulacion.tiempo_hasta_fin_de_atencion = simulacion.uniforme(simulacion.rnd_atencion, simulacion.min_atencion, simulacion.max_atencion)


            if simulacion.tiempo_hasta_fin_de_atencion < simulacion.tiempo_hasta_proxima_llegada:
                from app.domain.models.event.FinAtencion import FinAtencion
                simulacion.proximo_evento = FinAtencion()
            else:
                from app.domain.models.event.LlegaCliente import LlegaCliente
                simulacion.proximo_evento = LlegaCliente()
        else:
            # si no hay clientes en la cola, entonces el próximo evento puede ser la llegada de un nuevo cliente o la reparación de un equipo
            if simulacion.cola_equipos.cantidad() > 0: # si hay equipos en la cola, entonces el próximo evento puede ser la reparación de un equipo o la llegada de un nuevo cliente

                primer_equipo: Equipo = simulacion.cola_equipos.primero()

                if primer_equipo.tiempo_de_reparacion is None:
                    # es la primera vez que se trabaja con este equipo, debo calcular cuanto va a tardar en repararse

                    simulacion.rnd_reparacion = round(random.random(), 3)
                    simulacion.tiempo_hasta_reparacion = simulacion.exponencial_negativa(simulacion.media_reparacion,
                                                                                         simulacion.rnd_reparacion)

                    # le asigno al primer equipo el tiempo de reparación que acabo de calcular
                    primer_equipo.tiempo_de_reparacion = simulacion.tiempo_hasta_reparacion
                    primer_equipo.tiempo_reparacion_restante = simulacion.tiempo_hasta_reparacion

                if simulacion.cola_equipos.primero().tiempo_reparacion_restante < simulacion.tiempo_hasta_proxima_llegada:
                    simulacion.proximo_evento = FinReparacion()
                else:
                    from app.domain.models.event.LlegaCliente import LlegaCliente
                    simulacion.proximo_evento = LlegaCliente()

                    # Si se interrumpe la reparacion del equipo, tengo que guardar los datos del tiempo que lo reparé y actualizar el tiempo faltante



            else:
                # si no hay clientes ni equipos en la cola, entonces el próximo evento es la llegada de un nuevo cliente
                from app.domain.models.event.LlegaCliente import LlegaCliente
                simulacion.proximo_evento = LlegaCliente()
        
        # TODO Revisar logica del equipo, creo que nos falta guardar la informacion cuando se le interrumpe