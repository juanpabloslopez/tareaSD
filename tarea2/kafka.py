from confluent_kafka import Producer
import random

bootstrap_servers = 'localhost:9092'
topic = 'mi-topic'

def delivery_report(err, msg):
    if err is not None:
        print(f'Error al enviar el mensaje: {err}')
    else:
        print(f'Mensaje enviado al topic {msg.topic()} - partición {msg.partition()} - offset {msg.offset()}')

def send_random_word():
    words = ['hello', 'world', 'example', 'kafka']
    random_word = random.choice(words)
    p = Producer({'bootstrap.servers': bootstrap_servers})

    p.produce(topic, value=random_word.encode('utf-8'), callback=delivery_report)
    p.flush()

if __name__ == '__main__':
    send_random_word()

