#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import requests
import json
import uuid
import random
from flask import Flask
from flask_restful import Resource, Api, reqparse

host_ds = os.getenv('DATASTORE_HOST')
port_ds = os.getenv('DATASTORE_PORT')
url_ds  = 'http://' + str(host_ds) + ':' + str(port_ds) + '/'

host_ct = os.getenv('COUNTER_HOST')
port_ct = os.getenv('COUNTER_PORT')
url_ct  = 'http://' + str(host_ct) + ':' + str(port_ct) + '/count'

# Version
class ReplyVersion(Resource):
    def get(self):
        return {'version': '1.0'}

# HTTPメソッドで分岐する
class RestApl(Resource):
    # ランダムに取り出し
    def get(self):
        id = random.randint(1000,1067)
        payload = {'id': id }
        json_str = requests.get(url_ds, params=payload)
        json_dict = json.loads(json_str.text)
        json_str_ct = requests.post(url_ct, params=payload)
        json_dict_ct = json.loads(json_str_ct.text)
        return { 'id': id, 'phrase': json_dict['id'], 'count': json_dict_ct['counter'] }

    def delete(self):
        args = parser.parse_args()
        payload = {'id': args['id'] }
        json_str = requests.delete(url_ds, params=payload)
        json_dict = json.loads(json_str.text)
        print(json_str)
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
    






