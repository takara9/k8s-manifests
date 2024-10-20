# K8sクラスタのためのアドオン・マニフェスト

## ロードバランサー＆イングレスコントローラー

* kube-keepalived-vip
* ingress-nginx
* ingress-haproxy

#### kube-keepalived-vip

ワーカー・ノードにVIPを設け、VIPへアクセス到達したトラフィックを指定の名前空間とサービス名へ転送する。Ingressコントローラーを介さないので、転送のみしか使えないが、IngressコントローラーのようにDNS名を必須としない。DNSとIngressコントローラーなどのコンポーネントの数を減らし、独立性を維持できるので、シンプルで堅牢な構成を作る事ができる。抑えておきたいコンポーネント。

#### ingress-nginx

NGINXを使用したIngressコントローラーで、パブリッククラウドでも利用される。URLリライト、仮想ホスト、セッション維持、デフォルトバックエンドなどの機能がある。NGINX Ingressコントローラー単独では、クラスタ外部のリクエストを受けられないので、前述のkube-keepalived-vipと合わせて利用する。

#### ingress-haproxy

Red hat OpenShiftなどで利用されるIngressコントローラーで、NGINX Ingress コントローラーほど豊富ではないが、同様の機能がある。HA-PROXYには、もともと高可用性の機能があるために、ノードの不慮の停止に対して、代替ノード上で機能を再開させやすい。こちらも、単独では外部のリクエストを受けられないため、kube-keepalived-vipと合わせて利用する。



## テスト用アプリケーション

これらはウェブベースのテスト用アプリケーション

* echoheader
* webserver
* webserver-ingress
* webserver-session-affinity


#### echoheader

HTTPヘッダーのエコーを返すだけのシンプルなアプリケーション。サービスとデプロイメントのセットである。


#### webserver

Nginxのデプロイメントとサービスの組み合わせで、サービスのタイプはNodePortとしている。


#### webserver-ingress

前述のwebserverをIngressを使って、VIPと共にクラスタ外へサービスを公開する。



#### webserver-session-affinity

NGINX Ingress のセッション・アフィニティ機能を確認するためのアプリケーションで、ポッドのホスト名とアクセス回数のカウンタ値をリプライする。
curlでのテストにあたっては、curl のオプション -c と -b を適切に使い分ける。１回目は -c で保存用ファイルを作成 ２回目以降は -b で読み取りと書き込みを実施する。

~~~
curl -c xxx -H 'Host:abc.sample.com' http://172.16.1.200/  # １回目
curl -b xxx -H 'Host:abc.sample.com' http://172.16.1.200/  # ２回目以降
~~~



※今後、ポッド名を返すアプリ、それから、負荷をかけるアプリ(CPU負荷、メモリ消費)のタイプがあると良いな


