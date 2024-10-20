#!/usr/bin/env python3

from cloudevents.http import CloudEvent, to_structured
import requests

# CloudEventの生成
# "id" は、省略することで自動生成
# "specversion" のデフォルトは"1.0"
attributes = {
    "type": "local.labo.k8s1.temp.gauge",
    "source": "/sensor/0001-01",
}
data = {"temperature": "20.3" }
event = CloudEvent(attributes, data)

# CloudEventのstructuredコンテントモードで、HTTPリクエストを生成
headers, body = to_structured(event)

# POSTで送信
requests.post("http://localhost:3000", data=body, headers=headers)
