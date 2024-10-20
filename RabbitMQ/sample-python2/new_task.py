#!/usr/bin/env python3

import pika
import sys

credentials = pika.PlainCredentials('apl1', 'pilot00pilot')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='192.168.1.84', credentials=credentials))    
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
    ))
print(" [x] Sent %r" % message)
connection.close()
