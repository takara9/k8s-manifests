# Istioテスト用のマルチレイヤなマイクロサービス

## Version 2.0

~~~
$ docker build -t maho/ml-head:2.0 .
$ docker run -it -p 5000:5000 --link dstore -e DATASTORE_HOST=dstore -e DATASTORE_PORT=9080 \
  --link counter -e COUNTER_HOST=dstore -e COUNTER_PORT=9080 maho/ml-head:2.0
$ docker login
$ docker push maho/ml-head:2.0
~~~
