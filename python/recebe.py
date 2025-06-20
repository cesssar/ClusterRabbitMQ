from src.rabbitmq_service import RabbitMQService

fila = input("Nome da fila: ")

rmq = RabbitMQService()
rmq.consume_message(fila)
