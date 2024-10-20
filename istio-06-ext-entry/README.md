# Istio Service Entry の検証

外部にあるREST-APIサーバーをアクセスするためのService Entry設定を実施する。


## KubernetesクラスタのCoreDNSの設定

オンプレ、プライベートクラウド、パブリッククラウドで、CoreDNSが、ローカル側のDNSを参照していないと、
隣のK8sクラスタのサービスのDNS名を解決できない。そのため、設定を先に実施する必要がある。


## k8sクラスタ外部にREST-APIサービスを起動

検証の準備として、k8sクラスタ外部に、または、外部のK8sクラスタに、REST-APIサービスを起動する。
maho/webapl5:0.1 をデプロイ、このサンプルアプリの詳細は https://github.com/takara9/webapl-5 を参照

~~~
$ cd ext-service
kubectl apply -f webapl5.yaml

$ kubectl get svc
NAME         TYPE           CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE
webapl5      LoadBalancer   10.32.0.201   10.0.2.82     8080:31940/TCP   5m49s
~~~

アクセスできることを確認

~~~
$ curl http://webapl5.default.k8s2.labo.local:8080/api/v1/person
[]
~~~

この後、Istio管理下のポッドからアクセスして、Kialiで連携が表示されることを確認する。
K8sクラスタ k8s3のIsito管理下のコンテナから、k8s2の上記サービスをアクセスする。




## テスト用のネームスペースとコンテキストを作成する

Istioのテスト用名前空間を作成、オートインジェクションを設定する

~~~
$ kubectl create -f create_ns.yaml
namespace/sandbox created
~~~

デフォルトの名前空間の設定する。

~~~
$ kubectl config set-context istio-sb --cluster=kubernetes --user=admin --namespace=sandbox
$ kubectl config use-context istio-sb
$ kubectl config get-contexts
CURRENT   NAME       CLUSTER      AUTHINFO   NAMESPACE
          default    kubernetes   admin      
*         isito-sb   kubernetes   admin      sandbox
~~~




## メッシュ外部へのアクセスの禁止

Istioオペレーターから設定情報を出力する。

~~~
$ kubectl -n istio-system get IstioOperator installed-state -o yaml > installed-state.yaml
~~~

Istioオペレーターに、アウトボウンドのポリシー REGISTRY_ONLY を設定する。

~~~
$ istioctl install -f installed-state.yaml --set meshConfig.outboundTrafficPolicy.mode=REGISTRY_ONLY
~~~

もし、反対にすべてを許可する場合は、ALLOW_ANY を設定する。




## テスト用のアプリケーションを起動する

このコマンドを実行することで、シェルから外部アクセスを試すポッドを起動する。

~~~
$ kubectl apply -f local-apl/webapl-6.yaml
~~~



## アクセステストの実施　＃1

Service Entry が入っていない状態なので、アクセスに失敗することを確認する。
ポッドから、外部に立ち上げたサービスをアクセスする。

~~~
$ kubectl get pod
NAME                       READY   STATUS    RESTARTS   AGE
webapl6-796b44949d-w7xb2   2/2     Running   0          45h
~~~

エラーが返ってくることを確認。502が予定どおりの結果

~~~
$ kubectl exec -it webapl6-796b44949d-w7xb2 -- bash
root@webapl6-796b44949d-w7xb2:/# curl -i http://webapl5.default.k8s2.labo.local:8080/api/v1/person
HTTP/1.1 502 Bad Gateway
date: Sat, 30 Jan 2021 11:59:01 GMT
server: envoy
content-length: 0
~~~



## アクセステストの実施　＃2

Service Entry を設定して、アクセス可能であることを確認する。

~~~
$ kubectl apply -f se.yaml 
serviceentry.networking.istio.io/webapl5 created
~~~

結果は 200 であることを確認する。

~~~
$ kubectl exec -it webapl6-796b44949d-w7xb2 -- bash

root@webapl6-796b44949d-w7xb2:/# curl -i http://webapl5.default.k8s2.labo.local:8080/api/v1/person
HTTP/1.1 200 OK
content-type: application/json
date: Sat, 30 Jan 2021 12:22:22 GMT
x-envoy-upstream-service-time: 5
server: envoy
transfer-encoding: chunked

[]
~~~



