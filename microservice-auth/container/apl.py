#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import uuid
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import make_response
import python_jwt as jwt, jwcrypto.jwk as jwk, datetime
import json

jwks = { 'keys':[] }
data_store = {}
PRIVATE_KEY_FILE="/private-key.pem"
PUBLIC_KEY_FILE="/public-key.pem"


# 鍵ペアの生成
def create_keys():
    os.system("openssl genrsa -out " + PRIVATE_KEY_FILE + " 2048")
    os.system("openssl rsa -in " + PRIVATE_KEY_FILE + " -pubout -out " + PUBLIC_KEY_FILE)

    with open(PUBLIC_KEY_FILE, "rb") as pemfile:
        public_key = jwk.JWK.from_pem(pemfile.read()).export()
        #public_key = public_key.export()
        jwks['keys'].append(json.loads(public_key))


# バージョン応答
class ReplyVersion(Resource):
    def get(self):
        return {'version': '1.0'}

# ユーザー管理本体
class DataStore(Resource):
    
    # ユーザー登録
    def post(self):
        args = parser.parse_args()
        if len(args['user']) < 3 or len(args['password']) < 8:
            return {'error_msg': 'too short password or user' },403
        data_store[args['user'] ] = args['password']
        return {'ret': 'ok' },200

    # ユーザーの存在チュック（テスト用）
    def get(self):
        args = parser.parse_args()
        uid = args['user']
        if uid in data_store:
            return {'msg': 'exist'},200
        else:
            return {'error_msg': 'not exist' },404

    # パスワード変更
    def put(self):
        args = parser.parse_args()
        if len(args['password']) < 8:
            return {'error_msg': 'too short password' },403

        if args['user'] in data_store:
            data_store[ uid ] = args['password']
            return {'ret': 'ok' },200
        else:
            return {'error_msg': 'not exist' },404
    
    # ユーザーの削除
    def delete(self):
        args = parser.parse_args()        
        uid = args['user']
        if uid in data_store:
            del data_store[uid]
            return {'ret': 'ok' },200
        else:
            return {'error_msg': 'not exist' },404            

## ログイン処理
class Login(Resource):
    def get(self):
        args = parser.parse_args()

        # ユーザーIDとパスワードが一致していたら、
        # JWTとJWKのデータをユーザーIDをキーにして保存する
        uid = args['user']
        if uid in data_store:
            if args['password'] == data_store[uid]:
                token = generate_jwt_token(uid)
                resp = make_response({'msg': 'login ok' }, 200)
                resp.headers['Authorization'] = 'Bearer ' + token
                resp.set_cookie('Authorization', 'Bearer ' + token)
                return resp
            else:
                return {'msg': 'login faild'},401
        else:
            return {'error_msg': 'not exist' },404


## JWTトークンの生成
def generate_jwt_token(user):
    payload = {
        'iss':'ISSUER', 
        'sub': user, 
        'aud': user, 
        'role': 'user', 
        'permission': 'all' 
    }

    private_key = ""
    with open(PRIVATE_KEY_FILE, "rb") as pemfile:
        private_key = jwk.JWK.from_pem(pemfile.read())
        private_key = private_key.export()

    return jwt.generate_jwt(payload, jwk.JWK.from_json(private_key), 'RS256', datetime.timedelta(minutes=120))

## JWTのバリデーション
class Jwks(Resource):
    def get(self):
        return jwks
        
##
## MAIN
##
if __name__ == '__main__':

    # 公開鍵の生成
    create_keys()

    # Flaskの初期化
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(ReplyVersion, '/ver')     
    api.add_resource(DataStore, '/')
    api.add_resource(Login, '/login')
    api.add_resource(Jwks, '/jwks')    

    # 受け取るパラメータの設定
    parser = reqparse.RequestParser()
    parser.add_argument('user')
    parser.add_argument('password')
    parser.add_argument('Authorization', location='headers')

    # ポートの設定とイベントループ待ち
    bx_port = os.getenv("PORT")
    listen_port = int(bx_port if bx_port else 5000)
    app.run(host='0.0.0.0', port=listen_port, debug=True)


