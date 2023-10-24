#!/usr/bin/env python

# Importar el paquete pika, necesario para trabajar con el protocolo de RabbitMQ
import pika
import time

# Conectarse a la instancia de RabbitMQ, corriendo en nuestro equipo (localhost)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


# Definimos la función que se ejecutará con cada mensaje:
def callback(ch, method, properties, body):
    print("Iniciando procesamiento")
    time.sleep(0.5)
    print(f" [x] Received {body}")


# Indicamos que queremos CONSUMIR la cola "prueba",
# y para cada mensaje se ejecutará la función "callback",
# definida anteriormente.
channel.basic_consume(queue='prueba',
                      auto_ack=True,
                      on_message_callback=callback)

# Printar mensaje informativo por pantalla.
print(' [*] Waiting for messages. To exit press CTRL+C')

# Empezar a consumir la cola.
channel.start_consuming()
