#!/usr/bin/env python3
import pika, sys, os

def main():
    
    #credentials = pika.PlainCredentials('default_user_kGBQ_HdezlEvuiWJW8F', 'wKdW9zfH_56X5866mD18Hkml1fGt0hgQ')
    credentials = pika.PlainCredentials('username', 'password')    
    connection = pika.BlockingConnection(
        #pika.ConnectionParameters(host='192.168.1.84', credentials=credentials))
        pika.ConnectionParameters(host='172.16.1.43',port='31619', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
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
