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
        primer_equipo = simulacion.cola_equipos.primero()
        # Si el equipo nunca tuvo tiempo calculado, calcularlo ahora
        if primer_equipo.tiempo_reparacion_restante is None:
            simulacion.rnd_reparacion = random.random()
            simulacion.tiempo_hasta_reparacion = simulacion.exponencial_negativa(
                simulacion.media_reparacion,
                simulacion.rnd_reparacion
            )
            primer_equipo.tiempo_de_reparacion = simulacion.tiempo_hasta_reparacion
            primer_equipo.tiempo_reparacion_restante = simulacion.tiempo_hasta_reparacion

        # # Actualizo la hora actual con el tiempo restante de reparacion del equipo
        # # que está primero en la cola de equipos
        # simulacion.hora_actual += simulacion.cola_equipos.primero().tiempo_reparacion_restante
        #
        # # # Aumentamos el acumulador del tecnico
        # # simulacion.tecnico.acum_reparacion += simulacion.cola_equipos.primero().tiempo_reparacion_restante

        # Actualizo la hora actual con el tiempo restante de reparacion del equipo
        simulacion.hora_actual += primer_equipo.tiempo_reparacion_restante

        # Retiro el equipo que se acaba de reparar de la cola de equipos
        simulacion.cola_equipos.retirar()

        # Ahora queda calcular cuál es el próximo evento a ejecutar

        if self.comprobar_hora_final(simulacion):
            return


        if simulacion.cola_clientes.cantidad() > 0: # si hay clientes en la cola, entonces el próximo evento puede ser el fin de atención del próximo cliente, o la llegada de un nuevo cliente
            # si termine de atender a un cliente y hay clientes en la cola, entonces, debo comenzar la atención del siguiente cliente, entonces calculo el
            # tiempo de atención del siguiente cliente, y luego comparo si el próximo evento es la llegada de un nuevo cliente o el fin de atención del cliente actual
            simulacion.tecnico.estado = EstadoTecnico.ATENDIENDO_CLIENTE
            simulacion.rnd_atencion = random.random()
            simulacion.tiempo_hasta_fin_de_atencion = simulacion.uniforme(simulacion.rnd_atencion, simulacion.min_atencion, simulacion.max_atencion)
            simulacion.hora_proximo_fin_atencion = simulacion.hora_actual + simulacion.tiempo_hasta_fin_de_atencion


            if simulacion.hora_proximo_fin_atencion < simulacion.hora_proxima_llegada:
                from app.domain.models.event.FinAtencion import FinAtencion
                simulacion.proximo_evento = FinAtencion()
            else:
                from app.domain.models.event.LlegaCliente import LlegaCliente
                simulacion.proximo_evento = LlegaCliente()
        else:
            # si no hay clientes en la cola, entonces el próximo evento puede ser la llegada de un nuevo cliente o la reparación de un equipo
            if simulacion.cola_equipos.cantidad() > 0: # si hay equipos en la cola, entonces el próximo evento puede ser la reparación de un equipo o la llegada de un nuevo cliente
                simulacion.tecnico.estado = EstadoTecnico.REPARANDO
                primer_equipo: Equipo = simulacion.cola_equipos.primero()

                if primer_equipo.tiempo_de_reparacion is None:
                    # es la primera vez que se trabaja con este equipo, debo calcular cuanto va a tardar en repararse

                    simulacion.rnd_reparacion = random.random()
                    simulacion.tiempo_hasta_reparacion = simulacion.exponencial_negativa(simulacion.media_reparacion,
                                                                                         simulacion.rnd_reparacion)

                    # le asigno al primer equipo el tiempo de reparación que acabo de calcular
                    primer_equipo.tiempo_de_reparacion = simulacion.tiempo_hasta_reparacion
                    primer_equipo.tiempo_reparacion_restante = simulacion.tiempo_hasta_reparacion


                hora_proxima_reparacion = simulacion.hora_actual + simulacion.cola_equipos.primero().tiempo_reparacion_restante

                if hora_proxima_reparacion < simulacion.hora_proxima_llegada:
                    simulacion.proximo_evento = FinReparacion()
                else:
                    from app.domain.models.event.LlegaCliente import LlegaCliente
                    simulacion.proximo_evento = LlegaCliente()

                    # Si se interrumpe la reparacion del equipo, tengo que guardar los datos del tiempo que lo reparé y actualizar el tiempo faltante

                    tiempo_transcurrido_reparando = simulacion.hora_proxima_llegada - simulacion.hora_actual

                    primer_equipo.tiempo_reparacion_restante -= tiempo_transcurrido_reparando

                    simulacion.cola_equipos.modificar_primero(primer_equipo)


            else:
                simulacion.tecnico.estado = EstadoTecnico.LIBRE
                # si no hay clientes ni equipos en la cola, entonces el próximo evento es la llegada de un nuevo cliente
                from app.domain.models.event.LlegaCliente import LlegaCliente
                simulacion.proximo_evento = LlegaCliente()
        
        # TODO Revisar logica del equipo, creo que nos falta guardar la información cuando se le interrumpe