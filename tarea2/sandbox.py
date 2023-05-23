import random
import string
import pika
from confluent_kafka import Producer
import json
import threading
import time

# Configuración de RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'admin'
RABBITMQ_PASSWORD = 'admin'
RABBITMQ_QUEUE = 'my_queue'

# Configuración de Kafka
bootstrap_servers = 'localhost:9092'
topic = 'kafkin'

# Generar palabra aleatoria en formato JSON con timestamp
def generar_palabra_aleatoria(device_id):
    longitud = random.randint(5, 10)
    palabra = ''.join(random.choices(string.ascii_letters, k=longitud))
    data = {
        'timestamp': int(time.time()),
        'value': {
            'data': palabra
        },
        'device_id': device_id
    }
    return json.dumps(data)

# Enviar palabra aleatoria a los servidores en formato JSON
def enviar_servers(palabra, device_id):
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=palabra)
    print(f"Dispositivo {device_id} - Palabra '{palabra}' enviada a RabbitMQ")
    connection.close()

    # Esto es para Kafka
    p = Producer({'bootstrap.servers': bootstrap_servers})

    def delivery_report(err, msg):
        if err is not None:
            print('Error al enviar mensaje a Kafka:', err)
        else:
            print(f"Dispositivo {device_id} - Mensaje enviado a Kafka: {msg.topic()}[{msg.partition()}]")

    p.produce(topic, value=palabra.encode('utf-8'), callback=delivery_report)
    p.flush()

# Función para simular un dispositivo IoT
def dispositivo_iot(device_id):
    while True:
        palabra = generar_palabra_aleatoria(device_id)
        enviar_servers(palabra, device_id)
        time.sleep(random.randint(1, 5))  # Esperar un tiempo aleatorio antes de enviar el siguiente mensaje

# Crear hilos para simular dispositivos IoT
num_dispositivos = 5  # Número de dispositivos a simular

threads = []

for i in range(num_dispositivos):
    t = threading.Thread(target=dispositivo_iot, args=(i,))
    threads.append(t)
    t.start()

# Esperar a que todos los hilos terminen
for t in threads:
    t.join()

