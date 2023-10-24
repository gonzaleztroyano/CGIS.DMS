import pika
import time
import datetime

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='prueba2', durable=True)
print(f'{datetime.datetime.now()}: [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):

    # Printar por pantalla el contenido del mensaje que ha recibido. TODAVÍA NO se ha marcado como entregado.
    print(f"{datetime.datetime.now()}: [-] Received {body.decode()}")

    # Dormirá el número de veces que el caracter "b" aparezca en la cadena.
    # Es un ejemplo algo "inútil", pero sirve como diferenciador de dificultad.
    time.sleep(body.count(b'a'))

    # Printar por pantalla que ya se ha realizado el trabajo, una vez ha pasado el tiempo "dormido" correspondiente.
    print(f"{datetime.datetime.now()}: [+] Done")

    # Por si falla, no decimos a RabbitMQ que marque como entregado el mensaje hasta que no lo hemos terminado
    # de procesar. De esta forma, si el 'worker' tuviera algún problema y fallara, RabbitMQ volvería a entregar
    # el mensaje/tarea a otro worker que sí estuviera disponible.
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Coger mensajes de uno en uno
channel.basic_qos(prefetch_count=1)

# Empezar a consumir la cola "prueba2"
channel.basic_consume(queue='prueba2', on_message_callback=callback)

channel.start_consuming()
