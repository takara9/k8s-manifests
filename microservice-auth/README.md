# oAuth2認証サーバーの開発

Istioの認証に対応する oAuth2サーバーを開発する。

* ユーザー登録と削除
* ログイン処理 認証してJWTトークンを返す
* JWKSデータを返す


JWTトークンは、HTTPヘッダーの"Authorization: Bearer ${TOKEN}"で返すので、
ブラウザでアクセスする場合は、JavaScript で Header をコピーして、
次の送信のヘッダーへコピーする。


## デプロイ

これで、簡易認証サーバーがクラスタ内で稼働する。

~~~
kubectl apply -f auth-server.yaml
~~~




## アクセステスト

~~~
$ kubectl run -it mypod --image=maho/my-ubuntu:0.1 -- bash
~~~

ユーザーIDとパスワードの登録

~~~
root@mypod:/# curl -i --header 'Content-Type: application/json' -d '{"user":"takara","password":"testtest"}' -X POST http://auth-server:8000/
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 20
Server: Werkzeug/1.0.1 Python/3.6.9
Date: Tue, 15 Dec 2020 06:14:27 GMT

{
    "ret": "ok"
}
~~~

ログインを投げることで、JWTトークンを生成して返してくれる。クッキーにもセットするので、これをJavaScriptでヘッダーにセットすると良い。

~~~
root@mypod:/# curl -i --header 'Content-Type: application/json' -d '{"user":"takara","password":"testtest"}' -X GET http://auth-server:8000/login
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 24
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ0YWthcmEiLCJleHAiOjE2MDgwMjAwNzUsImlhdCI6MTYwODAxMjg3NSwiaXNzIjoiSVNTVUVSIiwianRpIjoiSXA4ZkZzeFhJNUpBM3Y3QnI5Nk5wZyIsIm5iZiI6MTYwODAxMjg3NSwicGVybWlzc2lvbiI6ImFsbCIsInJvbGUiOiJ1c2VyIiwic3ViIjoidGFrYXJhIn0.RsvI0pg2i4PutiXzRhFYt-2SDG-g97B-nCscllXyqH9PM-r66db6AtL-drNIJsuOWr62aXf0BSlcFA1xcMAOoGn3e2TvgDOLxANJg_ciP9M4mE1vcCBcR1arLLLoJL3dXeQpZ15r-m3nLomAgTThwoFPBobWobwXmpoBhR1ptrQHZXsE2J9b5YzcKzlsrt6BTgo_D7wDIdQQOidXj1YWxI70bUkIw9FPvUvUiGi_ONOoHW9SoIY2g-Rqt_FGexfW70kaPIsdqXWP41JYf3LJvib65mPq4l7ngVAFwIQOhc3pVKE4cFKEDsGDxmrqMksRVrqPVVJKWQFrdrdkvA4NqA
Set-Cookie: Authorization="Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ0YWthcmEiLCJleHAiOjE2MDgwMjAwNzUsImlhdCI6MTYwODAxMjg3NSwiaXNzIjoiSVNTVUVSIiwianRpIjoiSXA4ZkZzeFhJNUpBM3Y3QnI5Nk5wZyIsIm5iZiI6MTYwODAxMjg3NSwicGVybWlzc2lvbiI6ImFsbCIsInJvbGUiOiJ1c2VyIiwic3ViIjoidGFrYXJhIn0.RsvI0pg2i4PutiXzRhFYt-2SDG-g97B-nCscllXyqH9PM-r66db6AtL-drNIJsuOWr62aXf0BSlcFA1xcMAOoGn3e2TvgDOLxANJg_ciP9M4mE1vcCBcR1arLLLoJL3dXeQpZ15r-m3nLomAgTThwoFPBobWobwXmpoBhR1ptrQHZXsE2J9b5YzcKzlsrt6BTgo_D7wDIdQQOidXj1YWxI70bUkIw9FPvUvUiGi_ONOoHW9SoIY2g-Rqt_FGexfW70kaPIsdqXWP41JYf3LJvib65mPq4l7ngVAFwIQOhc3pVKE4cFKEDsGDxmrqMksRVrqPVVJKWQFrdrdkvA4NqA"; Path=/
Server: Werkzeug/1.0.1 Python/3.6.9
Date: Tue, 15 Dec 2020 06:14:35 GMT

{
  "msg": "login ok"
}
~~~


JWKSトークンの取得方法は、簡易認証サーバーのアドレスにGETを送信することでJWTトークンの検証に必要なJSONデータを取得できる。

~~~
$ curl -X GET http://localhost:5000/jwks
{
    "keys": [
        {
            "e": "AQAB",
            "kid": "CCrLvqdGSOXG-CgVD4C12_IMvt62HpFCjTmbIzmqFw4",
            "kty": "RSA",
            "n": "tcr6jfVhLjhPZ2Kc-CaDyF9QjO_gsBNE5F3LYiqugkSwsJP2gGkpez0yAzd89OLt-LKyIETS3ERZ_bjssE7lNaMhh3e5dU-8QqDog2u6eulO49ffA0go2rlxssmygMVAj4wJqyenqm2qrDA4Wxy6u80BN-0nphDxpBVd6ILW5I0ldfrOiVGnrPAIxU5pN-8Dkcfa2xR_wJeATPzVKB4GuO9AKYggySTvpfytjmhLJmWbpiuOPPm3UXdIvZrSO3NBQxNFEl223_zFWUOi_umovQuGRbVCXtC_LLLBoQHHNLJgFgFnhtCaAHoX6kv6A48RuKoRE9NwP2I99MNuESRkvw"
        }
    ]
}
~~~




---

# 簡易認証サーバーの仕様

## ユーザー登録
POST / { user: "user1", password: "user1passwd" }

#### 応答 
* 200: 登録成功
* 406: 登録失敗

#### 処理
キャッシュにuserをキーとして、パスワードをハッシュとして保存する。

#### 失敗の条件
* キー項目 user, password が存在しない場合
* user が3文字未満の場合
* password が8文字未満の場合
* 文字数が20バイトを超える場合




## ユーザー削除
DELETE / { user: "user1" }

#### 応答 
* 200: 削除成功
* 406: 削除失敗

#### 処理
キー項目のキャッシュを削除する

#### 失敗の条件
* キー項目 user が存在しない



## ユーザーのログイン
POST /login { user: "user1", password: "user1passwd" }

#### 応答
* 200: ログイン成功
* 401: ログイン失敗

#### 処理
* userが存在して、パスワードのハッシュが一致した場合は、"Authorization: Bearer ${TOKEN}" を返す。
* トークンは、JWTトークンを生成して返す。
* トークンの有効期限は1時間とする

#### 失敗の条件
* userが登録されてない場合
* パスワードのハッシュが一致しない場合



## JWKSの取得
GET /jwks

#### 応答
* 200: 処理完了 JWKSフォーマットの文字列を返却


#### 処理
JWKSフォーマットの文字列を応答する。


-------

# 内部処理

## 起動時初期化処理

以下のコマンドを実行して、プライベートキー、パブリックキーを生成する。
* openssl genrsa -out private-key.pem 2048
* openssl rsa -in private-key.pem -pubout -out public-key.pem



## ログイン時の処理

ログインでユーザーとパスワードの認証に成功したら、次を実行する。
* JWTトークンを生成する
* トークン項目は適当に設定する
* Cookie のトークンをセットして応答する。
* JWKSはユーザーIDに対応して保存する。


## バリデーションの処理
* トークンに対応する JWKSを返却する。






-----
参考資料
* Where to Store your JWTs – Cookies vs HTML5 Web Storage, https://stormpath.com/blog/where-to-store-your-jwts-cookies-vs-html5-web-storage
* Token Based Authentication for Single Page Apps (SPAs), https://stormpath.com/blog/token-auth-spa
* Istio & JWT: Step by Step Guide for Micro-Services Authentication, https://medium.com/intelligentmachines/istio-jwt-step-by-step-guide-for-micro-services-authentication-690b170348fc
* https://github.com/fai555/Istio-and-JWT








