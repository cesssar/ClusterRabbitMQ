import pika
from pyrabbit.api import Client
from dotenv import load_dotenv
import os
from pathlib import Path

class RabbitMQService:
    def __init__(self):
        env_path = Path(__file__).resolve().parent.parent / ".env"
        load_dotenv(dotenv_path=env_path)
        self.host = os.getenv("RABBITMQ_HOST", "localhost")
        self.user = os.getenv("RABBITMQ_USER", "guest")
        self.password = os.getenv("RABBITMQ_PASSWORD", "guest")
        self.api = f'{self.host}:{os.getenv("RABBITMQ_API_PORT", "15672")}'

    def _connect(self):
        try:
            return pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    credentials=pika.PlainCredentials(self.user, self.password)
                )
            )
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Erro ao conectar ao RabbitMQ: {e}")
            return None
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao conectar ao RabbitMQ: {e}")
            return None

    def send_message(self, queue_name: str, message: str):
        conn = None
        try:
            conn = self._connect()
            if not conn:
                return

            channel = conn.channel()
            channel.queue_declare(queue=queue_name, durable=True) # durable=True para persistir a fila
            channel.basic_publish(exchange='', routing_key=queue_name, body=message,
                                  properties=pika.BasicProperties(delivery_mode=2)) # delivery_mode=2 para persistir a mensagem
            print(f"Mensagem enviada: '{message}' para a fila '{queue_name}'")
        except pika.exceptions.AMQPChannelError as e:
            print(f"Erro de canal AMQP ao enviar mensagem: {e}")
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Erro de conexão AMQP ao enviar mensagem: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao enviar mensagem: {e}")
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as e:
                    print(f"Erro ao fechar a conexão no send_message: {e}")

    def consume_message(self, queue_name: str) -> str | None:
        conn = None
        try:
            conn = self._connect()
            if not conn:
                return None

            channel = conn.channel()
            channel.queue_declare(queue=queue_name, durable=True)

            method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)

            if method_frame:
                print(f"Mensagem consumida: '{body.decode()}' da fila '{queue_name}'")
                return body.decode()
            else:
                print(f"Nenhuma mensagem na fila '{queue_name}'")
                return None
        except pika.exceptions.AMQPChannelError as e:
            print(f"Erro de canal AMQP ao consumir mensagem: {e}")
            return None
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Erro de conexão AMQP ao consumir mensagem: {e}")
            return None
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao consumir mensagem: {e}")
            return None
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as e:
                    print(f"Erro ao fechar a conexão no consume_message: {e}")

    def list_queues(self):
        try:
            client = Client(self.api, self.user, self.password)
            # Verifica se a conexão com a API de gerenciamento foi bem-sucedida
            if not client.is_alive():
                print(f"Erro: Não foi possível conectar à API de gerenciamento do RabbitMQ em {self.api}")
                return []
            return [q['name'] for q in client.get_queues()]
        except ConnectionRefusedError:
            print(f"Erro: Conexão recusada ao tentar acessar a API de gerenciamento do RabbitMQ em {self.api}. Verifique se o RabbitMQ está em execução e a porta da API está correta.")
            return []
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao listar as filas: {e}")
            return []