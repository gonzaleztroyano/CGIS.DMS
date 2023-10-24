#!/usr/bin/env python

# Importar el paquete pika, necesario para trabajar con el protocolo de RabbitMQ
import pika

# Conectarse a la instancia de RabbitMQ, corriendo en nuestro equipo (localhost)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Antes de enviar un mensaje tenemos que asegurarnos de que la cola exista.

# Creamos una cola:
channel.queue_declare(queue='prueba')

# Para enviar un mensaje con el contenido "¡Hola Mundo!" a la cola "prueba" ejecutamos:

for i in range(1,100001,1):
    cadena = "Hola Mundo! - " + str(i)
    channel.basic_publish(exchange='',
                          routing_key='prueba',
                          body=str(cadena))

# Para que aparezca la confirmación por pantalla:
print(" [x] Sent 'Hello World!'")

# Cerramos la conexión
connection.close()
