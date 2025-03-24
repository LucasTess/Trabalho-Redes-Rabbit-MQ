import pika
import time
import random

# Configuração do servidor RabbitMQ
RABBITMQ_HOST = '172.21.29.200'
EXCHANGE_NAME = 'sensors'

def publish_humidity():
    """Publica valores de umidade no RabbitMQ a cada 5 segundos."""
    
    # Conectar ao servidor RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    
    # Declarar um exchange do tipo 'topic'
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')

    while True:
        # Gerar um valor aleatório de umidade entre 40% e 60%
        humidity = round(random.uniform(40.0, 60.0), 2)
        message = f'Humidity: {humidity}%'
        
        # Publicar a mensagem no RabbitMQ com a routing key 'sensor.humidity'
        channel.basic_publish(exchange=EXCHANGE_NAME, routing_key='sensor.humidity', body=message)
        
        print(f'[Sent] {message}')
        time.sleep(5)  # Esperar 5 segundos antes de enviar a próxima leitura

    connection.close()

# Executar a função se o script for chamado diretamente
if __name__ == '__main__':
    publish_humidity()
