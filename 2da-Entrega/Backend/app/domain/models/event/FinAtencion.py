import random

from app.domain.models.event.Evento import Evento
from app.domain.models.Equipo import Equipo
from app.domain.models.EstadoEquipo import EstadoEquipo

from typing import TYPE_CHECKING

from app.domain.models.EstadoTecnico import EstadoTecnico

if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular

class FinAtencion(Evento):
    def __init__(self):
        super().__init__("Fin_Atención")

    def ejecutar_accion(self, simulacion: Simular):

        # Aumentamos el acumulador del tecnico
        simulacion.tecnico.acum_atencion += simulacion.hora_proximo_fin_atencion - simulacion.hora_actual

        # 1 - Actualizo la hora
        simulacion.hora_actual = simulacion.hora_proximo_fin_atencion

        if simulacion.hora_actual > simulacion.hora_final:
            simulacion.clientes_no_atendidos = simulacion.cola_clientes.cantidad()
            simulacion.cola_clientes.vaciar()

        # 2 - Elimino al cliente de la fila
        simulacion.cola_clientes.retirar()

        # 3 - Se calcula si el cliente acepta la reparación o no
        simulacion.rnd_presupuesto = random.random()

        simulacion.presupuesto = "Normal"
        simulacion.tiempo_hasta_reparacion = None #TODO revisar esto

        simulacion.acepto = True
        if simulacion.rnd_presupuesto < 0.3:
            simulacion.presupuesto = "Elevado"
            simulacion.rnd_acepta = random.random()
            if simulacion.rnd_acepta < 0.5:
                simulacion.acepto = False

        # 4 - Si aceptó, deja el dispositivo, por lo que lo agrego a la fila
        if simulacion.acepto:
            nuevo_equipo = Equipo(EstadoEquipo.EN_COLA_REPARACION, simulacion.hora_actual, None,
                                  None, None, 0)

            simulacion.cola_equipos.agregar(nuevo_equipo)

        # 5 - Defino cuál es el próximo evento a ejecutar

        if self.comprobar_hora_final(simulacion):
            return


        if simulacion.cola_clientes.cantidad() > 0:
            # si hay clientes en la cola, entonces el próximo evento puede ser el fin de atención del próximo cliente, o la llegada de un nuevo cliente
            # si termine de atender a un cliente y hay clientes en la cola, entonces, debo comenzar la atención del siguiente cliente, entonces calculo el
            # tiempo de atención del siguiente cliente, y luego comparo si el próximo evento es la llegada de un nuevo cliente o el fin de atención del cliente actual

            # Actualizo el estado del técnico
            simulacion.tecnico.estado = EstadoTecnico.ATENDIENDO_CLIENTE

            # Calculo el tiempo de atencion
            simulacion.rnd_atencion = random.random()
            simulacion.tiempo_hasta_fin_de_atencion = simulacion.uniforme(simulacion.rnd_atencion, simulacion.min_atencion, simulacion.max_atencion)
            simulacion.hora_proximo_fin_atencion = simulacion.hora_actual + simulacion.tiempo_hasta_fin_de_atencion


            if simulacion.hora_proximo_fin_atencion < simulacion.hora_proxima_llegada:
                simulacion.proximo_evento = FinAtencion()
            else:
                from app.domain.models.event.LlegaCliente import LlegaCliente
                simulacion.proximo_evento = LlegaCliente()
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        else:
            # si no hay clientes en la cola, entonces el próximo evento puede ser la llegada de un nuevo cliente o la reparación de un equipo
            # de cualquier forma, si no hay clientes en la cola, entonces debo empezar a reparar el primer equipo de la cola,
            # así que debo calcular el tiempo de reparación del equipo, y luego comparar si el próximo evento es la llegada de un nuevo cliente o la reparación del equipo
            if simulacion.cola_equipos.cantidad() > 0:

                # Actualizo el estado del técnico
                simulacion.tecnico.estado = EstadoTecnico.REPARANDO

                # si hay equipos en la cola, entonces debo calcular el tiempo de reparación del primer equipo de la cola, si este tiempo no fue calculado antes, es decir, si se está trabajando por primera vez con ese equipo
                primer_equipo: Equipo = simulacion.cola_equipos.primero()

                if primer_equipo.tiempo_de_reparacion is None:

                    # es la primera vez que se trabaja con este equipo, debo calcular cuanto va a tardar en repararse

                    simulacion.rnd_reparacion = random.random()
                    simulacion.tiempo_hasta_reparacion = simulacion.exponencial_negativa(simulacion.media_reparacion,
                                                                                         simulacion.rnd_reparacion)

                    # le asigno al primer equipo el tiempo de reparación que acabo de calcular
                    primer_equipo.tiempo_de_reparacion = simulacion.tiempo_hasta_reparacion
                    primer_equipo.tiempo_reparacion_restante = simulacion.tiempo_hasta_reparacion

                else:
                    simulacion.tiempo_hasta_reparacion = primer_equipo.tiempo_reparacion_restante
                    # si ya se trabajó con este equipo, entonces el tiempo de reparación que falta es el
                    # tiempo de reparación restante que tiene el equipo, que se actualiza cada vez que se interrumpe la reparación

                hora_fin_reparacion = simulacion.hora_actual + simulacion.tiempo_hasta_reparacion

                if hora_fin_reparacion < simulacion.hora_proxima_llegada:
                    from app.domain.models.event.FinReparacion import FinReparacion
                    simulacion.proximo_evento = FinReparacion()
                    # si el evento es un fin de reparación entonces efectivamente se terminó con la reparación actual, así que no debo devolver el equipo a la cola
                else:
                    from app.domain.models.event.LlegaCliente import LlegaCliente
                    simulacion.proximo_evento = LlegaCliente()
                    # si el evento es que llega un cliente, entonces se interrumpe la reparación del equipo, por lo cual debo devolver
                    # el equipo a la cola, pero con el tiempo de reparación actualizado, para que cuando vuelva a salir el equipo de la cola, sepa cuánto tiempo le falta para ser reparado

                    tiempo_transcurrido_reparando = simulacion.hora_proxima_llegada - simulacion.hora_actual

                    primer_equipo.tiempo_reparacion_restante -= tiempo_transcurrido_reparando

                    simulacion.cola_equipos.modificar_primero(primer_equipo)
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            else:
                # Actualizo el estado del tecnico
                simulacion.tecnico.estado = EstadoTecnico.LIBRE
                # Va a estar libre hasta que llegue un cliente
                from app.domain.models.event.LlegaCliente import LlegaCliente
                simulacion.proximo_evento = LlegaCliente()