# Istioテスト用のマルチレイヤなマイクロサービス

## Version 1.0

~~~
$ cd apl-v1

# Build
$ docker build -t maho/simple:1.0 .

# Local test
$ docker run -it -p 5000:5000 maho/simple:1.0

# Push
$ docker login
$ docker push maho/simple:1.0
~~~
