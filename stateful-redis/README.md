# ステートフルなアプリケーションのテスト

環境設定

~~~
kubectl create ns redis
kubectl config set-context redis --namespace=redis --cluster=kubernetes --user=admin
kubectl config use-context redis
kubectl config get-contexts
~~~


設定ファイルのデプロイ

~~~
$ kubectl create configmap redis-config --from-file=redis.conf
~~~



Redisのデプロイ

~~~
$ kubectl apply -f redis-kvs.yaml
~~~


実行例

~~~
tkr@hmc:~/k8s3/manifests/stateful-redis$ kubectl create configmap redis-config --from-file=redis.conf
configmap/redis-config created

tkr@hmc:~/k8s3/manifests/stateful-redis$ kubectl apply -f redis-kvs.yaml
service/redis created
persistentvolumeclaim/redis-vol created
deployment.apps/redis created

tkr@hmc:~/k8s3/manifests/stateful-redis$ kubectl get all
NAME                         READY   STATUS    RESTARTS   AGE
pod/redis-696598454f-qrbgk   1/1     Running   0          73s

NAME            TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
service/redis   ClusterIP   None         <none>        6379/TCP   73s

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/redis   1/1     1            1           74s

NAME                               DESIRED   CURRENT   READY   AGE
replicaset.apps/redis-696598454f   1         1         1       74s
~~~


アクセステストは、対話型ポッドを立ち上げて redis-toolsをインストール、redis-cliで操作して確認

~~~
$ kubectl run -it redis-client --image maho/my-ubuntu:0.1 -- bash
If you don't see a command prompt, try pressing enter.
root@redis-client:/# apt-get update -y
root@redis-client:/# apt install redis-tools -y
root@redis-client:/# redis-cli -h redis  
redis:6379> keys *
(empty list or set)
redis:6379> set gundam RX78
OK
redis:6379> set guncanon RX77
OK
redis:6379> keys *
1) "gundam"
2) "guncanon"
redis:6379> get gundam
"RX78"
redis:6379> get guncanon
"RX77"
~~~

