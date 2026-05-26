from __future__ import annotations
import random

from app.domain.models.event.Evento import Evento
from app.domain.models.Equipo import Equipo
from app.domain.models.EstadoEquipo import EstadoEquipo

from typing import TYPE_CHECKING

from app.domain.models.EstadoTecnico import EstadoTecnico
from app.domain.models.EstadoCliente import EstadoCliente

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

        # 2 - Elimino al cliente de la fila
        # si retiro un cliente de la cola el caché se ensucia
        simulacion.cola_clientes.marcar_dirty()
        simulacion.cola_clientes.retirar()

        # reviso si termine de atender con el local cerrado y si es así, reviso si quedan clientes en la cola
        if simulacion.hora_actual > simulacion.hora_cierre:
            if simulacion.cola_clientes.cantidad() > 0:
                # si quedan clientes en la cola, entonces los echo de la tienda
                simulacion.clientes_no_atendidos += simulacion.cola_clientes.cantidad()
                # les marco el estado como echados
                for cliente in simulacion.cola_clientes.elementos:
                    cliente.estado = EstadoCliente.NO_ATENDIDO_POR_CIERRE.value
                # actualizo el serial de la fila para que refleje los cambios
                simulacion.cola_clientes.marcar_dirty()
                simulacion.cola_clientes.serialize()
                #vacio la cola
                simulacion.cola_clientes.vaciar()
            # si ya con la tienda cerrada me quedan equipos por reparar, entonces, empiezo a repararlos
            if simulacion.cola_equipos.cantidad() > 0:
                # Actualizo el estado del técnico
                simulacion.tecnico.estado = EstadoTecnico.REPARANDO

                # calculo el tiempo que me tomara reparar el primer dispositivo de la cola
                self.calcular_tiempo_hasta_reparacion(simulacion)

                # como la tienda ya está cerrada, no voy a atender a nadie más, entonces no necesito comprobar si me van
                # a interrumpir o no, se que no van a venir más clientes.

                from app.domain.models.event.FinReparacion import FinReparacion
                # el proximo evento va a ser un fin de reparación
                simulacion.proximo_evento = FinReparacion()
            # si terminé de atender al último cliente a puertas cerradas y no me queda ningún equipo por reparar, entonces
            # el técnico se va a su casa, queda libre y el proximo evento es la apertura del día siguiente
            else:
                # Actualizo el estado del técnico
                simulacion.tecnico.estado = EstadoTecnico.LIBRE
                from app.domain.models.event.AbreTienda import AbreTienda
                # defino el proximo evento como la apertura de la tienda a las 10:00 AM del día siguiente
                simulacion.proximo_evento = AbreTienda()

            # necesito asegurarme de no pisar nada de lo que definí acá,
            # si la tienda efectivamente cerró, entoncés la lógica de abajo no le aplica
            return # corta la ejecución del método

        # terminamos de atender a un cliente antes de la hora de cierre
        elif simulacion.hora_actual < simulacion.hora_cierre:

            # 3 - Se calcula si el cliente acepta la reparación o no
            simulacion.rnd_presupuesto = random.random()

            simulacion.presupuesto = "Normal"

            # 3.5 verificamos si el presupuesto fue bajo o elevado y si aceptó o no
            simulacion.acepto = True
            if simulacion.rnd_presupuesto < 0.3:
                simulacion.presupuesto = "Elevado"
                simulacion.rnd_acepta = random.random()
                if simulacion.rnd_acepta < 0.5:
                    simulacion.acepto = False

            # 4 - Si aceptó, deja el dispositivo, por lo que lo agrego a la fila
            if simulacion.acepto:
                simulacion.contador_equipos += 1
                id_equipo = simulacion.contador_equipos
                nuevo_equipo = Equipo(id_equipo, EstadoEquipo.EN_COLA_REPARACION,
                                      simulacion.hora_actual, None,
                                      None, None, 0)

                # si agrego equipos a la cola, entonces mi caché de la cola de clientes se vuelve sucio, por lo que tengo que marcarlo como tal
                simulacion.cola_equipos.marcar_dirty()
                simulacion.cola_equipos.agregar(nuevo_equipo)


        # 5 - Defino cuál es el próximo evento a ejecutar

        # si hay clientes en cola
        if simulacion.cola_clientes.cantidad() > 0:
            # entonces el próximo evento puede ser el fin de atención del próximo cliente, o la llegada de un nuevo cliente
            # si termine de atender a un cliente y hay clientes en la cola, entonces, debo comenzar la atención del siguiente cliente, entonces calculo el
            # tiempo de atención del siguiente cliente, y luego comparo si el próximo evento es la llegada de un nuevo cliente o el fin de atención del cliente actual

            # Actualizo el estado del técnico
            simulacion.tecnico.estado = EstadoTecnico.ATENDIENDO_CLIENTE
            # Actualizo el estado del cliente

            primero = simulacion.cola_clientes.primero()
            primero.estado = EstadoCliente.SIENDO_ATENDIDO.value

            simulacion.cola_clientes.modificar_primero(primero)

            # Calculo el tiempo de atencion
            simulacion.rnd_atencion = random.random()
            simulacion.tiempo_hasta_fin_de_atencion = simulacion.uniforme(simulacion.rnd_atencion, simulacion.min_atencion, simulacion.max_atencion)
            simulacion.hora_proximo_fin_atencion = simulacion.hora_actual + simulacion.tiempo_hasta_fin_de_atencion

            # si lo proximo es un fin de atencion
            if simulacion.hora_proximo_fin_atencion < simulacion.hora_proxima_llegada:
                simulacion.proximo_evento = FinAtencion()
            # si lo proximo es la llegada de un nuevo cliente
            else:
                from app.domain.models.event.LlegaCliente import LlegaCliente
                simulacion.proximo_evento = LlegaCliente()
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # si no hay clientes en la cola
        else:
            # entonces el próximo evento puede ser la llegada de un nuevo cliente o la reparación de un equipo
            # de cualquier forma, si no hay clientes en la cola, entonces debo empezar a reparar el primer equipo de la cola,
            # así que debo calcular el tiempo de reparación del equipo, y luego comparar si el próximo evento es la llegada de un nuevo cliente o la reparación del equipo
            if simulacion.cola_equipos.cantidad() > 0:
                # si hay equipos en la cola

                # Actualizo el estado del técnico
                simulacion.tecnico.estado = EstadoTecnico.REPARANDO

                primer_equipo: Equipo = self.calcular_tiempo_hasta_reparacion(simulacion)

                primer_equipo.estado = EstadoEquipo.EN_REPARACION.value

                simulacion.cola_equipos.modificar_primero(primer_equipo)

                # calculo a que hora terminaría de reparar el equipo si no me interrumpen
                hora_fin_reparacion = simulacion.hora_actual + simulacion.tiempo_hasta_reparacion

                # determino si llego a terminar de reparar sin que me interrumpan o me interrumpen antes
                # si no me interrumpen antes
                if hora_fin_reparacion < simulacion.hora_proxima_llegada:
                    from app.domain.models.event.FinReparacion import FinReparacion
                    simulacion.proximo_evento = FinReparacion()
                    # si el evento es un fin de reparación entonces efectivamente se terminó con la reparación actual, así que no debo devolver el equipo a la cola
                else:
                    # si me interrumpen antes
                    from app.domain.models.event.LlegaCliente import LlegaCliente
                    simulacion.proximo_evento = LlegaCliente()
                    # si el evento es que llega un cliente, entonces se interrumpe la reparación del equipo, por lo cual debo devolver
                    # el equipo a la cola, pero con el tiempo de reparación actualizado, para que cuando vuelva a salir el equipo de la cola, sepa cuánto tiempo le falta para ser reparado

                    tiempo_transcurrido_reparando = simulacion.hora_proxima_llegada - simulacion.hora_actual

                    primer_equipo.tiempo_reparacion_restante -= tiempo_transcurrido_reparando
                    primer_equipo.estado = EstadoEquipo.REPARACION_INTERRUPIDA.value

                    # al principio de llega_cliente se calcula y se suma el tiempo correspondiente al acumulador de
                    # reparación del técnico, no es necesario calcular y acumular acá

                    #se actualiza el tiempo restante para ser reparado
                    simulacion.cola_equipos.modificar_primero(primer_equipo)
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            else:
                # si no hay equipos en la cola
                # Actualizo el estado del tecnico
                simulacion.tecnico.estado = EstadoTecnico.LIBRE
                # Va a estar libre hasta que llegue un cliente
                from app.domain.models.event.LlegaCliente import LlegaCliente
                simulacion.proximo_evento = LlegaCliente()