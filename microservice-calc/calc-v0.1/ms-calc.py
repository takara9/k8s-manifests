#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from flask import Flask
from flask_restful import Resource, Api, reqparse

# version
class ReplyVersion(Resource):
    def get(self):
        return {'version': 'calculater 0.1'}
    
# for POST
class Add(Resource):
    def post(self):
        args = parser.parse_args()
        ans = float(args['a']) + float(args['b'])
        return {'ans': ans }

if __name__ == '__main__':

    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Add, '/add')
    api.add_resource(ReplyVersion, '/ver')     

    parser = reqparse.RequestParser()
    parser.add_argument('a')
    parser.add_argument('b')

    bx_port = os.getenv("PORT")
    listen_port = int(bx_port if bx_port else 5000)
    app.run(host='0.0.0.0', port=listen_port, debug=True)
