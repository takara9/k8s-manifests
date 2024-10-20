#!/usr/bin/env python3

from cloudevents.http import CloudEvent, to_binary
import requests

# Create a CloudEvent
# - The CloudEvent "id" is generated if omitted. "specversion" defaults to "1.0".
attributes = {
    "type": "com.example.sampletype1",
    "source": "https://example.com/event-producer",
}
data = {"message": "Hello World!"}
event = CloudEvent(attributes, data)

# Creates the HTTP request representation of the CloudEvent in binary content mode
headers, body = to_binary(event)

# POST
requests.post("http://localhost:3000", data=body, headers=headers)
