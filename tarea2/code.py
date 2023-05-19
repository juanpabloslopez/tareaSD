import pika
from confluent_kafka import Producer
import json
import random
import time
import threading

# Configuración de RabbitMQ
rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
rabbitmq_channel = rabbitmq_connection.channel()
rabbitmq_channel.queue_declare(queue='rabbitmq_queue')

# Configuración de Kafka
kafka_conf = {'bootstrap.servers': 'localhost:9092'}
kafka_producer = Producer(kafka_conf)

# Lista de palabras aleatorias
words = ['apple', 'banana', 'orange', 'grape', 'pineapple', 'watermelon', 'mango', 'strawberry']

# Función para enviar mensajes de los dispositivos
def send_messages(device_id, delta_t):
    while True:
        word = random.choice(words)
        timestamp = int(time.time())

        # Envío a RabbitMQ
        rabbitmq_message = {
            'timestamp': timestamp,
            'word': word
        }
        rabbitmq_channel.basic_publish(exchange='', routing_key='rabbitmq_queue', body=json.dumps(rabbitmq_message))

        # Envío a Kafka
        kafka_message = {
            'timestamp': timestamp,
            'word': word
        }
        kafka_producer.produce(topic='kafka_topic', value=json.dumps(kafka_message))
        kafka_producer.flush()

        # Mostrar log en la consola
        print(f"Device {device_id} sending: {json.dumps(rabbitmq_message)}")

        time.sleep(delta_t)

# Simulación de múltiples dispositivos IoT
num_devices = 5  # Cantidad de dispositivos IoT
delta_t = 2  # Tiempo entre cada envío de mensaje (segundos)

# Crear y ejecutar los threads de los dispositivos
threads = []
for i in range(num_devices):
    thread = threading.Thread(target=send_messages, args=(i+1, delta_t))
    threads.append(thread)
    thread.start()

# Esperar a que todos los threads terminen
for thread in threads:
    thread.join()

# Cerrar conexiones
rabbitmq_connection.close()
