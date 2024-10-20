# ポッドのPDツール


## 準備

テスト用に専用の名前空間を作成

~~~
sudo chown tkr:tkr ../../admin.kubeconfig-k8s3
kubectl create ns apl-pdtool
kubectl config set-context apl-pd --namespace=apl-pdtool --cluster=kubernetes --user=admin
kubectl config use-context apl-pd
kubectl config get-contexts
~~


## デプロイ

~~~
$ kubectl apply -f webserver-node3.yaml 
deployment.apps/pd-tools created
service/pd-tools created
~~~

## デプロイチェック

~~~
$ kubectl get all
NAME                           READY   STATUS    RESTARTS   AGE
pod/pd-tools-586c9fcfd-bjgc7   1/1     Running   0          39m

NAME               TYPE       CLUSTER-IP   EXTERNAL-IP   PORT(S)        AGE
service/pd-tools   NodePort   10.32.0.52   <none>        80:30300/TCP   39m

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/pd-tools   1/1     1            1           39m

NAME                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/pd-tools-586c9fcfd   1         1         1       39m
~~~


## アクセステスト

* http://<Node external IP>:30300  HTMLページを応答
* http://<Node external IP>:30300/info  JSON形式で応答

以下は、JSON形式でリクエストしたときの応答です。
IPアドレスはポッドのIPアドレスとなり、
hostはクライアントがアクセスしたホストとポートです。

~~~
maho:pod-pd-tools maho$ curl -s http://192.168.1.111:30300/info |jq
{
  "hostname": "pd-tools-586c9fcfd-bjgc7",
  "ip": "10.244.6.29/24",
  "host": "192.168.1.111:30300",
  "agent": "curl/7.64.1"
}
~~~

