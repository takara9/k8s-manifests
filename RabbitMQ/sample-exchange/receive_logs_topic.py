#!/usr/bin/env python3
import pika, sys, os

username = 'apl1'
password = 'password'
rmq_url  = 'rmq.default.k8s1.labo.local'
ex_name  = 'topic_logs'

# メッセージ受信時の処理
def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body.decode()))

# メイン    
def main():
    # RabbitMQブローカーへの接続
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rmq_url, credentials=credentials))    
    channel = connection.channel()

    # エクスチェンジとキュー
    channel.exchange_declare(exchange=ex_name, exchange_type='topic')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # バインディングキー
    binding_keys = sys.argv[1:]
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
        sys.exit(1)

    for binding_key in binding_keys:
        channel.queue_bind(
            exchange=ex_name, queue=queue_name, routing_key=binding_key)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
