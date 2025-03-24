import pika
import sys

# Configurações do RabbitMQ
RABBITMQ_HOST = 'localhost'
EXCHANGE_NAME = 'sensors'

def receive_data(topics):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')
    
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    
    for topic in topics:
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=topic)
    
    def callback(ch, method, properties, body):
        print(f'[Received] {body.decode()}')
    
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(f'[*] Waiting for messages on topics: {topics}')
    channel.start_consuming()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python receiver.py [sensor.temperature] [sensor.humidity]")
        sys.exit(1)
    
    topics = sys.argv[1:]
    receive_data(topics)
