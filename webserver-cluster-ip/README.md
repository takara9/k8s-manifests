# Service Cluster IP のテスト

クラスタ内部のポッドクラスタを作成して、ポッドからのアクセステストを実施する。

準備作業として、ネームスペースを作成してデフォルトを変更する

~~~
sudo chown tkr:tkr ../../admin.kubeconfig-k8s3
kubectl create ns apl-cluster-ip
kubectl config set-context apl-ci --namespace=apl-cluster-ip --cluster=kubernetes --user=admin
kubectl config use-context apl-ci
kubectl config get-contexts
~~


webserver1.yaml をデプロイして、アクセステストを実施する。

~~~
tkr@hmc:~/k8s3/manifests/webserver-cluster-ip$ kubectl create ns apl-cluster-ip
namespace/apl-cluster-ip created
tkr@hmc:~/k8s3/manifests/webserver-cluster-ip$ kubectl config set-context apl-ci --namespace=apl-cluster-ip --cluster=kubernetes --user=admin
Context "apl-ci" created.
tkr@hmc:~/k8s3/manifests/webserver-cluster-ip$ kubectl config use-context apl-ci
Switched to context "apl-ci".
tkr@hmc:~/k8s3/manifests/webserver-cluster-ip$ kubectl config get-contexts
CURRENT   NAME      CLUSTER      AUTHINFO   NAMESPACE
          apl-1     kubernetes   admin      apl-session
*         apl-ci    kubernetes   admin      apl-cluster-ip
          default   kubernetes   admin      
~~~

デプロイ

~~~
tkr@hmc:~/k8s3/manifests/webserver-cluster-ip$ kubectl apply -f webserver1.yaml
service/webserver1 created
deployment.apps/webserver1 created
~~~

動作確認

~~~
tkr@hmc:~/k8s3/manifests/webserver-cluster-ip$ kubectl get all
NAME                              READY   STATUS    RESTARTS   AGE
pod/webserver1-6cbddc5b58-pcgzt   1/1     Running   0          70s
pod/webserver1-6cbddc5b58-r8nhq   1/1     Running   0          70s
pod/webserver1-6cbddc5b58-rrpsb   1/1     Running   0          70s

NAME                 TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
service/webserver1   ClusterIP   10.32.0.254   <none>        80/TCP    70s

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/webserver1   3/3     3            3           70s

NAME                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/webserver1-6cbddc5b58   3         3         3       70s
~~~

対話型のポッドを起動して、サービスの名称でアクセスする。

~~~
tkr@hmc:~/k8s3/manifests/webserver-cluster-ip$ kubectl run -it client --image maho/my-ubuntu:0.1 -- bash
If you don't see a command prompt, try pressing enter.
root@client:/# curl http://webserver1
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
~~~


ネームスペース外からアクセスする場合は、名前空間名を追加して、アクセスする。


~~~
tkr@hmc:~/k8s3/manifests/webserver-cluster-ip$ kubectl config use-context default
Switched to context "default".

tkr@hmc:~/k8s3/manifests/webserver-cluster-ip$ kubectl config get-contexts
CURRENT   NAME      CLUSTER      AUTHINFO   NAMESPACE
          apl-1     kubernetes   admin      apl-session
          apl-ci    kubernetes   admin      apl-cluster-ip
*         default   kubernetes   admin      

tkr@hmc:~/k8s3/manifests/webserver-cluster-ip$ kubectl run -it client --image maho/my-ubuntu:0.1 -- bash
If you don't see a command prompt, try pressing enter.
root@client:/# curl http://webserver1.apl-cluster-ip
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
~~~


## webserver2 のテスト

オブジェクトのデプロイ

~~~
tkr@hmc:~/k8s3/manifests/webserver-cluster-ip$ kubectl config use-context apl-ci
Switched to context "apl-ci".
tkr@hmc:~/k8s3/manifests/webserver-cluster-ip$ kubectl apply -f webserver2.yaml
service/webserver2 created
deployment.apps/webserver2 created
~~~

デプロイ結果の確認

~~
tkr@hmc:~/k8s3/manifests/webserver-cluster-ip$ kubectl get all --selector=app=webserver2
NAME                             READY   STATUS    RESTARTS   AGE
pod/webserver2-68c6d456c-7dwhf   1/1     Running   0          7m9s
pod/webserver2-68c6d456c-v9wc5   1/1     Running   0          7m12s
pod/webserver2-68c6d456c-vd4n4   1/1     Running   0          7m11s

NAME                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/webserver2-68c6d456c    3         3         3       7m12s
replicaset.apps/webserver2-85c464787f   0         0         0       12m

tkr@hmc:~/k8s3/manifests/webserver-cluster-ip$ kubectl get svc
NAME         TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
webserver1   ClusterIP   10.32.0.254   <none>        80/TCP    55m
webserver2   ClusterIP   10.32.0.181   <none>        80/TCP    12m
~~~

アクセステスト

~~~
tkr@hmc:~/k8s3/manifests/webserver-cluster-ip$ kubectl exec -it client -- bash
root@client:/# curl http://webserver2
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
  <title>Web Application 2</title>
~~~

