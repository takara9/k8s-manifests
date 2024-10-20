#!/usr/bin/env python3
from kafka import KafkaConsumer

consumer = KafkaConsumer('my-topic2',
                         bootstrap_servers='172.16.2.41:32100',
                         group_id='my-group')



for msg in consumer:
    print (msg)     
