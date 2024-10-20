# Ingressによるセッションアフィニティの動作確認

ラボ環境でデフォルトでインストールしているNginxイングレスコントローラーを利用した
セッションアフィニティの機能を確認してみる。

K8sAPIオブジェクトのサービスでType LoadBalancerを指定すると、K8sクラスタ内部のサー
ビスをK8sクラスタ外へ公開できる。しかし、このサービスには、HTTPヘッダーのCookieの
情報によるセッションアフィニティの機能が無い。そのため、ログインした情報を保有する
特定のポッドへリクエストを転送することができない。
これでは、HTTPヘッダーのCookieにセッション情報を保持するタイプの従来型のウェブアプ
リケーションを動かすことができない。
その解決策となるのが、K8s APIのイングレス（Ingress)である。


## 準備作業 デフォルトのNamespaceの変更

専用の名前空間として apl-session を作成して、デフォルトにする。
事前にクライアント証明書のオーナーを変更しておき、編集可能にしておかなければならない。

~~~
sudo chown tkr:tkr ../../admin.kubeconfig-k8s3
kubectl create ns apl-session
kubectl config set-context apl-1 --namespace=apl-session --cluster=kubernetes --user=admin
kubectl config use-context apl-1
kubectl config get-contexts
~~


## 準備作業 ホスト名の変更

以下のYAMLファイルにあるホストのクラスタ名を変更する。

* ingress-tls.yaml
* session-ingress.yaml

変更例

~~~
- host: ingress.k8s2.labo.local -> ingress.k8s3.labo.local
~~~



## アプリケーションのデプロイ

HTTPヘッダーのCookieにセッション情報を保存して、アクセス回数をカウントするコンテナを
デプロイする。

~~~
$ kubectl apply -f session.yaml

$ kubectl get svc
NAME              TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)          AGE
session-ingress   ClusterIP      10.32.0.197   <none>          9080/TCP         4s

$ kubectl get pod
NAME                                          READY   STATUS    RESTARTS   AGE
session-deployment-ingress-5ff9954967-2xq4d   1/1     Running   0          6s
session-deployment-ingress-5ff9954967-8b2dm   1/1     Running   0          6s
session-deployment-ingress-5ff9954967-fj7tp   1/1     Running   0          6s
session-deployment-ingress-5ff9954967-jpjhh   1/1     Running   0          6s
session-deployment-ingress-5ff9954967-mr864   1/1     Running   0          6s
session-deployment-ingress-5ff9954967-nrx6k   1/1     Running   0          6s
session-deployment-ingress-5ff9954967-w7dqx   1/1     Running   0          6s
session-deployment-ingress-5ff9954967-xzglc   1/1     Running   0          6s
session-deployment-ingress-5ff9954967-zlrhb   1/1     Running   0          6s
session-deployment-ingress-5ff9954967-zzvvg   1/1     Running   0          6s
~~~


## イングレスのデプロイ

先にデプロイしたアプリケーションをK8sクラスタ外へ公開するためのAPIオブジェクトをデプロイ
する。

~~~
$ kubectl apply -f session-ingress.yaml

$ kubectl get ing
NAME              CLASS    HOSTS                                                    ADDRESS   PORTS   AGE
ingress-session   <none>   ingress-nginx-controller.ingress-nginx.k8s1.labs.local             80      4s
~~~

これでは、Ingressコントローラが保持する外部公開用のドメインを利用して、クラアントのリクエストトラフィックを
サービスを経由してポッドへ届けることができる。

下記のアクセステストの結果から、リクエストを特定のポッドへ導き、カウンターの値を増加させていることが読み取れる。

~~~
$ curl -c cookie   ingress-nginx-controller.ingress-nginx.k8s1.labs.local/session
Hostname: session-deployment-ingress-5ff9954967-zzvvg<br>
1th time access.
$ curl -b cookie   ingress-nginx-controller.ingress-nginx.k8s1.labs.local/session
Hostname: session-deployment-ingress-5ff9954967-zzvvg<br>
2th time access.
$ curl -b cookie   ingress-nginx-controller.ingress-nginx.k8s1.labs.local/session
Hostname: session-deployment-ingress-5ff9954967-zzvvg<br>
3th time access.
$ curl -b cookie   ingress-nginx-controller.ingress-nginx.k8s1.labs.local/session
Hostname: session-deployment-ingress-5ff9954967-zzvvg<br>
4th time access.
$ curl -b cookie   ingress-nginx-controller.ingress-nginx.k8s1.labs.local/session
Hostname: session-deployment-ingress-5ff9954967-zzvvg<br>
5th time access.
~~~




# 追加情報 TLS暗号化

## 名前空間 ingress-nginx のシークレットを他の名前空間へコピーする。

~~~
kubectl get secret ingress-credential -n ingress-nginx -oyaml | grep -v '^\s*namespace:\s' | kubectl apply -f -
~~~


## 暗号化Ingressをデプロイする

~~~
kubectl apply -f ingress-tls.yaml
~~~





# 実行例



~~~
tkr@hmc:~/k8s3/manifests/ingress-session-affinity$ sudo chown tkr:tkr ../../admin.kubeconfig-k8s3

tkr@hmc:~/k8s3/manifests/ingress-session-affinity$ kubectl create ns apl-session
Error from server (AlreadyExists): namespaces "apl-session" already exists

tkr@hmc:~/k8s3/manifests/ingress-session-affinity$ kubectl config set-context apl-1 --namespace=apl-session --cluster=kubernetes --user=admin
Context "apl-1" created.

tkr@hmc:~/k8s3/manifests/ingress-session-affinity$ kubectl config use-context apl-1
Switched to context "apl-1".

tkr@hmc:~/k8s3/manifests/ingress-session-affinity$ kubectl config get-contexts
CURRENT   NAME      CLUSTER      AUTHINFO   NAMESPACE
*         apl-1     kubernetes   admin      apl-session
          default   kubernetes   admin      

tkr@hmc:~/k8s3/manifests/ingress-session-affinity$ kubectl apply -f session.yaml 
deployment.apps/session-deployment-ingress created
service/session-ingress created


tkr@hmc:~/k8s3/manifests/ingress-session-affinity$ kubectl get all
NAME                                              READY   STATUS    RESTARTS   AGE
pod/session-deployment-ingress-68bf7d9d68-64sh9   1/1     Running   0          97s
pod/session-deployment-ingress-68bf7d9d68-6f59h   1/1     Running   0          97s
pod/session-deployment-ingress-68bf7d9d68-76kvg   1/1     Running   0          97s
pod/session-deployment-ingress-68bf7d9d68-ckd7f   1/1     Running   0          97s
pod/session-deployment-ingress-68bf7d9d68-ggr9x   1/1     Running   0          97s
pod/session-deployment-ingress-68bf7d9d68-l46rs   1/1     Running   0          97s
pod/session-deployment-ingress-68bf7d9d68-nk9hj   1/1     Running   0          97s
pod/session-deployment-ingress-68bf7d9d68-vvx7h   1/1     Running   0          97s
pod/session-deployment-ingress-68bf7d9d68-x67zb   1/1     Running   0          97s
pod/session-deployment-ingress-68bf7d9d68-zphp9   1/1     Running   0          97s

NAME                      TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
service/session-ingress   ClusterIP   10.32.0.40   <none>        9080/TCP   97s

NAME                                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/session-deployment-ingress   10/10   10           10          97s

NAME                                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/session-deployment-ingress-68bf7d9d68   10        10        10      97s
~~~


イングレスの設定を実施する。

~~~
tkr@hmc:~/k8s3/manifests/ingress-session-affinity$ kubectl apply -f session-ingress.yaml
ingress.networking.k8s.io/ingress-session created
tkr@hmc:~/k8s3/manifests/ingress-session-affinity$ kubectl get ingress
NAME              CLASS    HOSTS                     ADDRESS   PORTS   AGE
ingress-session   <none>   ingress.k8s3.labo.local             80      7s
~~~

イングレスのアドレスへアクセステスト

URLだけでアクセスすると、404 が帰る。

~~~
maho:~ maho$ curl http://ingress.k8s3.labo.local
<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx/1.19.2</center>
</body>
</html>
~~~

クッキーを保存しないで、実行しても機能しない。カウンターが上がらない。

~~~
maho:~ maho$ curl http://ingress.k8s3.labo.local/session
Hostname: session-deployment-ingress-68bf7d9d68-ckd7f<br>
1th time access.
maho:~ maho$ curl http://ingress.k8s3.labo.local/session
Hostname: session-deployment-ingress-68bf7d9d68-nk9hj<br>
1th time access.
maho:~ maho$ curl http://ingress.k8s3.labo.local/session
Hostname: session-deployment-ingress-68bf7d9d68-ckd7f<br>
1th time access.
~~~

クッキーの保存先を作成して、使用することで、セッションカウントが機能する。

~~~
maho:~ maho$ curl -c cookie http://ingress.k8s3.labo.local/session
Hostname: session-deployment-ingress-68bf7d9d68-x67zb<br>
1th time access.
maho:~ maho$ curl -b cookie http://ingress.k8s3.labo.local/session
Hostname: session-deployment-ingress-68bf7d9d68-x67zb<br>
2th time access.
maho:~ maho$ curl -b cookie http://ingress.k8s3.labo.local/session
Hostname: session-deployment-ingress-68bf7d9d68-x67zb<br>
3th time access.
maho:~ maho$ curl -b cookie http://ingress.k8s3.labo.local/session
Hostname: session-deployment-ingress-68bf7d9d68-x67zb<br>
4th time access.
~~~

クッキーの保存先指定を外すと、機能しない。

~~~
maho:~ maho$ curl http://ingress.k8s3.labo.local/session
Hostname: session-deployment-ingress-68bf7d9d68-zphp9<br>
1th time access.
maho:~ maho$ 
~~~

TLS暗号化セッションのテスト

~~~
tkr@hmc:~/k8s3/manifests/ingress-session-affinity$ kubectl get secret ingress-credential -n ingress-nginx -oyaml | grep -v '^\s*namespace:\s' | kubectl apply -f -
secret/ingress-credential created
tkr@hmc:~/k8s3/manifests/ingress-session-affinity$ kubectl get secret
NAME                  TYPE                                  DATA   AGE
default-token-cjr4l   kubernetes.io/service-account-token   3      19m
ingress-credential    kubernetes.io/tls                     2      6s
~~~

イングレスを変更

~~~
tkr@hmc:~/k8s3/manifests/ingress-session-affinity$ kubectl apply -f ingress-tls.yaml
ingress.networking.k8s.io/ingress-session configured
tkr@hmc:~/k8s3/manifests/ingress-session-affinity$ kubectl get ing
NAME              CLASS    HOSTS                     ADDRESS       PORTS     AGE
ingress-session   <none>   ingress.k8s3.labo.local   172.16.3.51   80, 443   12m
~~~

アクセステスト

~~~
maho:~ maho$ curl -k -b cookie https://ingress.k8s3.labo.local/session
Hostname: session-deployment-ingress-68bf7d9d68-x67zb<br>
5th time access.
maho:~ maho$ curl -k -b cookie https://ingress.k8s3.labo.local/session
Hostname: session-deployment-ingress-68bf7d9d68-x67zb<br>
6th time access.
maho:~ maho$ curl -k -b cookie https://ingress.k8s3.labo.local/session
Hostname: session-deployment-ingress-68bf7d9d68-x67zb<br>
7th time access.
~~~

