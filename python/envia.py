from src.rabbitmq_service import RabbitMQService

rmq = RabbitMQService()

print()
fila = input("Nome da fila: ")
msg = input("Mensagem: ")

rmq.send_message(fila, msg)
