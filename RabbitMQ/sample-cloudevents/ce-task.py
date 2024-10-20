#!/usr/bin/env python3
import pika
import sys
import json
from cloudevents.http import CloudEvent, to_structured

# RabbitMQへの接続情報
username = 'apl1'
password = 'password'
rmq_url  = 'rmq.default.k8s1.labo.local'
que_name = 'topic_sales'

# CloudEventsのヘッダーセット
attributes = {
    "type": "local.labo.k8s1.sales",
    "source": "/pgm002/inventory_reservation",
}

# アプリケーションのデータセット
data = {
    "product_code": "201401",
    "quantity": "1",
    "customer_code": "984091",
    "country": "Japan"
}


# RabbitMQ ブローカーへの接続
credentials = pika.PlainCredentials(username, password)
connection  = pika.BlockingConnection(
                 pika.ConnectionParameters(
                     host=rmq_url, credentials=credentials))
channel     = connection.channel()

# キュー宣言
channel.queue_declare(queue=que_name, durable=True)

# CloudEventのデータ作成（Structured)
event = CloudEvent(attributes, data)
http_headers, body = to_structured(event)

# メッセージ送信
channel.basic_publish(
    exchange='',
    routing_key=que_name,
    body=body,
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
    ))
print(" [x] Sent %r" % json.loads(body))
connection.close()
