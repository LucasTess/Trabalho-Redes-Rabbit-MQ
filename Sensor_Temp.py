import pika
import time
import random

# Configurações do RabbitMQ
RABBITMQ_HOST = '172.21.29.200'
EXCHANGE_NAME = 'sensors'

def publish_temperature():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')
    
    while True:
        temperature = round(random.uniform(20.0, 30.0), 2)
        message = f'Temperature: {temperature}°C'
        channel.basic_publish(exchange=EXCHANGE_NAME, routing_key='sensor.temperature', body=message)
        print(f'[Sent] {message}')
        time.sleep(5)
    
    connection.close()

if __name__ == "__main__":
    publish_temperature()
