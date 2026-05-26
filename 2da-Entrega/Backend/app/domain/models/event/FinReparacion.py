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

        # Aumentamos el acumulador del tecnico
        simulacion.tecnico.acum_reparacion += simulacion.cola_equipos.primero().tiempo_reparacion_restante

        # Retiro el equipo que se acaba de reparar de la cola de equipos
        # si retiro un equipo de la cola, el caché se vuelve dirty
        simulacion.cola_equipos.marcar_dirty()
        simulacion.cola_equipos.retirar()

        # Ahora queda calcular cuál es el próximo evento a ejecutar

        if simulacion.hora_actual >= simulacion.hora_cierre:
            # todo, por el momento elijo asumir que no va a pasar lo imposible y que nunca vamos a estar reparando dispositivos
            # todo mientras hay clientes en la cola
            # si hay equipos en la cola y la tienda ya cerró, entonces el próximo evento DEBE SER la reparación de un equipo
            if simulacion.cola_equipos.cantidad() > 0:
                # si hay equipos en la cola, entonces el técnico empieza a reparar
                # actualizo estado
                simulacion.tecnico.estado = EstadoTecnico.REPARANDO

                # calculo el tiempo de reparación del primer dispositivo de la cola
                primer_equipo: Equipo = self.calcular_tiempo_hasta_reparacion(simulacion)
                # me aseguro de que se refleje el cambio del cálculo del tiempo restante del equipo
                simulacion.cola_equipos.modificar_primero(primer_equipo)
                # no necesito revisar si es que me interrumpen o no, tengo la certeza de que no me van a interrumpir
                simulacion.proximo_evento = FinReparacion()
            # si no hay equipos en la cola para ser reparados y la tienda está cerrada, entonces quedo libre
            # y el próximo evento debe ser la apertura de la tienda el día siguiente a las 10 AM
            else:
                #Marco el proximo evento como la apertura de la tienda
                from domain.models.event.AbreTienda import AbreTienda
                simulacion.proximo_evento = AbreTienda()
        else:
            # si hay clientes en la cola, entonces el próximo evento puede ser el fin de atención del próximo cliente, o la llegada de un nuevo cliente
            # todo según yo esto nunca debería llegar a pasar, pero por las dudas lo dejo, de cualquier forma no hace daño
            if simulacion.cola_clientes.cantidad() > 0:
                # TODO eventualmente eliminar estos print debug
                print('-'*100)
                print()
                print('-'*100)
                print('PASO LO IMPOSIBLE, TERMINE DE REPARAR UN EQUIPO MIENTRAS HABÍA CLIENTES EN LA COLA')
                print('-'*100)
                print()
                print('-0'*100)
                # si termine de reparar y hay clientes en la cola, entonces, debo comenzar la atención del siguiente cliente:

                # actualizo el estado del técnico
                simulacion.tecnico.estado = EstadoTecnico.ATENDIENDO_CLIENTE

                # entonces calculo el tiempo de atención del siguiente cliente
                simulacion.rnd_atencion = random.random()
                simulacion.tiempo_hasta_fin_de_atencion = simulacion.uniforme(simulacion.rnd_atencion, simulacion.min_atencion, simulacion.max_atencion)
                simulacion.hora_proximo_fin_atencion = simulacion.hora_actual + simulacion.tiempo_hasta_fin_de_atencion

                # comparo si el próximo evento es la llegada de un nuevo cliente o el fin de atención del cliente actual
                if simulacion.hora_proximo_fin_atencion < simulacion.hora_proxima_llegada:
                    from app.domain.models.event.FinAtencion import FinAtencion
                    simulacion.proximo_evento = FinAtencion()
                else:
                    from app.domain.models.event.LlegaCliente import LlegaCliente
                    simulacion.proximo_evento = LlegaCliente()
            # este debería ser el camino default, no veo como podría entrar al if de arriba
            # SI TERMINO DE REPARAR Y NO HAY CLIENTES EN LA COLA:
            else:
                # si no hay clientes en la cola, entonces el próximo evento puede ser la llegada de un nuevo cliente o la reparación de un equipo
                # si hay equipos en la cola, entonces el próximo evento puede ser la reparación de un equipo o la llegada de un nuevo cliente
                if simulacion.cola_equipos.cantidad() > 0:
                    # si hay equipos en la cola, entonces el técnico empieza a reparar
                    # actualizo estado
                    simulacion.tecnico.estado = EstadoTecnico.REPARANDO

                    # calculo el tiempo de reparación del primer dispositivo de la cola
                    primer_equipo: Equipo = self.calcular_tiempo_hasta_reparacion(simulacion)

                    # calculo a que hora terminaría de reparar el equipo si no me interrumpen
                    hora_fin_reparacion = simulacion.hora_actual + simulacion.tiempo_hasta_reparacion


                    if hora_fin_reparacion < simulacion.hora_proxima_llegada:
                        simulacion.proximo_evento = FinReparacion()
                    else:
                        from app.domain.models.event.LlegaCliente import LlegaCliente

                        # Si se interrumpe la reparacion del equipo, tengo que guardar los datos del tiempo que lo reparé y actualizar el tiempo faltante

                        tiempo_transcurrido_reparando = simulacion.hora_proxima_llegada - simulacion.hora_actual

                        primer_equipo.tiempo_reparacion_restante -= tiempo_transcurrido_reparando

                        simulacion.cola_equipos.modificar_primero(primer_equipo)

                        simulacion.proximo_evento = LlegaCliente()


                else:
                    # Si no hay equipos en la cola, entonces quedo libre hasta la llegada de un proximo cliente
                    simulacion.tecnico.estado = EstadoTecnico.LIBRE
                    # si no hay clientes ni equipos en la cola, entonces el próximo evento es la llegada de un nuevo cliente
                    from app.domain.models.event.LlegaCliente import LlegaCliente
                    simulacion.proximo_evento = LlegaCliente()
