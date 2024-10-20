# Istio Ingtress Gatewayを使わないアクセス

Istioプロキシが注入されたアプリケーションのポッドをLoadBalancerでダイレクトの公開することもできる。

趙高負荷のシステムでは、Ingress-Gatwayに負荷が集中することになり、スケールできない懸念がある。
その対策として、外部ロードバランサーからサービスへダイレクトにリクエストを分配することが望ましい。



## アプリケーションのデプロイ

セッションカウンタのアプリケーションをデプロイする。このケースではマニュアルでIstioプロキシをインジェクトションする。

~~~
$ kubectl apply -f <(istioctl kube-inject -f session2.yaml)

~~~



