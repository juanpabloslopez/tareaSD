import random
import string
import pika
from confluent_kafka import Producer
import threading

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

# Enviar palabra aleatoria a RabbitMQ
def enviar_a_rabbitmq(palabra, dispositivo):
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=f"[Dispositivo {dispositivo}] {palabra}")
    print(f"[Dispositivo {dispositivo}] Palabra '{palabra}' enviada a RabbitMQ")
    connection.close()

# Enviar palabra aleatoria a Kafka
def enviar_a_kafka(palabra, dispositivo):
    p = Producer({'bootstrap.servers': bootstrap_servers})
    p.produce(topic, value=f"[Dispositivo {dispositivo}] {palabra}".encode('utf-8'))
    p.flush()
    print(f"[Dispositivo {dispositivo}] Palabra '{palabra}' enviada a Kafka")

# Función para enviar palabra aleatoria a ambos servidores
def enviar_palabra_aleatoria(dispositivo):
    palabra = generar_palabra_aleatoria()
    enviar_a_rabbitmq(palabra, dispositivo)
    enviar_a_kafka(palabra, dispositivo)

# Crear hilos para simular dispositivos IoT
threads = []
num_threads = 5  # Número de dispositivos que deseas simular

for i in range(num_threads):
    t = threading.Thread(target=enviar_palabra_aleatoria, args=(i+1,))
    threads.append(t)
    t.start()

# Esperar a que todos los hilos terminen
for t in threads:
    t.join()

