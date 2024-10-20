# Istio Eagress Gateway の検証

外部にあるREST-APIサーバーをアクセスするためのegress-gatewayの設定を実施する。



## EgressGateway を有効化する方法

Istioオペレータからインストール状態を取得

~~~
$ kubectl -n istio-system get IstioOperator installed-state -o yaml > installed-state.yaml
~~~

メタデータを削除して、spec.components.egressGateways 以下の enabled = true に変更

~~~
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  namespace: istio-system
spec:
  addonComponents:
    istiocoredns:
      enabled: false
  components:
    base:
      enabled: true
    cni:
      enabled: false
    egressGateways:
    - enabled: true
      k8s:
        env:
<以下省略>
~~~

変更をIstioオペレータへ伝える

~~~
$ istioctl install -f installed-state.yaml 
Detected that your cluster does not support third party JWT authentication.
Falling back to less secure first party JWT.
See https://istio.io/docs/ops/best-practices/security/#configure-third-party-service-account-tokens for details.
✔ Istio core installed
✔ Istiod installed
✔ Ingress gateways installed
✔ Egress gateways installed
✔ Installation complete
~~~

Egressゲートウェイが起動したことを確認する。

~~~
$ kubectl get pod -l istio=egressgateway -n istio-system
NAME                                   READY   STATUS    RESTARTS   AGE
istio-egressgateway-64bbcc6d9b-fhjcf   1/1     Running   0          38s
~~~



## 登録されなサイトへのアクセス禁止

現在の設定を取り出し

~~~
$ kubectl -n istio-system get IstioOperator installed-state -o yaml > installed-state.yaml
~~~

metadataのnameとnamespace以外の設定を削除して、次のオプションをセットしてアクセス禁止にする。

~~~
$ istioctl install -f installed-state.yaml --set meshConfig.outboundTrafficPolicy.mode=REGISTRY_ONLY
~~~





## KubernetesクラスタのCoreDNSの設定

オンプレ、プライベートクラウド、パブリッククラウドで、CoreDNSが、ローカル側のDNSを参照していないと、
隣のK8sクラスタのサービスのDNS名を解決できない。そのため、設定を先に実施する必要がある。



## k8sクラスタ外部にREST-APIサービスを起動

検証の準備として、k8sクラスタ外部に、または、外部のK8sクラスタに、REST-APIサービスを起動する。
maho/webapl5:0.1 をデプロイ、このサンプルアプリの詳細は https://github.com/takara9/webapl-5 を参照

~~~
$ kubectl apply -f ext-service/webapl5.yaml
$ kubectl get svc
NAME         TYPE           CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE
webapl5      LoadBalancer   10.32.0.201   10.0.2.82     80:31940/TCP     5m49s
~~~

アクセスできることを確認

~~~
$ curl http://webapl5.default.k8s2.labo.local/api/v1/person
[]
~~~

この後、Istio管理下のポッドからアクセスして、Kialiで連携が表示されることを確認する。
K8sクラスタ k8s3のIsito管理下のコンテナから、k8s2の上記サービスをアクセスする。



## サンドボックス用の名前空間を作成する。

~~~
$ kubectl create -f create_ns.yaml
~~~

~~~
$ kubectl config set-context istio-sb --cluster=kubernetes --user=admin --namespace=sandbox

$ kubectl config use-context istio-sb
$ kubectl config get-contexts
CURRENT   NAME       CLUSTER      AUTHINFO   NAMESPACE
          default    kubernetes   admin      
*         isito-sb   kubernetes   admin      sandbox
~~~



## IstioのAPIオブジェクトを作成する。

エクスターナルゲートウェイを設定する。

~~~
$ kubectl create -f gw.yaml
$ kubectl create -f vs.yaml
$ kubectl create -f dr.yaml
$ kubectl create -f se.yaml
~~~



## テスト用アプリを起動してアクセステスト


このコマンドを実行することで、シェルから外部アクセスを試すポッドを起動する。

~~~
$ kubectl apply -f local-apl/webapl-6.yaml
~~~

~~~
$ kubectl get pod
NAME                       READY   STATUS    RESTARTS   AGE
webapl6-796b44949d-w7xb2   2/2     Running   0          45h
~~~

~~~
$ kubectl exec -it webapl6-796b44949d-w7xb2 -- bash
root@webapl6-796b44949d-w7xb2:/# curl -i http://webapl5.default.k8s2.labo.local/api/v1/person

HTTP/1.1 200 OK
content-type: application/json
date: Sat, 30 Jan 2021 15:58:50 GMT
x-envoy-upstream-service-time: 7
server: envoy
transfer-encoding: chunked
~~~
