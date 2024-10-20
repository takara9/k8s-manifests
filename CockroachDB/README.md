# CockroachDB

## 専用名前空間の作成

~~~
kubectl create ns crdb
kubectl config set-context crdb --namespace=crdb --cluster=kubernetes --user=admin
kubectl config use-context crdb
kubectl config get-contexts
~~~

ステートフルセットでの構築方法と、オペレーターによる構築方法の２つの方法が利用できる。


## ステートフルセットによる構築

次のコマンドで、コックローチDBのポッドクラスタとロードバランサーを起動する。

~~~
cd statefulset
kubectl apply -f crdb-sts.yaml
kubectl apply -f crdb-lb.yaml
~~~

起動が完了したら、クラスタの活動を開始する。

~~~
kubectl apply -f crdb-init.yaml
~~~



## オペレーターによる構築

カスタムリソース定義を追加、オペレータをデプロイ、オペレーターのポッド起動の確認

~~~
kubectl apply -f https://raw.githubusercontent.com/cockroachdb/cockroach-operator/v2.4.0/install/crds.yaml
kubectl apply -f https://raw.githubusercontent.com/cockroachdb/cockroach-operator/v2.4.0/install/operator.yaml
kubectl get po -n cockroach-operator-system
NAME                                          READY   STATUS    RESTARTS   AGE
cockroach-operator-manager-74f6c548b8-zlxsx   1/1     Running   0          27s
~~~


## オペレーターを使ったデータベースクラスタの構築

~~~
$ kubectl apply -f sampledb.yaml

$ kubectl get po
NAME        READY   STATUS    RESTARTS   AGE
my-crdb-0   1/1     Running   0          77s
my-crdb-1   1/1     Running   0          77s
my-crdb-2   1/1     Running   0          77s
my-crdb-3   1/1     Running   0          77s
my-crdb-4   1/1     Running   0          77s

$ kubectl get pvc
NAME                STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
datadir-my-crdb-0   Bound    pvc-3a675450-8ac5-40c2-94cb-537f20770a9e   60Gi       RWO            csi-rbd-sc     98s
datadir-my-crdb-1   Bound    pvc-9970347e-9743-4439-9dc8-20abfef0924b   60Gi       RWO            csi-rbd-sc     98s
datadir-my-crdb-2   Bound    pvc-c0e7add2-c920-400b-8af6-14a546821c91   60Gi       RWO            csi-rbd-sc     98s
datadir-my-crdb-3   Bound    pvc-c7c15395-efb0-4d4f-8474-e20643f1a0da   60Gi       RWO            csi-rbd-sc     98s
datadir-my-crdb-4   Bound    pvc-b5205772-3511-4a8e-be9b-dd9cf19b31c9   60Gi       RWO            csi-rbd-sc     98s

$ kubectl get svc
NAME             TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)                        AGE
my-crdb          ClusterIP   None          <none>        26258/TCP,8080/TCP,26257/TCP   119s
my-crdb-public   ClusterIP   10.32.0.124   <none>        26258/TCP,8080/TCP,26257/TCP   119s
~~~


## クライアントの起動


~~~
$ kubectl create -f https://raw.githubusercontent.com/cockroachdb/cockroach-operator/master/examples/client-secure-operator.yaml
pod/cockroachdb-client-secure created

$ kubectl get po cockroachdb-client-secure
NAME                        READY   STATUS    RESTARTS   AGE
cockroachdb-client-secure   1/1     Running   0          56s

$ kubectl exec -it cockroachdb-client-secure  -- ./cockroach sql --certs-dir=/cockroach/cockroach-certs  --host=cockroachdb-public
#
# Welcome to the CockroachDB SQL shell.
# All statements must be terminated by a semicolon.
# To exit, type: \q.
#
# Client version: CockroachDB CCL v21.2.5 (x86_64-unknown-linux-gnu, built 2022/02/07 21:01:07, go1.16.6)
# Server version: CockroachDB CCL v21.1.11 (x86_64-unknown-linux-gnu, built 2021/10/18 14:39:35, go1.15.14)

warning: server version older than client! proceed with caution; some features may not be available.

# Cluster ID: ab6c5431-3c80-48f2-9f75-23baeaf0f945
#
# Enter \? for a brief introduction.
#
root@cockroachdb-public:26257/defaultdb> 
~~~


## データの書き込みテスト

~~~
root@cockroachdb-public:26257/defaultdb> CREATE DATABASE bank;
CREATE DATABASE


Time: 108ms total (execution 108ms / network 0ms)

root@cockroachdb-public:26257/defaultdb> CREATE TABLE bank.accounts (id INT PRIMARY KEY, balance DECIMAL);
CREATE TABLE


Time: 87ms total (execution 87ms / network 0ms)

root@cockroachdb-public:26257/defaultdb> INSERT INTO bank.accounts VALUES (1, 1000.50);
INSERT 1


Time: 113ms total (execution 112ms / network 0ms)

root@cockroachdb-public:26257/defaultdb> SELECT * FROM bank.accounts;
  id | balance
-----+----------
   1 | 1000.50
(1 row)


Time: 3ms total (execution 3ms / network 0ms)
~~~


## パスワード設定　Web管理画面アクセスなど用途

~~~
root@cockroachdb-public:26257/defaultdb> CREATE USER roach WITH PASSWORD 'Q7gc8rEdS';
CREATE ROLE


Time: 160ms total (execution 160ms / network 0ms)

root@cockroachdb-public:26257/defaultdb> GRANT admin TO roach;
GRANT


Time: 366ms total (execution 366ms / network 0ms)
~~~


## 起動確認

~~~
tkr@hmc:~/k8s1/manifests/CockroachDB$ kubectl get po -o wide
NAME                        READY   STATUS    RESTARTS   AGE   IP               NODE    NOMINATED NODE   READINESS GATES
cockroachdb-0               1/1     Running   0          36m   172.17.3.68      node4   <none>           <none>
cockroachdb-1               1/1     Running   0          36m   172.17.135.7     node3   <none>           <none>
cockroachdb-2               1/1     Running   0          36m   172.17.104.3     node2   <none>           <none>
cockroachdb-client-secure   1/1     Running   0          16m   172.17.166.134   node1   <none>           <none>
~~~

## 模擬障害発生

ワーカーノードのVMから停止させて、模擬障害とする。

~~~
root@hv3:/home/tkr# virsh destroy node4-k8s1
Domain node4-k8s1 destroyed
~~~
node4が停止している状態

~~~
tkr@hmc:~/k8s1/manifests/CockroachDB$ kubectl get no
NAME      STATUS     ROLES    AGE   VERSION
master1   Ready      master   86m   v1.22.4
node1     Ready      worker   83m   v1.22.4
node2     Ready      worker   83m   v1.22.4
node3     Ready      worker   83m   v1.22.4
node4     NotReady   worker   83m   v1.22.4
~~~

データにアクセスできることを確認

~~~
root@cockroachdb-public:26257/defaultdb> SELECT * FROM bank.accounts;
  id | balance
-----+----------
   1 | 1000.50
(1 row)


Time: 2ms total (execution 2ms / network 0ms)

root@cockroachdb-public:26257/defaultdb> SELECT * FROM bank.accounts;
ERROR: rpc error: code = Unavailable desc = transport is closing
root@cockroachdb-public:26257/defaultdb> SELECT * FROM bank.accounts;
  id | balance
-----+----------
   1 | 1000.50
(1 row)


Time: 439ms total (execution 439ms / network 0ms)

root@cockroachdb-public:26257/defaultdb> SELECT * FROM bank.accounts;
  id | balance
-----+----------
   1 | 1000.50
(1 row)


Time: 1ms total (execution 1ms / network 0ms)
~~~



## Benchmarkテスト

~~~
cockroach init --url postgresql://root@192.168.1.84:26257 --insecure
cockroach workload fixtures import tpcc --warehouses=10 'postgresql://root@192.168.1.84:26257?sslmode=disable'
cockroach workload run tpcc --warehouses=10 --ramp=3m --duration=10m 'postgresql://root@192.168.1.182:32257?sslmode=disable'
_elapsed___errors__ops/sec(inst)___ops/sec(cum)__p50(ms)__p95(ms)__p99(ms)_pMax(ms)
    1.0s        0            0.0            0.0      0.0      0.0      0.0      0.0 delivery
    1.0s        0            0.0            0.0      0.0      0.0      0.0      0.0 newOrder
    1.0s        0            0.0            0.0      0.0      0.0      0.0      0.0 orderStatus
    1.0s        0            0.0            0.0      0.0      0.0      0.0      0.0 payment
    1.0s        0            0.0            0.0      0.0      0.0      0.0      0.0 stockLevel
    2.0s        0            0.0            0.0      0.0      0.0      0.0      0.0 delivery
    2.0s        0            0.0            0.0      0.0      0.0      0.0      0.0 newOrder
    2.0s        0            0.0            0.0      0.0      0.0      0.0      0.0 orderStatus
    2.0s        0            0.0            0.0      0.0      0.0      0.0      0.0 payment
    2.0s        0            0.0            0.0      0.0      0.0      0.0      0.0 stockLevel
    3.0s        0            0.0            0.0      0.0      0.0      0.0      0.0 delivery
    3.0s        0            0.0            0.0      0.0      0.0      0.0      0.0 newOrder
    3.0s        0            1.0            0.3    302.0    302.0    302.0    302.0 orderStatus
    3.0s        0            0.0            0.0      0.0      0.0      0.0      0.0 payment
    3.0s        0            0.0            0.0      0.0      0.0      0.0      0.0 stockLevel

...

_elapsed___errors__ops/sec(inst)___ops/sec(cum)__p50(ms)__p95(ms)__p99(ms)_pMax(ms)
  604.1s        0            0.0            0.2      0.0      0.0      0.0      0.0 delivery
  604.1s        0            1.0            2.0    104.9    104.9    104.9    104.9 newOrder
  604.1s        0            1.0            0.2     19.9     19.9     19.9     19.9 orderStatus
  604.1s        0            3.0            2.1     71.3     79.7     79.7     79.7 payment
  604.1s        0            0.0            0.2      0.0      0.0      0.0      0.0 stockLevel
  605.1s        0            1.0            0.2    134.2    134.2    134.2    134.2 delivery
  605.1s        0            2.0            2.0     83.9    100.7    100.7    100.7 newOrder
  605.1s        0            0.0            0.2      0.0      0.0      0.0      0.0 orderStatus
  605.1s        0            0.0            2.1      0.0      0.0      0.0      0.0 payment
  605.1s        0            0.0            0.2      0.0      0.0      0.0      0.0 stockLevel
  606.1s        0            0.0            0.2      0.0      0.0      0.0      0.0 delivery
  606.1s        0            2.0            2.0     79.7     83.9     83.9     83.9 newOrder
  606.1s        0            1.0            0.2     19.9     19.9     19.9     19.9 orderStatus
  606.1s        0            3.0            2.1     75.5     75.5     75.5     75.5 payment
  606.1s        0            0.0            0.2      0.0      0.0      0.0      0.0 stockLevel

_elapsed___errors_____ops(total)___ops/sec(cum)__avg(ms)__p50(ms)__p95(ms)__p99(ms)_pMax(ms)__total
  606.1s        0            118            0.2    142.2    142.6    192.9    285.2    385.9  delivery

_elapsed___errors_____ops(total)___ops/sec(cum)__avg(ms)__p50(ms)__p95(ms)__p99(ms)_pMax(ms)__total
  606.1s        0           1237            2.0    103.4     96.5    167.8    352.3    704.6  newOrder

_elapsed___errors_____ops(total)___ops/sec(cum)__avg(ms)__p50(ms)__p95(ms)__p99(ms)_pMax(ms)__total
  606.1s        0            126            0.2     23.2     19.9     31.5     92.3    218.1  orderStatus

_elapsed___errors_____ops(total)___ops/sec(cum)__avg(ms)__p50(ms)__p95(ms)__p99(ms)_pMax(ms)__total
  606.1s        0           1246            2.1     71.1     67.1    121.6    268.4    570.4  payment

_elapsed___errors_____ops(total)___ops/sec(cum)__avg(ms)__p50(ms)__p95(ms)__p99(ms)_pMax(ms)__total
  606.1s        0            126            0.2     31.6     23.1     60.8    318.8    318.8  stockLevel

_elapsed___errors_____ops(total)___ops/sec(cum)__avg(ms)__p50(ms)__p95(ms)__p99(ms)_pMax(ms)__result
  606.1s        0           2853            4.7     84.2     79.7    159.4    318.8    704.6  
Audit check 9.2.1.7: SKIP: not enough delivery transactions to be statistically significant
Audit check 9.2.2.5.1: SKIP: not enough orders to be statistically significant
Audit check 9.2.2.5.2: SKIP: not enough orders to be statistically significant
Audit check 9.2.2.5.5: SKIP: not enough payments to be statistically significant
Audit check 9.2.2.5.6: SKIP: not enough order status transactions to be statistically significant
Audit check 9.2.2.5.3: SKIP: not enough orders to be statistically significant
Audit check 9.2.2.5.4: SKIP: not enough payments to be statistically significant

_elapsed_______tpmC____efc__avg(ms)__p50(ms)__p90(ms)__p95(ms)__p99(ms)_pMax(ms)
  606.1s      122.5  95.2%    103.4     96.5    142.6    167.8    352.3    704.6
~~~
