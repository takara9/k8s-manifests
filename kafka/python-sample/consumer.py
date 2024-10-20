#!/usr/bin/env python3
from kafka import KafkaConsumer

consumer = KafkaConsumer('my-topic3',
                         bootstrap_servers='172.16.2.41:32100',
                         group_id='my-group',
                         auto_offset_reset='earliest', enable_auto_commit=False)


for msg in consumer:
    print (msg)     
