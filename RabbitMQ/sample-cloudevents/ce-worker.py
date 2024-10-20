#!/usr/bin/env python3
import pika
import time
import json

# RabbitMQへの接続情報
username = 'apl1'
password = 'password'
rmq_url  = 'rmq.default.k8s1.labo.local'
que_name = 'topic_sales'

# メッセージ受信時のコールバック処理
def callback(ch, method, properties, body):
    body = json.loads(body.decode())
    print(json.dumps(body,indent=4))
    #time.sleep(1)
    # 受信応答
    ch.basic_ack(delivery_tag=method.delivery_tag)
    ##
    ## 業務処理をココに書く
    ##
    return
    
    
# RabbitMQ ブローカーへの接続
credentials = pika.PlainCredentials(username, password)
connection  = pika.BlockingConnection(
                 pika.ConnectionParameters(
                     host=rmq_url, credentials=credentials))
channel     = connection.channel()

# キュー宣言
channel.queue_declare(queue=que_name, durable=True)

# メッセージの受信ループ
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=que_name, on_message_callback=callback)
channel.start_consuming()
