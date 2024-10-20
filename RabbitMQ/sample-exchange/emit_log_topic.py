#!/usr/bin/env python3
import pika
import sys

username = 'apl1'
password = 'password'
rmq_url  = 'rmq.default.k8s1.labo.local'
ex_name  = 'topic_logs'

credentials = pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rmq_url, credentials=credentials))    
channel = connection.channel()

# エクスチェンジの宣言
channel.exchange_declare(exchange=ex_name, exchange_type='topic')

# ルーティングキーの設定
routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'

# メッセージ作成
message = ' '.join(sys.argv[2:]) or 'Hello World!'

# メッセージ送信
channel.basic_publish(
    exchange=ex_name,
    routing_key=routing_key,
    body=message)
print(" [x] Sent %r:%r" % (routing_key, message))

connection.close()


