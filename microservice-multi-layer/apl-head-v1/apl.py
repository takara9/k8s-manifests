#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import requests
import json
import uuid
import random
from flask import Flask
from flask_restful import Resource, Api, reqparse

host = os.getenv('DATASTORE_HOST')
port = os.getenv('DATASTORE_PORT')
url = 'http://' + str(host) + ':' + str(port) + '/'

# Version
class ReplyVersion(Resource):
    def get(self):
        return {'version': '1.0'}

# マイクロサービス本体
# HTTPメソッドで分岐
class RestApl(Resource):
    def get(self):
        id = random.randint(1000,1067)
        payload = {'id': id }
        json_str = requests.get(url, params=payload)
        json_dict = json.loads(json_str.text)
        return { 'id': id, 'phrase': json_dict['id'] }
    def delete(self):
        args = parser.parse_args()
        payload = {'id': args['id'] }
        json_str = requests.delete(url, params=payload)
        json_dict = json.loads(json_str.text)
        return{'ret': 'ok'}

#
# メイン
#
if __name__ == '__main__':

    # 初期化
    app = Flask(__name__)
    api = Api(app)

    # 機能設定
    api.add_resource(ReplyVersion, '/ver')     
    api.add_resource(RestApl, '/phrase')

    # パーサーの追加
    parser = reqparse.RequestParser()
    parser.add_argument('val')
    parser.add_argument('id')    
    
    # RESTサーバー開始
    bx_port = os.getenv("PORT")
    listen_port = int(bx_port if bx_port else 5000)
    app.run(host='0.0.0.0', port=listen_port, debug=True)
    






