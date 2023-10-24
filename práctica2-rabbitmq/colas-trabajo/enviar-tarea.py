#!/usr/bin/env python

# Importar el paquete pika, necesario para trabajar con el protocolo de RabbitMQ
import pika

# También se usarán los paquetes 'sys' y 'datetime', para  diversas funciones que se explican en el código.
import sys
import datetime


# Conectarse a la instancia de RabbitMQ, corriendo en nuestro equipo (localhost)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declarar que se usará como canal la cola "prueba2"
channel.queue_declare(queue='prueba2', durable=True)

# El mensaje que se enviará a la cola será el primer valor pasado por parámetros al llamar al script,
# o, en caso de que no se haya pasado ningún valor, "Hola Mundo!"
message = ' '.join(sys.argv[1:]) or "Hola Mundo!"

channel.basic_publish(
    exchange='',

    # Se usa la cola "prueba2"
    routing_key='prueba2',

    # Se envía el valor de la variable "message" como cuerpo del mensaje.
    body=message,

    # Activar el modo persistente de entrega, para que RabbitMQ espere a la confirmación del worker
    # para marcar como entregado el mensaje.
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ))

# Registrar la hora y la confirmación de que se ha enviado el mensaje.
print(f" {datetime.datetime.now()}: [+] Sent {message}")

# Cerrar la conexión.
connection.close()
