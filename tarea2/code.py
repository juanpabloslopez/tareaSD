import random
import string
import pika

from confluent_kafka import Producer
import random

# Configuración de RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'admin'
RABBITMQ_PASSWORD = 'admin'
RABBITMQ_QUEUE = 'my_queue'


# Configuración de Kafka
bootstrap_servers = 'localhost:9092'
topic = 'kafkin'

# Generar palabra aleatoria
def generar_palabra_aleatoria():
    longitud = random.randint(5, 10)
    palabra = ''.join(random.choices(string.ascii_letters, k=longitud))
    return palabra

def delivery_report(err, msg):
    if err is not None:
        print(f'Error al enviar el mensaje: {err}')
    else:
        print(f'Mensaje enviado al topic {msg.topic()} - partición {msg.partition()} - offset {msg.offset()}')

# Enviar palabra aleatoria a RabbitMQ
def enviar_servers(palabra):
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=palabra)
    print(f"Palabra '{palabra}' enviada a RabbitMQ")
    connection.close()

    # Esto es para kafka
    p = Producer({'bootstrap.servers': bootstrap_servers})
    p.produce(topic, value=palabra.encode('utf-8'))
    p.flush()


# Generar palabra aleatoria y enviarla a RabbitMQ
def enviar_palabra_aleatoria():
    palabra = generar_palabra_aleatoria()
    enviar_servers(palabra)

# Ejecutar el envío de la palabra aleatoria
enviar_palabra_aleatoria()
