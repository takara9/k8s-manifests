#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import uuid
from flask import Flask
from flask_restful import Resource, Api, reqparse

data_store = {}

# バージョン応答
class ReplyVersion(Resource):
    def get(self):
        return {'version': '1.0'}

# データストア本体
class DataStore(Resource):
    # POST リソースの作成
    def post(self):
        args = parser.parse_args()
        id = args['id']
        data_store[ id ] = args['val']
        return {'ret': 'ok' }                    

    # GET リソースの取得
    def get(self):
        args = parser.parse_args()
        id = args['id']
        if id in data_store:
            return {'id': data_store[id] }
        else:
            return {'ret': 'not exist' }            

    # PUT リソースの更新（全体を置き換え）
    def put(self):
        args = parser.parse_args()
        id = args['id']
        if id in data_store:
            data_store[ id ] = args['val']
            return {'ret': 'ok' }
        else:
            return {'id': 'error' }
    
    # DELETE リソースの削除
    def delete(self):
        args = parser.parse_args()        
        id = args['id']
        if id in data_store:
            del data_store[args['id']]
            return {'ret': 'ok' }
        else:
            return {'ret': 'error' }
    
## MAIN
if __name__ == '__main__':

    app = Flask(__name__)
    api = Api(app)
    api.add_resource(ReplyVersion, '/ver')     
    api.add_resource(DataStore, '/')
    
    parser = reqparse.RequestParser()
    parser.add_argument('val')
    parser.add_argument('id')    

    bx_port = os.getenv("PORT")
    listen_port = int(bx_port if bx_port else 5000)
    app.run(host='0.0.0.0', port=listen_port, debug=True)


