import random
import string
import pika

# Configuración de RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'admin'
RABBITMQ_PASSWORD = 'admin'
RABBITMQ_QUEUE = 'my_queue'

# Generar palabra aleatoria
def generar_palabra_aleatoria():
    longitud = random.randint(5, 10)
    palabra = ''.join(random.choices(string.ascii_letters, k=longitud))
    return palabra

# Enviar palabra aleatoria a RabbitMQ
def enviar_rabbitmq(palabra):
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=palabra)
    print(f"Palabra '{palabra}' enviada a RabbitMQ")
    connection.close()

# Generar palabra aleatoria y enviarla a RabbitMQ
def enviar_palabra_aleatoria():
    palabra = generar_palabra_aleatoria()
    enviar_rabbitmq(palabra)

# Ejecutar el envío de la palabra aleatoria
enviar_palabra_aleatoria()
