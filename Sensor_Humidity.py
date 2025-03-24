import pika
import time
import random

# Configurações do RabbitMQ
RABBITMQ_HOST = '172.21.29.200'
EXCHANGE_NAME = 'sensors'

def publish_humidity():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')
    
    while True:
        humidity = round(random.uniform(40.0, 60.0), 2)
        message = f'Humidity: {humidity}%'
        channel.basic_publish(exchange=EXCHANGE_NAME, routing_key='sensor.humidity', body=message)
        print(f'[Sent] {message}')
        time.sleep(5)
    
    connection.close()

if __name__ == "__main__":
    publish_humidity()
