import pika
import json
import random
import time

"""
O SENDER SÓ PRECISA TER INSTALADO O PIKA E AJUSTAR O IP DO PC RECEIVER

Conecta-se ao RabbitMQ do computador Receiver.
Simula um sensor de temperatura e envia valores aleatórios a cada 5 segundos.
Publica os dados no tópico "TemperaturaPlanta".
"""

# Configurar a conexão com o RabbitMQ do computador Receiver
rabbitmq_host = "192.168.1.220" #ip do pc receiver
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

# Enviar dados periodicamente
while True:
    temperatura = round(random.uniform(20, 35), 2)  # Simula temperatura entre 20°C e 35°C
    mensagem = {"sensor": "PlantaTeste", "temperatura": temperatura}

    # Converter a mensagem para JSON
    mensagem_json = json.dumps(mensagem)

    # Publicar a mensagem no tópico 'TemperaturaPlanta'
    routing_key = "TemperaturaPlanta"
    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=mensagem_json)

    print(f"📤 Enviado: {mensagem_json}")

    time.sleep(5)  # Envia uma temperatura a cada 5 segundos
