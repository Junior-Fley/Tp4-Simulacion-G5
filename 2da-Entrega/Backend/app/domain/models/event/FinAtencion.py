import random

from app.domain.models.Equipo import Equipo
from app.domain.models.EstadoEquipo import EstadoEquipo
from app.domain.models.event.Evento import Evento
from app.domain.models.event.FinReparacion import FinReparacion
from app.domain.models.event.LlegaCliente import LlegaCliente


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.application.useCases.Simular import Simular

class FinAtencion(Evento):
    def __init__(self):
        super().__init__("Fin_Atención")

    def ejecutar_accion(self, simulacion: Simular):
        simulacion.hora_actual += simulacion.tiempo_hasta_fin_de_atencion
        simulacion.cola_clientes.retirar()


        # se calcula si el cliente acepta la reparación o no
        simulacion.rnd_presupuesto = random.random()
        simulacion.presupuesto = "Normal"
        simulacion.tiempo_hasta_reparacion = None
        simulacion.acepto = True # TODO revisar si esto hace falta mostrarlo en la fila de la simulacion o no, de momento asumí que no, más que nada porque me daba pereza fijarme
        if simulacion.rnd_presupuesto < 0.3:
            simulacion.presupuesto = "Elevado"
            simulacion.rnd_acepta = random.random()
            if simulacion.rnd_acepta < 0.5:
                simulacion.acepto = False


        if simulacion.acepto:  # TODO MOVER ESTO, SE CALCULA CUANTO SE TARDA EN LA REPARACIÓN CUANDO EMPEZAMOS A REPARAR, NO ANTES
            # si llego hasta acá es porque su presupuesto no era elevado, o era elevado, pero
            # aceptó la reparación, entonces se asigna el cliente al técnico
            nuevo_equipo = Equipo(EstadoEquipo.EN_COLA_REPARACION, simulacion.hora_actual, None,
                                  None, None, 0)

            simulacion.cola_equipos.agregar(nuevo_equipo)



        # ahora queda calcular cuál es el próximo evento a ejecutar

        if simulacion.cola_clientes.cantidad() > 0: # si hay clientes en la cola, entonces el próximo evento puede ser el fin de atención del próximo cliente, o la llegada de un nuevo cliente
            # si termine de atender a un cliente y hay clientes en la cola, entonces, debo comenzar la atención del siguiente cliente, entonces calculo el
            # tiempo de atención del siguiente cliente, y luego comparo si el próximo evento es la llegada de un nuevo cliente o el fin de atención del cliente actual

            simulacion.rnd_atencion = random.random()
            simulacion.tiempo_hasta_fin_de_atencion = simulacion.uniforme(simulacion.rnd_atencion, simulacion.min_atencion, simulacion.max_atencion)


            if simulacion.tiempo_hasta_fin_de_atencion < simulacion.tiempo_hasta_proxima_llegada:
                simulacion.evento = FinAtencion()
            else:
                simulacion.evento = LlegaCliente()
        else:
            # si no hay clientes en la cola, entonces el próximo evento puede ser la llegada de un nuevo cliente o la reparación de un equipo
            # de cualquier forma, si no hay clientes en la cola, entonces debo empezar a reparar el primer equipo de la cola,
            # así que debo calcular el tiempo de reparación del equipo, y luego comparar si el próximo evento es la llegada de un nuevo cliente o la reparación del equipo
            if simulacion.cola_equipos.cantidad() > 0:
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


                if simulacion.tiempo_hasta_reparacion < simulacion.tiempo_hasta_proxima_llegada:
                    simulacion.evento = FinReparacion()
                    # si el evento es un fin de reparación entonces efectivamente se terminó con la reparación actual, así que no debo devolver el equipo a la cola
                else:
                    simulacion.evento = LlegaCliente()
                    # si el evento es que llega un cliente, entonces se interrumpe la reparación del equipo, por lo cual debo devolver
                    # el equipo a la cola, pero con el tiempo de reparación actualizado, para que cuando vuelva a salir el equipo de la cola, sepa cuánto tiempo le falta para ser reparado

                    primer_equipo.tiempo_reparacion_restante = primer_equipo.tiempo_reparacion_restante - simulacion.tiempo_hasta_proxima_llegada

                    simulacion.cola_equipos.modificar_primero(primer_equipo)

                # TODO CREO QUE ACÁ VA LO DE GUARDAR LA FILA A LA BDD PERO NO LO TENGO CLARO, CAPAZ LO DE GUARDAR LA FILA A LA BDD SE PUEDE MOVER DE ALGUNA FORMA AL MÉTODO EJECUTAR SIMULACIÓN
                # todo YA QUE ES EN PARTE ALGO COMÚN A TODOS LOS MÉTODOS DE CADA ESTADO... DEBERÍA REVISARLO BIEN LA VERDAD,
                # todo POR AHORA LO DEJO ACÁ MARCADO CON UN TODO, Y QUEDA EL TRABAJO PARA MI YO DEL FUTURO O PARA EL PRÓXIMO QUE TOQUE EL BACKEND