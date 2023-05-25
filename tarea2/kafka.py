from aiokafka import AIOKafkaConsumer
import asyncio

# Configuración de Kafka
bootstrap_servers = 'localhost:9092'
group_id = 'my_consumer_group'
topics = ['kafkin']

async def consume():
    consumer = AIOKafkaConsumer(
        'my_topic', 'kafkin',
        bootstrap_servers='localhost:9092',
        group_id="my-group")
    await consumer.start()
    try:
        
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        await consumer.stop()

asyncio.run(consume())
