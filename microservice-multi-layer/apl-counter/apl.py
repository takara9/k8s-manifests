#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# カウンタサービス
#
#  POST,GET
#    キーについてカウント
#    存在しなければ作成してカウント開始
#

import os
import requests
import json
import uuid
import random
from flask import Flask
from flask_restful import Resource, Api, reqparse

counter_data = {}

# Version
class ReplyVersion(Resource):
    def get(self):
        return {'version': '1.0'}

class RestApl(Resource):
    # カウント
    def post(self):
        args = parser.parse_args()
        key = args['id']
        print("KEY=",key)
        if key in counter_data:
            counter_data[key] += 1
        else:
            counter_data[key] = 1
        return {'counter': counter_data[key] }

    # 削除
    def delete(self):
        args = parser.parse_args()
        key = args['id']
        ret = "not exist"
        if key in counter_data:
            del counter_data[key]
            ret = "ok"
        return { 'ret' : ret }

        
#
# メイン
#
if __name__ == '__main__':

    # 初期化
    app = Flask(__name__)
    api = Api(app)

    # 機能設定
    api.add_resource(ReplyVersion, '/ver')     
    api.add_resource(RestApl, '/count')

    parser = reqparse.RequestParser()
    parser.add_argument('id')
    
    # RESTサーバー開始
    bx_port = os.getenv("PORT")
    listen_port = int(bx_port if bx_port else 5500)
    app.run(host='0.0.0.0', port=listen_port, debug=True)
    






