# Istioテスト用のマルチレイヤなマイクロサービス

## Version 1.0

~~~
cd container
docker build -t maho/oauth-server:0.1 .

docker run -it --rm maho/oauth-server:0.1 bash

docker run -it -p 5000:5000 --rm maho/oauth-server:0.1
docker run -it --name auth-server -p 5000:5000 maho/oauth-server:0.1
docker run -d --name auth-server -p 5000:5000 maho/oauth-server:0.1

docker login
docker push maho/oauth-server:0.1
~~~


ローカル環境でテスト時

~~~
curl -i --header 'Content-Type: application/json' -d '{"user":"tkr","password":"testtest"}' -X POST http://localhost:5000/
curl -i --header 'Content-Type: application/json' -d '{"user":"tkr","password":"testtest"}' -X GET http://localhost:5000/login
curl -X GET http://localhost:5000/jwks
~~~


Kubernetes環境でのテスト時

~~~
kubectl apply -f auth-server.yaml
kubectl run -it mypod --image=maho/my-ubuntu:0.1 -- bash

curl -i --header 'Content-Type: application/json' -d '{"user":"takara","password":"testtest"}' -X POST http://auth-server:8000/
curl -i --header 'Content-Type: application/json' -d '{"user":"takara","password":"testtest"}' -X GET http://auth-server:8000/login
curl -X GET http://auth-server:8000/jwks
~~~



