## 概要

Nginx Ingress コントローラーでアプリケーションを
公開するための構成ファイル(マニフェスト）


## 説明

Ingress コントローラーを設定することで、サービスのタイプ ClusterIP で
クラスタ内部へ公開するアプリケーションを外部へ公開することができる。

このマニフェストは、コンテナイメージ 'docker.io/maho/webapl3:0.1' の
サービスをKubernetesクラスタ外へ公開する。


## 事前準備

専用の名前空間を作成してデフォルトを変更する。

~~~
kubectl create ns apl-ingress
kubectl config set-context a-ing --namespace=apl-ingress --cluster=kubernetes --user=admin
kubectl config use-context a-ing
kubectl config get-contexts
~~~

ingressのホスト名を変更する。

'- host: ingress.k8s3.labs.local' の k8s3の部分がクラスタ名なので、実行するクラスタ名に置き換える。



## デプロイ方法

`kubectl apply -f webserver3.yaml` を実行することで、前述の全てのAPIオブジェクト
をデプロイする。

~~~
$ kubectl apply -f webserver3.yaml 
namespace/webserver3 created
service/webserver created
deployment.apps/webserver created
ingress.networking.k8s.io/webserver created


$ kubectl get all -n webserver3
NAME                             READY   STATUS    RESTARTS   AGE
pod/webserver-5dcfb59bff-bsvwg   1/1     Running   0          13s
pod/webserver-5dcfb59bff-k9d8k   1/1     Running   0          13s
pod/webserver-5dcfb59bff-z7wjx   1/1     Running   0          13s

NAME                TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/webserver   ClusterIP   10.32.0.30   <none>        80/TCP    13s

NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/webserver   3/3     3            3           13s

NAME                                   DESIRED   CURRENT   READY   AGE
replicaset.apps/webserver-5dcfb59bff   3         3         3       13s

$ kubectl get ingress -n webserver3
NAME        CLASS    HOSTS            ADDRESS        PORTS   AGE
webserver   <none>   k8s.labs.local   172.16.23.43   80      25s
~~~


## アクセス方法

Ingressで公開するアプリケーションにアクセスするためには、
必ず DNSに登録された URLアドレスでなかればならない。

予めイングレスコントローラーが動作するノードのVIPを
外部DNSに登録しておき、そのDNSでアドレスを解決することで
ブラウザから URL ingress.k8s3.labo.local によってアクセスできる。
簡便な方法では、`curl ingress.k8s3.labo.local` として確認できる。

~~~
$ curl ingress.k8s3.labo.local
Hostname: webserver-5dcfb59bff-k9d8k<br>
1th time access.
<br>
HTTP_CLIENT_IP = <br>
HTTP_X_FORWARDED_FOR = 10.244.104.0<br>
HTTP_X_FORWARDED = <br>
HTTP_X_CLUSTER_CLIENT_IP = <br>
HTTP_FORWARDED_FOR = <br>
HTTP_FORWARDED = <br>
REMOTE_ADDR = 10.244.135.1<br>
~~~


## クリーンナップ方法

コマンド `kubectl delete ns webserver3` によって消去できる。




# 実行例

名前空間を作成して、デフォルトを変更する。

~~~
tkr@hmc:~/k8s3/manifests/webserver-ingress$ kubectl create ns apl-ingress
namespace/apl-ingress created
tkr@hmc:~/k8s3/manifests/webserver-ingress$ kubectl config set-context a-ing --namespace=apl-ingress --cluster=kubernetes --user=admin
Context "a-ing" created.
tkr@hmc:~/k8s3/manifests/webserver-ingress$ kubectl config use-context a-ing
Switched to context "a-ing".
tkr@hmc:~/k8s3/manifests/webserver-ingress$ kubectl config get-contexts
CURRENT   NAME      CLUSTER      AUTHINFO   NAMESPACE
*         a-ing     kubernetes   admin      apl-ingress
          apl-1     kubernetes   admin      apl-session
          apl-ci    kubernetes   admin      apl-cluster-ip
          default   kubernetes   admin
~~~

アプリをデプロイ

~~~
tkr@hmc:~/k8s3/manifests/webserver-ingress$ kubectl apply -f webserver3.yaml 
service/webserver3 created
deployment.apps/webserver3 created
ingress.networking.k8s.io/webserver3 created
~~~

デプロイを確認

~~~
tkr@hmc:~/k8s3/manifests/webserver-ingress$ kubectl get -f webserver3.yaml 
NAME                 TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
service/webserver3   ClusterIP   10.32.0.155   <none>        80/TCP    9s

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/webserver3   3/3     3            3           9s

NAME                                   CLASS    HOSTS                     ADDRESS       PORTS   AGE
ingress.networking.k8s.io/webserver3   <none>   ingress.k8s3.labs.local   172.16.3.51   80      9s
~~~


