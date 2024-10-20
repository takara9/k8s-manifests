# Istio Gateway を使って公開するアプリケーションの例

このサンプルコードは、模擬アプリのバージョン1と2をIstioのトラフィック管理機能を使って
一定の比率で、リクエストトラフィックを流すものです。比率は、v1:v2 = 8:2 となっています。



## ファイルの説明

* webapl-namespace.yaml     : このアプリ用の名前空間を作成、Isitoインジェクションの指定
* webapl-deployment-v1.yaml : アプリとしてVersion 1 を返す
* webapl-deployment-v2.yaml : アプリとしてVersion 2 を返す
* webapl-service.yaml       : ラベル app: webapls へリクエストを振るサービス
* webapl-destination-rule.yaml : webapls の転送先を設定
* webapl-virtual-service.yaml  : Ingressゲートウェイとサービスを繋ぐ仮想サービス
* webapl-virtual-service-weighted.yaml : 上記にウェイトを設定した版
* webapl-gateway.yaml : 外部にサービスを公開するIngressゲートウェイ



## デプロイ方法

~~~
kubectl apply -k ./
~~~


## ウェイト設定を無くす方法

~~~
kubectl apply -f webapl-virtual-service.yaml
~~~



## Isitoでのアクセステスト

IsitoのIngressゲートウェイ管理下のDNS名を求めて、アクセスを実施する。

istio-ingressgateway.istio-system.k8s3.labo.local/version
~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~ ~~~~~~~~~~~~~~~ ~~~~~~~
IstioイングレスGW名　Istio名前空間  K8sクラスタ名  アプリへのマッピング


~~~
curl http://istio-ingressgateway.istio-system.k8s3.labo.local/version
version: 1.0
~~~




## クリーンナップ

~~~
kubectl delete ns istio-apl
~~~

