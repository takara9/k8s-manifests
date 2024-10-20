## バージョン0.1のビルドとレジストリへのプッシュ

~~~
$ cd calc-v0.1
# Build
$ docker build -t maho/calculator:0.1 .

# Local test
$ docker run -it -p 5000:5000 maho/calculator:0.1

# Push
$ docker login
$ docker push maho/calculator:0.1
~~~

## バージョン0.2のビルドとレジストリへのプッシュ

~~~
$ cd calc-v0.2
# Build
$ docker build -t maho/calculator:0.2 .

# Local test
$ docker run -it -p 5000:5000 maho/calculator:0.2

# Push
$ docker login
$ docker push maho/calculator:0.2
~~~



# How to use


## Geting version

~~~
$ curl http://localhost:5000/ver
{
    "version": "calculation 0.1"
}
~~~


## Do calculation

~~~
$ curl -X POST -H "Content-Type: application/json" -d '{"a":"3", "b":"5"}' localhost:5000/add
{
    "ans": 8.0
}
~~~

