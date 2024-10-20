# Istioテスト用のマルチレイヤなマイクロサービス

## Version 1.0

~~~
$ docker build -t maho/ml-load:1.0 .
$ docker run -it -p 5000:5000 -e DATASTORE_HOST=dstore -e DATASTORE_PORT=9080 maho/ml-load:1.0
$ docker login
$ docker push maho/ml-load:1.0
~~~
