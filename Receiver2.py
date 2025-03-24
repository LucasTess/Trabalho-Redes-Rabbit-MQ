import pika
import sys

# Configuração do servidor RabbitMQ
RABBITMQ_HOST = 'localhost'
EXCHANGE_NAME = 'sensors'

def receive_data(topics):
    """Escuta mensagens dos sensores com base nos tópicos fornecidos via terminal."""
    
    # Conectar ao servidor RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    
    # Declarar um exchange do tipo 'topic'
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')
    
    # Criar uma fila exclusiva para este Receiver
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    # Associar a fila aos tópicos desejados
    for topic in topics:
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=topic)
    
    print(f'[*] Esperando mensagens nos tópicos: {topics}')
    
    # Função callback para processar mensagens recebidas
    def callback(ch, method, properties, body):
        print(f'[Received] {body.decode()}')
    
    # Consumir mensagens da fila
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

# Verifica se o usuário forneceu os tópicos como argumento no terminal
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python receiver.py <topico1> <topico2> ...")
        sys.exit(1)

    # Lista de tópicos passados pelo terminal
    topics = sys.argv[1:]
    receive_data(topics)
