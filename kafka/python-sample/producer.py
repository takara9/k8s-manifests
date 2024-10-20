#!/usr/bin/env python3
import json
import time
from kafka import KafkaProducer

producer = KafkaProducer(
     bootstrap_servers='172.16.2.41:32000,172.16.2.42:32001,172.16.2.43:32002',
     value_serializer=lambda v: json.dumps(v).encode('utf-8')
     )

for id in range(10):
     import uuid     
     uuid = str(uuid.uuid4())
     producer.send('my-topic3', {'id': id, 'uuid': uuid})
     print(id,uuid)
     producer.flush()
     time.sleep(1)


