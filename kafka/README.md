# Kafka

## 専用の名前空間を作成

~~~
kubectl create ns kafka
kubectl config set-context kafka --namespace=kafka --cluster=kubernetes --user=admin
kubectl config use-context kafka
kubectl config get-contexts
~~~

## KafkaとオペレーターStrimziのダウンロード

~~~
curl -OL https://archive.apache.org/dist/kafka/3.0.1/kafka_2.13-3.0.1.tgz
curl -OL https://github.com/strimzi/strimzi-kafka-operator/releases/download/0.27.1/strimzi-0.27.1.tar.gz
~~~


## ハイパフォーマンス Kafkaクラスタの作成

各ノードでローカルディスク/data1と/zookeeperがマウントされていること。

~~~
cd kafka-hs
kubectl apply -f kafka-operator.yaml
kubectl apply -f local-node-1.yaml
kubectl apply -f local-node-2.yaml
kubectl apply -f local-node-3.yaml
kubectl apply -f kafka-4.yaml
~~~

## ダイナミックプロビジョニングのストレージを利用するKafkaクラスタ

~~~
cd kafka-hs
kubectl apply -f kafka-operator.yaml
kubectl apply -f kafka-std.yaml
~~~


## 専用の監視画面

次のコマンド実行でKafka専用の名前空間kafkaにGrafana, Prometheusが起動する。
このプロメテウスなどは、オペレーターによって起動するため、K8sクラスタで
prometheus-operator が実行されていなければならない。

~~~
kubectl -f prometheus-podmonitor/
~~~

Kubernetesクラスタのメトリックス監視用のプロメテウスを起動することで、
名前空間 monitoringにオペレーターが稼働する。これを利用することになる。

~~~
git clone -b release-0.10 https://github.com/prometheus-operator/kube-prometheus
cd kube-prometheus/
kubectl apply --server-side -f manifests/setup
kubectl apply -f manifests
~~~


Web管理画面にアクセスするには、kubectl port-fowardを利用する

K8sクラスタ用のプロメテウスとグラファナ用

~~~
kubectl -n monitoring port-forward svc/prometheus-k8s 9090
kubectl -n monitoring port-forward svc/grafana 3000
~~~

Kafka専用のプロメテウスとグラファナ用

~~~
kubectl -n kafka port-forward svc/grafana 3002:3000
kubectl -n kafka monitoring port-forward svc/prometheus-k8s 9092:9090
~~~



## アクセステスト

コンテナを使ったトピックスへの書込みと読取り

~~~
kubectl -n kafka run kafka-producer -ti --image=quay.io/strimzi/kafka:0.27.1-kafka-3.0.0 --rm=true --restart=Never -- bin/kafka-console-producer.sh --broker-list my-cluster-kafka-bootstrap:9092 --topic my-topic
~~~

~~~
kubectl -n kafka run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.27.1-kafka-3.0.0 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic --from-beginning
~~~



kafkaのテスト用コマンドを使ったの書込みと読取り

先にダウンロードしたkafkaのtarファイルを展開して、シェルからJavaを実行する。

~~~
bin/kafka-console-producer.sh --broker-list 172.16.2.41:32000,172.16.2.42:32001,172.16.2.43:32002 --topic my-topic
~~~

~~~
bin/kafka-console-consumer.sh --bootstrap-server 172.16.2.41:32100 --topic my-topic --from-beginning
~~~

