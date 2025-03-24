import pika
import time
import random

# Configuração do servidor RabbitMQ
RABBITMQ_HOST = '172.21.29.200'
EXCHANGE_NAME = 'sensors'

def publish_temperature():
    """Publica valores de temperatura no RabbitMQ a cada 5 segundos."""
    
    # Conectar ao servidor RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    
    # Declarar um exchange do tipo 'topic'
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')

    while True:
        # Gerar um valor aleatório de temperatura entre 20 e 30°C
        temperature = round(random.uniform(20.0, 30.0), 2)
        message = f'Temperature: {temperature}°C'
        
        # Publicar a mensagem no RabbitMQ com a routing key 'sensor.temperature'
        channel.basic_publish(exchange=EXCHANGE_NAME, routing_key='sensor.temperature', body=message)
        
        print(f'[Sent] {message}')
        time.sleep(5)  # Esperar 5 segundos antes de enviar a próxima leitura

    connection.close()

# Executar a função se o script for chamado diretamente
if __name__ == '__main__':
    publish_temperature()