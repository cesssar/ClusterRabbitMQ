<?php

require_once __DIR__ . '/vendor/autoload.php';

use App\Services\RabbitMQService;

$rabbit = new RabbitMQService();
$rabbit->enviarMensagem('fila1', 'Mensagem de teste via classe!');
$rabbit->fecharConexao();
