<?php

namespace App\Services;

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;
use Dotenv\Dotenv;

class RabbitMQService
{
    private $connection;
    private $channel;

    public function __construct()
    {
        $dotenv = Dotenv::createImmutable(__DIR__ . '/../');
        $dotenv->load();

        $host = $_ENV['RABBITMQ_HOST'];
        $port = $_ENV['RABBITMQ_PORT'];
        $user = $_ENV['RABBITMQ_USER'];
        $password = $_ENV['RABBITMQ_PASSWORD'];

        $this->connection = new AMQPStreamConnection($host, $port, $user, $password);
        $this->channel = $this->connection->channel();
    }

    public function enviarMensagem(string $fila, string $mensagem): void
    {
        $this->channel->queue_declare($fila, false, false, false, false);
        $msg = new AMQPMessage($mensagem);
        $this->channel->basic_publish($msg, '', $fila);

        echo "Mensagem enviada para a fila '{$fila}': {$mensagem}\n";
    }

    public function consumirFila(string $fila, callable $callback): void
    {
        $this->channel->queue_declare($fila, false, false, false, false);

        $this->channel->basic_consume($fila, '', false, true, false, false, function ($msg) use ($callback) {
            $callback($msg->body);
        });

        echo "Aguardando mensagens da fila '{$fila}'...\n";

        while ($this->channel->is_consuming()) {
            $this->channel->wait();
        }
    }

    public function fecharConexao(): void
    {
        $this->channel->close();
        $this->connection->close();
    }
}
