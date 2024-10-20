# Istio と OAuth2 JWT認証

Istioと簡易認証プロバイダーを利用したシングルサインオン環境

この検証を実施するには https://github.com/takara9/webapl-8 のOAuthサーバーをデプロイして
DNSを登録して、アクセスできる状態でなければならない。

この設定を入れるとIstio イングレスゲートウェイ全体に認証が必要となるので、IsitoイングレスGWを
共有するアプリケーションがあれば影響を受けるため注意が必要だ。



## デプロイ

アプリとIstioの一式をデプロイ

~~~
$ kubectl apply -k .
~~~


## DNSサーバー設定

IstioイングレスGWのアドレスを求める

~~~
$ kubectl get svc -n istio-system  -l istio=ingressgateway
NAME                   TYPE           CLUSTER-IP   EXTERNAL-IP   PORT(S)                                                      AGE
istio-ingressgateway   LoadBalancer   10.32.0.88   10.0.3.42     15021:32217/TCP,80:32342/TCP,443:31300/TCP,15443:31875/TCP   3d23h
~~~


CoreDNSに設定する。

~~~labo.db 
labo.local.	3600 IN SOA ns1.labo.local. root.labo.local. (
				20         ; serial
				7200       ; refresh (4 hours)
				3600       ; retry (1 hour)
				604800     ; expire (1 week)
				1800       ; minimum (30 min)
				)

; Infra Servers
ns1             3600 IN  A     192.168.1.241 ; This server CoreDNS
ca              3600 IN  CNAME ns1           ; Local CA

;; CICD Servers
harbor          3600 IN  A     10.0.0.221    ; Container Image Registry
gitlab          3600 IN  A     10.0.0.222    ; Code Repository
jenkins         3600 IN  A     10.0.0.223    ; CICD Server

; Edge Nodes
raspi07         3600 IN  A     192.168.1.241 ; Edge Node 1
raspi08         3600 IN  A     192.168.1.242 ; Edge Node 2

; Istio Ingress Gateway
igw3            3600 IN  A     10.0.3.42     ; Istio Ingress GW <--- これが本体
svc1            3600 IN  CNAME igw3          ; Istio apl #1
svc2            3600 IN  CNAME igw3          ; Istio apl #2
svc3            3600 IN  CNAME igw3          ; Istio apl #2  <--- 追加

; OAuth Server
oauth           3600 IN  A     10.0.2.83     ; <--- 認証サーバー
~~~





## アクセステスト

認証トークンJWTが無い状態でのアクセスは、当然、アクセスできない。

~~~
$ curl svc3.labo.local;echo
RBAC: access denied
~~~


## OAuthサーバーへユーザー登録

~~~
$ curl -i --header 'Content-Type: application/json' -d '{"user":"takara","password":"testtest"}' -X POST http://oauth.labo.local/
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 20
Server: Werkzeug/1.0.1 Python/3.6.9
Date: Mon, 01 Feb 2021 12:04:41 GMT

{
    "ret": "ok"
}
~~~



## OAuthサーバーにログインしてトークンを取得

~~~
$ curl -i --header 'Content-Type: application/json' -d '{"user":"takara","password":"testtest"}' -X GET http://oauth.labo.local/login
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 24
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ0YWthcmEiLCJleHAiOjE2MTIxODgyODYsImlhdCI6MTYxMjE4MTA4NiwiaXNzIjoiSVNTVUVSIiwianRpIjoibGJvRmh3aUhYeEtHZDVQcDhQMTJtdyIsIm5iZiI6MTYxMjE4MTA4NiwicGVybWlzc2lvbiI6ImFsbCIsInJvbGUiOiJ1c2VyIiwic3ViIjoidGFrYXJhIn0.eXqXYobjMoqtxW8QxmK8Ap9MtEmHiOzeSc2ldt_LlhbVUO4v5feYgmGgaSiwh2ORwTP4fRlRMlUlLOYQdjZjHbs0vDYT4wq6XRPde402Ekqk5aQk6CvobCHUWwhvHasTg2cVjTjxkJNMEzHAg3tuoPjjYvnDqbuHpsyggejg6K7HYiDvV3L6P8U5tT3eHieMZXsEjoBqqSIFMICuN2f8FcM46hBcnc6x7_uC0h3bUWASOO_TMdhwZeRnca-w8XEBbL8fTbY-n6LQyr44TZKke4--oOFRF8Vx5LTsBCg91SPgLQK7Qx4soiZYAn3R-fs7BQjNFIgWCDxuMrISBTLQYg
Set-Cookie: Authorization="Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ0YWthcmEiLCJleHAiOjE2MTIxODgyODYsImlhdCI6MTYxMjE4MTA4NiwiaXNzIjoiSVNTVUVSIiwianRpIjoibGJvRmh3aUhYeEtHZDVQcDhQMTJtdyIsIm5iZiI6MTYxMjE4MTA4NiwicGVybWlzc2lvbiI6ImFsbCIsInJvbGUiOiJ1c2VyIiwic3ViIjoidGFrYXJhIn0.eXqXYobjMoqtxW8QxmK8Ap9MtEmHiOzeSc2ldt_LlhbVUO4v5feYgmGgaSiwh2ORwTP4fRlRMlUlLOYQdjZjHbs0vDYT4wq6XRPde402Ekqk5aQk6CvobCHUWwhvHasTg2cVjTjxkJNMEzHAg3tuoPjjYvnDqbuHpsyggejg6K7HYiDvV3L6P8U5tT3eHieMZXsEjoBqqSIFMICuN2f8FcM46hBcnc6x7_uC0h3bUWASOO_TMdhwZeRnca-w8XEBbL8fTbY-n6LQyr44TZKke4--oOFRF8Vx5LTsBCg91SPgLQK7Qx4soiZYAn3R-fs7BQjNFIgWCDxuMrISBTLQYg"; Path=/
Server: Werkzeug/1.0.1 Python/3.6.9
Date: Mon, 01 Feb 2021 12:04:46 GMT

{
  "msg": "login ok"
}
~~~



## TOKENをリクエストのヘッダーにセットしてアクセス

~~~
# トークンを環境変数にセット
$ export TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ0YWthcmEiLCJleHAiOjE2MTIxODgyODYsImlhdCI6MTYxMjE4MTA4NiwiaXNzIjoiSVNTVUVSIiwianRpIjoibGJvRmh3aUhYeEtHZDVQcDhQMTJtdyIsIm5iZiI6MTYxMjE4MTA4NiwicGVybWlzc2lvbiI6ImFsbCIsInJvbGUiOiJ1c2VyIiwic3ViIjoidGFrYXJhIn0.eXqXYobjMoqtxW8QxmK8Ap9MtEmHiOzeSc2ldt_LlhbVUO4v5feYgmGgaSiwh2ORwTP4fRlRMlUlLOYQdjZjHbs0vDYT4wq6XRPde402Ekqk5aQk6CvobCHUWwhvHasTg2cVjTjxkJNMEzHAg3tuoPjjYvnDqbuHpsyggejg6K7HYiDvV3L6P8U5tT3eHieMZXsEjoBqqSIFMICuN2f8FcM46hBcnc6x7_uC0h3bUWASOO_TMdhwZeRnca-w8XEBbL8fTbY-n6LQyr44TZKke4--oOFRF8Vx5LTsBCg91SPgLQK7Qx4soiZYAn3R-fs7BQjNFIgWCDxuMrISBTLQYg



# トークンをヘッダーにセットしてアクセス
$ curl --header "Authorization: Bearer $TOKEN" -X GET http://svc3.labo.local
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>httpbin.org</title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700|Source+Code+Pro:300,600|Titillium+Web:400,600,700"
<以下省略>
~~~




参考資料
[1] JWTRule, https://istio.io/latest/docs/reference/config/security/jwt/#JWTRule
[2] Authorization with JWT, https://istio.io/latest/docs/tasks/security/authorization/authz-jwt/
[3] Authorization on Ingress Gateway, https://istio.io/latest/docs/tasks/security/authorization/authz-ingress/


