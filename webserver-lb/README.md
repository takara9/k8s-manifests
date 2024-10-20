# ロードバランサーのテスト

IngressやIstioなどを介さず、K8sクラスタのフロントに配置されたロードバランサーで振り分けられたトラフィックを処理する。

専用の名前空間を設定してデフォルトにする。

~~~
kubectl create ns apl-1
kubectl config set-context apl1 --namespace=apl-1 --cluster=kubernetes --user=kubernetes-admin 
kubectl config use-context apl1
kubectl config get-contexts
~~~

アプリケーションをデプロイする。

~~~
tkr@hmc:~/k8s3/manifests/webserver-lb$ kubectl apply -f webserver1.yaml 
deployment.apps/webserver1 created
service/webserver1 created
~~~

状態確認して、ポッドが動作したら、次へ進む

~~~
tkr@hmc:~/k8s3/manifests/webserver-lb$ kubectl get pod -w
NAME                          READY   STATUS              RESTARTS   AGE
webserver1-85b94dd465-6497b   0/1     ContainerCreating   0          23s
webserver1-85b94dd465-9pftx   0/1     ContainerCreating   0          23s
webserver1-85b94dd465-q9klm   0/1     ContainerCreating   0          23s
webserver1-85b94dd465-9pftx   1/1     Running             0          32s
webserver1-85b94dd465-q9klm   1/1     Running             0          33s
webserver1-85b94dd465-6497b   1/1     Running             0          34s
~~~

ロードバランサーが取得したIPアドレスを表示して、このアドレスに接続してテストする。

~~~
tkr@hmc:~/k8s3/manifests/webserver-lb$ kubectl get svc
NAME         TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)                      AGE
webserver1   LoadBalancer   10.32.0.235   192.168.1.136   80:30947/TCP,443:31174/TCP   4m18s
~~~


以下のような応答があれば、成功だ。

~~~
maho:~ maho$ curl http://192.168.1.136
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>httpbin.org</title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700|Source+Code+Pro:300,600|Titillium+Web:400,600,700"
~~~
