from __future__ import annotations
from app.domain.models.Cliente import Cliente
from app.domain.models.EstadoCliente import EstadoCliente
from app.domain.models.event.Evento import Evento

import random

from typing import TYPE_CHECKING

from app.domain.models.EstadoTecnico import EstadoTecnico

if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular

class LlegaCliente(Evento):
    def __init__(self):
        super().__init__("Llega_Cliente")

    def ejecutar_accion(self, simulacion: Simular):

        #todo revisar
        simulacion.proximo_evento_2 = None


        if simulacion.tecnico.estado == EstadoTecnico.ATENDIENDO_CLIENTE:
            simulacion.tecnico.acum_atencion += simulacion.hora_proxima_llegada - simulacion.hora_actual
        elif simulacion.tecnico.estado == EstadoTecnico.REPARANDO:
            simulacion.tecnico.acum_reparacion += simulacion.hora_proxima_llegada - simulacion.hora_actual

        simulacion.hora_actual = simulacion.hora_proxima_llegada

        # si acaba de llegar un cliente y son más de las 18hs, la puerta está cerrada, por lo cual este cliente no debería nunca entrar a la cola
        if simulacion.hora_actual < simulacion.hora_cierre:
            simulacion.contador_clientes += 1
            id_cliente = simulacion.contador_clientes
            cliente = Cliente(id_cliente, EstadoCliente.EN_COLA)

            # si agrego clientes a la cola, entonces mi caché de la cola de clientes se vuelve sucio, por lo que tengo que marcarlo como tal
            simulacion.cola_clientes.marcar_dirty()
            simulacion.cola_clientes.agregar(cliente)

            simulacion.rnd_llegada = random.random()
            simulacion.tiempo_hasta_proxima_llegada = simulacion.exponencial_negativa(
                simulacion.media_llegada,
                simulacion.rnd_llegada
            )
            # calculo la hora a la que llegaría el proximo cliente
            simulacion.hora_proxima_llegada = simulacion.hora_actual + simulacion.tiempo_hasta_proxima_llegada
            # sea cual sea la situación si acaba de llegar un cliente, mi técnico tiene que estar atendiendo, o al que llego o al que esté primero
            simulacion.tecnico.estado = EstadoTecnico.ATENDIENDO_CLIENTE

            # si el primer cliente de la cola está en cola, es decir todavía no se comenzó a atenderlo, entonces se comienza a atenderlo
            if simulacion.cola_clientes.primero().estado == EstadoCliente.EN_COLA.value:

                primero = simulacion.cola_clientes.primero()
                primero.estado = EstadoCliente.SIENDO_ATENDIDO.value
                simulacion.cola_clientes.modificar_primero(primero)
                simulacion.rnd_atencion = random.random()
                # calculo cuanto durará la atención del primer cliente de la cola
                simulacion.tiempo_hasta_fin_de_atencion = simulacion.uniforme(
                    simulacion.rnd_atencion,
                    simulacion.min_atencion,
                    simulacion.max_atencion
                )
                # calculo la hora a la que terminaré de atender al primer cliente de la cola
                simulacion.hora_proximo_fin_atencion = simulacion.hora_actual + simulacion.tiempo_hasta_fin_de_atencion

        # que pasa si acaba de llegar un cliente, y el próximo llegaría cuando ya cerré las puertas del local
        if simulacion.hora_proxima_llegada > simulacion.hora_cierre:
            # A las 18:00 hs se cierran las puertas del local, entonces, asumo que no voy a dejar entrar a nadie a las 18:01 hs en adelante.
            # marco que cerré las puertas del local
            simulacion.local_abierto = False
            # me fijo si en la cola de clientes me queda un cliente que está siendo atendido ahora mismo, en cuyo caso debo terminar de atenderlo
            if simulacion.cola_clientes.cantidad() > 0 and simulacion.cola_clientes.primero().estado == EstadoCliente.SIENDO_ATENDIDO.value:
                #si es así, entonces lo termino de atender completamente a puertas cerradas si hace falta
                from app.domain.models.event.FinAtencion import FinAtencion
                simulacion.proximo_evento = FinAtencion()
                # si esto ocurre después del cierre, primero cierro
                if simulacion.hora_proximo_fin_atencion > simulacion.hora_cierre:
                    from app.domain.models.event.CierraTienda import CierraTienda
                    simulacion.proximo_evento = CierraTienda()
                    simulacion.proximo_evento_2 = FinAtencion()
            # si no hay clientes en la cola, pero si hay equipos para reparar en la cola, entonces reparo.
            elif simulacion.cola_equipos.cantidad() > 0:
                # Actualizo el estado del técnico
                simulacion.tecnico.estado = EstadoTecnico.REPARANDO
                self.calcular_tiempo_hasta_reparacion(simulacion)
                from app.domain.models.event.FinReparacion import FinReparacion
                simulacion.proximo_evento = FinReparacion()
                # si esto ocurre después del cierre, primero cierro
                if simulacion.cola_equipos.primero().tiempo_reparacion_restante is not None:
                    if simulacion.hora_actual + simulacion.cola_equipos.primero().tiempo_reparacion_restante > simulacion.hora_cierre:
                        from app.domain.models.event.CierraTienda import CierraTienda
                        simulacion.proximo_evento = CierraTienda()
                        simulacion.proximo_evento_2 = FinReparacion()
                # si no hay clientes ni equipos en las colas, entonces mi técnico se puede ir a casa tranquilo
                # y la proxima acción será la apertura de la tienda del día siguiente
            else:
                from app.domain.models.event.AbreTienda import AbreTienda
                simulacion.tecnico.estado = EstadoTecnico.LIBRE
                from app.domain.models.event.CierraTienda import CierraTienda
                simulacion.proximo_evento = CierraTienda()
                simulacion.proximo_evento_2 = AbreTienda()
            return


        if simulacion.hora_proxima_llegada > simulacion.hora_proximo_fin_atencion:
            from app.domain.models.event.FinAtencion import FinAtencion
            simulacion.proximo_evento = FinAtencion()
            # si esto ocurre después del cierre, primero cierro
            if simulacion.hora_proximo_fin_atencion > simulacion.hora_cierre:
                from app.domain.models.event.CierraTienda import CierraTienda
                simulacion.proximo_evento = CierraTienda()
                simulacion.proximo_evento_2 = FinAtencion()
        else:
            simulacion.proximo_evento = LlegaCliente()
            # si esto ocurre después del cierre, primero cierro
            if simulacion.hora_proxima_llegada > simulacion.hora_cierre:
                from app.domain.models.event.CierraTienda import CierraTienda
                simulacion.proximo_evento = CierraTienda()
                simulacion.proximo_evento_2 = LlegaCliente()