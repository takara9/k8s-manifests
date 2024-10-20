#!/usr/bin/env python3
import json
from flask import Flask, request
from cloudevents.http import from_http
app = Flask(__name__)

# FLASKでエンドポイント生成 http://localhost:/3000/
@app.route("/", methods=["POST"])
def home():
    # CloudEventで受信メッセージを処理
    event = from_http(request.headers, request.get_data())
    j = json.loads(request.get_data())
    print(json.dumps(j,indent=4))
    return "", 204

if __name__ == "__main__":
    app.run(port=3000)
