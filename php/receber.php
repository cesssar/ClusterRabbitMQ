<?php

require_once __DIR__ . '/vendor/autoload.php';

use App\Services\RabbitMQService;

$rabbit = new RabbitMQService();

// Declara o nome da fila
$fila = 'fila1';

// Acesso direto à conexão e canal
$reflection = new ReflectionClass($rabbit);
$channelProp = $reflection->getProperty('channel');
$channelProp->setAccessible(true);
$channel = $channelProp->getValue($rabbit);

// Garante que a fila existe
$channel->queue_declare($fila, false, false, false, false);

// Pega a primeira mensagem da fila (se houver)
$msg = $channel->basic_get($fila);

if ($msg) {
    echo "Mensagem recebida: {$msg->body}\n";
    // Confirma que a mensagem foi processada (se auto-ack = false)
    $channel->basic_ack($msg->delivery_info['delivery_tag']);
} else {
    echo "Nenhuma mensagem na fila '{$fila}'.\n";
}

$rabbit->fecharConexao();
