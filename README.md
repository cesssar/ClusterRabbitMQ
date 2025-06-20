# 🐇 Cluster RabbitMQ com HAProxy

Este repositório descreve os passos para subir um cluster RabbitMQ em Docker com 3 nós e balanceamento de carga via HAProxy.

---

## 🖼 Visão Geral

![Interface RabbitMQ](print.png)

---

## 🚀 Passos para Subir o Cluster

1. **Suba o Node 1**  
2. **Suba o Node 2**  
3. **Conecte o Node 2 ao cluster**:
   ```bash
   docker exec -it rabbit2 bash
   rabbitmqctl stop_app
   rabbitmqctl reset
   rabbitmqctl join_cluster rabbit@rabbit1
   rabbitmqctl start_app
   ```
4. **Suba o Node 3 e repita o processo de clusterização acima**.  
5. **Suba o HAProxy** para balancear as conexões.

---

Ajuste os arquivos `.env` e o arquivo `haproxy.cfg` com os IPs dos seus servidores Docker.  
Neste repositório foram utilizadas máquinas virtuais com Ubuntu 22.04 nos seguintes IPs:

- 192.168.122.200 - haproxy  
- 192.168.122.201 - nó RabbitMQ  
- 192.168.122.202 - nó RabbitMQ  
- 192.168.122.203 - nó RabbitMQ  

Sempre conectar-se ao IP do HAProxy para executar comandos no cluster e para acessar a página admin do mesmo.

---

## 🌐 Acesso à Interface Web

Acesse a página de administração do RabbitMQ pelo IP do proxy:  

[http://192.168.122.200:15672](http://192.168.122.200:15672)

> **Credenciais:** usuário e senha definidos no arquivo `.env`.

---

## 📈 Testes de Performance

### 📚 Referências

- [Tutorial de Teste de Carga no RabbitMQ (Medium)](https://phatdangx.medium.com/how-to-run-a-simple-performance-test-on-your-rabbitmq-cluster-13c0c5a870f4)  
- [RabbitMQ Perf Test no GitHub](https://github.com/rabbitmq/rabbitmq-perf-test)  
- [Vídeo explicativo no YouTube](https://www.youtube.com/watch?v=UIluPIy91no)  
- [Documentação oficial do PerfTest](https://perftest.rabbitmq.com/)

### 🔍 Comandos de Teste

#### ✅ Teste Geral
```bash
java -jar perf-test-latest.jar \
--uri amqp://mqadmin:Admsdvcein12a3XX@192.168.122.200:5672 \
-x 1 -y 2 -u "throughput-test-1" -a --id "test 1"
```

#### 👥 Teste com Múltiplos Produtores e Consumidores
```bash
java -jar perf-test-latest.jar \
--uri amqp://mqadmin:Admsdvcein12a3XX@192.168.122.200:5672 \
--queue-pattern 'perf-test-%d' --queue-pattern-from 1 --queue-pattern-to 10 \
--producers 50 --consumers 2
```

#### 🔥 Teste de Estresse
```bash
java -jar perf-test-latest.jar \
--uri amqp://mqadmin:Admsdvcein12a3XX@192.168.122.200:5672 \
--queue-pattern 'perf-test-%d' --queue-pattern-from 1 --queue-pattern-to 500 \
--producers 100 --consumers 1500 --metrics-format compact
```

---

## 📁 Estrutura do Projeto PHP

A pasta `php/` contém a implementação PHP para conexão e uso do RabbitMQ:

```
php/
├── enviar.php               # Exemplo para enviar mensagens
├── receber.php              # Exemplo para receber mensagens (consumir)
├── .env                     # Arquivo de configuração com dados de conexão
└── src/
    └── Services/
        └── RabbitMQService.php  # Classe PHP para conexão, envio e recebimento
```

---

## 🧰 Como Rodar o Exemplo PHP

### Requisitos

- PHP 8.4.8 (testado nesta versão)
- Composer (para gerenciar dependências)
- Extensão `php-amqplib/php-amqplib`
- Extensão `vlucas/phpdotenv`

### Instalação das dependências PHP

No diretório `php/`, execute:

```bash
composer install
```

### Configuração

Configure o arquivo `.env` na pasta `php/` com os dados do seu RabbitMQ:

```
RABBITMQ_HOST=192.168.122.200
RABBITMQ_PORT=5672
RABBITMQ_USER=mqadmin
RABBITMQ_PASSWORD=Admsdvcein12a3XX
```

### Executando os exemplos

- Para enviar uma mensagem:

```bash
php enviar.php
```

- Para consumir (receber) a primeira mensagem da fila:

```bash
php receber.php
```

---

## 📌 Observações

- A classe `RabbitMQService.php` implementa métodos para conectar, enviar e consumir mensagens, lendo configurações do `.env`.
- Ajuste os parâmetros do `.env` conforme seu ambiente.
- A comunicação via HAProxy garante balanceamento e alta disponibilidade.

---

## 🛠 Requisitos do Ambiente

- Docker & Docker Compose para o cluster RabbitMQ
- Java para testes de performance (PerfTest)
- PHP 8.4.8 com Composer para executar os exemplos PHP
