from __future__ import annotations
import random

from app.domain.models.Equipo import Equipo
from app.domain.models.EstadoTecnico import EstadoTecnico
from app.domain.models.event.Evento import Evento
from typing import TYPE_CHECKING

from app.domain.models.EstadoEquipo import EstadoEquipo

if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular

class FinReparacion(Evento):
    def __init__(self):
            super().__init__("Fin_Reparación")

    def ejecutar_accion(self, simulacion: Simular):
        # Actualizo la hora actual con el tiempo restante de reparacion del equipo
        # que está primero en la cola de equipos
        equipo_reparado = simulacion.cola_equipos.primero()
        simulacion.hora_actual += equipo_reparado.tiempo_reparacion_restante

        # Aumentamos el acumulador del tecnico
        simulacion.tecnico.acum_reparacion += equipo_reparado.tiempo_reparacion_restante

        # antes de retirar de la cola al equipo, debería asignarle su valor de tiempo fin y su estado reparado
        equipo_reparado.horario_fin_reparacion = simulacion.hora_actual
        equipo_reparado.estado = EstadoEquipo.REPARADO.value

        # guardo en la cola los cambios realizados al primer equipo
        simulacion.cola_equipos.modificar_primero(equipo_reparado)

        # debo mostrar estos cambios que le hice al primer equipo de la cola en el serialize siguiente, pero no en el
        # 2do siguiente, entonces, uso el marcar_dirty_2do

        # marco dirty normal para guardar los cambios actuales
        simulacion.cola_equipos.marcar_dirty()
        # serialize para que se guarden los cambios al caché
        simulacion.cola_equipos.serialize()
        # uso este méthod para asegurarme que el siguiente serialize no reescriba la caché, pero el que le siga
        # a ese, si la reescriba
        simulacion.cola_equipos.marcar_dirty_segunda()


        # debo acumular el tiempo que pasaron los equipos en el local desde que entraron hasta que salieron
        tiempo_transcurrido_en_local = equipo_reparado.horario_fin_reparacion - equipo_reparado.hora_ingreso_taller

        # acumulo el tiempo total que el equipo pasó en el taller
        simulacion.acum_tiempo_equipos += tiempo_transcurrido_en_local


        # Retiro el equipo que se acaba de reparar de la cola de equipos
        # si retiro un equipo de la cola, el caché se vuelve dirty
        # todo ya no necesito marcar dirty acá, se marcó dirty 2da arriba
        simulacion.cola_equipos.retirar()
        # si retiro el equipo de la cola, entonces ya está reparado
        simulacion.contador_reparaciones += 1

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


                # acá pasa algo chistoso, claro, yo le acabo de calcular el tiempo de reparación al que ahora
                # es el primer equipo de la fila, así que necesito reflejar eso en el caché, pero también es verdad
                # que llegado este punto ya retiré el que antes era el primer equipo de la cola, y también necesito
                # reflejar sus cambios...

                # como soluciono esto... vuelvo a añadir el que era el primer equipo a la cola, en la primera
                # posición y vuelvo a re-serializarlo

                simulacion.cola_equipos.agregar_primero(equipo_reparado)

                # para este punto en la cola ya está el equipo reparado con sus cambios reflejados
                # y también el que empecé a reparar con sus cambios reflejados en la 2da posición

                # guardo estos cambios en el caché
                simulacion.cola_equipos.marcar_dirty()
                simulacion.cola_equipos.serialize()

                # marco dirty segunda para que el 2do serialize ya no esté muestre más el equipo reparado
                simulacion.cola_equipos.marcar_dirty_segunda()

                # vuelvo a retirar el primer equipo de la cola para que no cause desgracias
                simulacion.cola_equipos.retirar()

            # si no hay equipos en la cola para ser reparados y la tienda está cerrada, entonces quedo libre
            # y el próximo evento debe ser la apertura de la tienda el día siguiente a las 10 AM
            else:
                #Marco el proximo evento como la apertura de la tienda
                from app.domain.models.event.AbreTienda import AbreTienda
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

                    # cálculo el tiempo de reparación del primer dispositivo de la cola
                        # esta función también se encarga de actualizar el estado y los tiempos y reflejar esos cambios en la cola
                    primer_equipo: Equipo = self.calcular_tiempo_hasta_reparacion(simulacion)

                    # calculo a que hora terminaría de reparar el equipo si no me interrumpen
                    hora_fin_reparacion = simulacion.hora_actual + simulacion.tiempo_hasta_reparacion


                    if hora_fin_reparacion < simulacion.hora_proxima_llegada:
                        # ---------------------------------------------
                        # acá pasa algo chistoso, claro, yo le acabo de calcular el tiempo de reparación al que ahora
                        # es el primer equipo de la fila, así que necesito reflejar eso en el caché, pero también es verdad
                        # que llegado este punto ya retiré el que antes era el primer equipo de la cola, y también necesito
                        # reflejar sus cambios...
                        # -----------------------------------------------
                        # como soluciono esto... vuelvo a añadir el que era el primer equipo a la cola, en la primera
                        # posición y vuelvo a re-serializarlo

                        simulacion.cola_equipos.agregar_primero(equipo_reparado)

                        # para este punto en la cola ya está el equipo reparado con sus cambios reflejados
                        # y también el que empecé a reparar con sus cambios reflejados en la 2da posición

                        # guardo estos cambios en el caché
                        simulacion.cola_equipos.marcar_dirty()
                        simulacion.cola_equipos.serialize()

                        # marco dirty segunda para que el 2do serialize ya no esté muestre más el equipo reparado
                        simulacion.cola_equipos.marcar_dirty_segunda()

                        # vuelvo a retirar el primer equipo de la cola para que no cause desgracias
                        simulacion.cola_equipos.retirar()



                        simulacion.proximo_evento = FinReparacion()
                    else:
                        from app.domain.models.event.LlegaCliente import LlegaCliente

                        # Si se interrumpe la reparacion del equipo, tengo que guardar los datos del tiempo que lo reparé y actualizar el tiempo faltante

                        tiempo_transcurrido_reparando = simulacion.hora_proxima_llegada - simulacion.hora_actual

                        primer_equipo.tiempo_reparacion_restante -= tiempo_transcurrido_reparando

                        simulacion.cola_equipos.modificar_primero(primer_equipo)

                        # ---------------------------------------------
                        # acá pasa algo chistoso, claro, yo le acabo de calcular el tiempo de reparación al que ahora
                        # es el primer equipo de la fila, así que necesito reflejar eso en el caché, pero también es verdad
                        # que llegado este punto ya retiré el que antes era el primer equipo de la cola, y también necesito
                        # reflejar sus cambios...
                        # -----------------------------------------------
                        # como soluciono esto... vuelvo a añadir el que era el primer equipo a la cola, en la primera
                        # posición y vuelvo a re-serializarlo

                        simulacion.cola_equipos.agregar_primero(equipo_reparado)

                        # para este punto en la cola ya está el equipo reparado con sus cambios reflejados
                        # y también el que empecé a reparar con sus cambios reflejados en la 2da posición

                        # guardo estos cambios en el caché
                        simulacion.cola_equipos.marcar_dirty()
                        simulacion.cola_equipos.serialize()

                        # marco dirty segunda para que el 2do serialize ya no esté muestre más el equipo reparado
                        simulacion.cola_equipos.marcar_dirty_segunda()

                        # vuelvo a retirar el primer equipo de la cola para que no cause desgracias
                        simulacion.cola_equipos.retirar()

                        simulacion.proximo_evento = LlegaCliente()


                else:
                    # Si no hay equipos en la cola, entonces quedo libre hasta la llegada de un proximo cliente
                    simulacion.tecnico.estado = EstadoTecnico.LIBRE
                    # si no hay clientes ni equipos en la cola, entonces el próximo evento es la llegada de un nuevo cliente
                    from app.domain.models.event.LlegaCliente import LlegaCliente
                    simulacion.proximo_evento = LlegaCliente()
