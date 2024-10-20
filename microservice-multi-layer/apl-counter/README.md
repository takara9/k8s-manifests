# Istioテスト用のマルチレイヤなマイクロサービス

## Version 1.0

~~~
$ docker build -t maho/ml-counter:1.0 .
$ docker run -it -p 5000:5000 maho/ml-counter:1.0
$ docker login
$ docker push maho/ml-counter:1.0
~~~
