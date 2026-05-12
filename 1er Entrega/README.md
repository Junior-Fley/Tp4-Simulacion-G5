Para la primera entrega
- Identificación de objetos: nombre, características, atributos (nombre, estado y resto de 
atributos necesarios, cada uno con sus valores posibles)

- Determinación de eventos.

- Colas existentes en el sistema y características.

- ¿Cuáles son las variables aleatorias de este sistema? Indicar la fórmula que se utiliza para 
generar valores para cada variable, reemplazando la fórmula teórica por la que corresponda 
en cada caso


Eventos 
- llegada_Cliente    Exp.neg(45)    x = - 45 . LN(1 - RND)
- Atención_Cliente   Unif(10, 20)   x = 10 + RND (20 - 10)
- Reparacion_taller  Exp.neg(90)    x = - 90 . LN(1 - RND)
- Cierre de Puertas (Evento Temporizado)

Objetos
Permanentes:
- Tecnico
Estados(Atendiendo_Client , Reparando_Equipo, libre )

Temporales:
- Cliente
Estado(atentido, esperando(Cola))
- equipo_reparar
Estado(EnEspera(Cola), Resparacion, Reparado)


