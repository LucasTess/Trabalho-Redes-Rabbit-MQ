import pika
import json

"""
Conecta-se ao RabbitMQ local (Receiver roda o servidor).
Escuta o tópico "TemperaturaPlanta" e exibe as mensagens recebidas.
"""

# Configurar a conexão com o RabbitMQ
rabbitmq_host = "localhost"  # Como o Receiver roda o RabbitMQ, usamos 'localhost'
username = "trabalho_redes"
password = "redesdecomputadores_20242"

# Configuração da conexão
credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)

# Conectar ao RabbitMQ
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Criar a troca de mensagens do tipo 'topic'
exchange_name = "sensores"
channel.exchange_declare(exchange=exchange_name, exchange_type="topic")

# Criar a fila e associá-la ao tópico "TemperaturaPlanta"
queue_name = "fila_temperatura"
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key="TemperaturaPlanta")

# Callback que será chamado sempre que uma mensagem for recebida
def callback(ch, method, properties, body):
    mensagem = json.loads(body)
    print(f"📥 Recebido: Sensor={mensagem['sensor']}, Temperatura={mensagem['temperatura']}°C")

# Consumir mensagens
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print("📡 Aguardando mensagens...")
channel.start_consuming()
