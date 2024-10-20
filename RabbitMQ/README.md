# RabbitMQ


## 専用名前空間の作成

~~~
kubectl create ns rabbitmq
kubectl config set-context rmq --namespace=rabbitmq --cluster=kubernetes --user=admin
kubectl config use-context rmq
kubectl config get-contexts
~~~


## Krewでオペレータをインストール

krewは事前にインストールしておく。
参考リンク: https://krew.sigs.k8s.io/docs/user-guide/setup/install/


プラグインrabbitmqで、オペレーターをインストールする。

~~~
kubectl krew install rabbitmq
kubectl rabbitmq install-cluster-operator
~~~

オペレーターの起動を確認する。

~~~
$ kubectl get po -n rabbitmq-system
NAME                                        READY   STATUS    RESTARTS   AGE
rabbitmq-cluster-operator-dcbc87df5-trp5n   1/1     Running   0          25h
~~~



## RabbitMQクラスタのデプロイ

RabbitMQのカスタムリソースをデプロイ

~~~
$ kubectl apply -f sample-rmq.yaml 
rabbitmqcluster.rabbitmq.com/rmq created

$ kubectl get po 
NAME           READY   STATUS    RESTARTS   AGE
rmq-server-0   1/1     Running   0          3m7s
rmq-server-1   1/1     Running   0          3m7s
rmq-server-2   1/1     Running   0          3m7s

$ kubectl get svc
NAME       TYPE         CLUSTER-IP   EXTERNAL-IP   PORT(S)
kubernetes ClusterIP    10.32.0.1    <none>        443/TCP
rmq        LoadBalancer 10.32.0.203  192.168.1.85  5672:30993/TCP,15672:32660/TCP,15692:31975/TCP
rmq-nodes  ClusterIP    None         <none>        4369/TCP,25672/TCP

$ kubectl get rabbitmqcluster
NAME   ALLREPLICASREADY   RECONCILESUCCESS   AGE
rmq    True               True               4m
~~~


