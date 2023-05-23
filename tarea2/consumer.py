import pika
from confluent_kafka import Consumer, KafkaException


# Configuración de RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'admin'
RABBITMQ_PASSWORD = 'admin'
RABBITMQ_QUEUE = 'my_queue'

# Configuración de Kafka
bootstrap_servers = 'localhost:9092'
group_id = 'my_consumer_group'
topics = ['kafkin']


# Consumidor de RabbitMQ
def consumir_rabbitmq():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)

    def callback(ch, method, properties, body):
        print(f"Mensaje recibido desde RabbitMQ: {body.decode('utf-8')}")

    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


# Consumidor de Kafka
def consumir_kafka():
    conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }
    c = Consumer(conf)

    def print_assignment(consumer, partitions):
        print('Particiones asignadas:', partitions)

    # Asignar función de callback para mostrar las particiones asignadas
    c.subscribe(topics, on_assign=print_assignment)

    try:
        while True:
            msg = c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    continue
                else:
                    print('Error al recibir mensaje de Kafka:', msg.error())
                    break

            print(f"Mensaje recibido desde Kafka: {msg.value().decode('utf-8')}")
            c.commit()

    except KeyboardInterrupt:
        pass

    finally:
        c.close()


# Consumir mensajes de RabbitMQ y Kafka en el mismo proceso
consumir_rabbitmq()
consumir_kafka()

