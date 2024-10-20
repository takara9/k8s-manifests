#!/usr/bin/env python3
import pika


#credentials = pika.PlainCredentials('default_user_kGBQ_HdezlEvuiWJW8F', 'wKdW9zfH_56X5866mD18Hkml1fGt0hgQ')
credentials = pika.PlainCredentials('username', 'password')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='192.168.1.84', credentials=credentials))
    #pika.ConnectionParameters(host='172.16.1.44',port='31619', credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
