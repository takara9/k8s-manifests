# Istio-Ingress-Gateway の仮想ホスト


下記のIngressゲートウェイのEXTERNAL-IPに対して、アプリケーションへのアクセス用のDNS名を2つ登録しておく。

~~~
$ kubectl get svc istio-ingressgateway -n istio-system
NAME                   TYPE           CLUSTER-IP   EXTERNAL-IP   PORT(S)                                                      AGE
istio-ingressgateway   LoadBalancer   10.32.0.93   10.0.3.42     15021:32312/TCP,80:30781/TCP,443:30461/TCP,15443:30185/TCP   2d8h
~~~

DNSのエントリーは、次のようにする。 10.0.3.42 のIPアドレスは、以下の3つのDNS名から求められるようにしておく。
* istio-ingressgateway.istio-system.k8s3.labo.local
* svc1.labo.local
* svc2.labo.local

~~~
labo.local.	3600 IN SOA ns1.labo.local. root.labo.local. (
<中略>

; Ingress Gateway
igw3            3600 IN  A     10.0.3.42
svc1            3600 IN  CNAME igw3          ; Istio apl #1
svc2            3600 IN  CNAME igw3          ; Istio apl #2
~~~



名前空間が、Istioのサイドカー自動インジェクション機能が有効になっている場合は、次のコマンドで実行する。

~~~
$ kubectl apply -f webapl-1.yaml
~~~

名前空間 default などで、マニュアルでIstioプロキシを注入するには、次のコマンドを実行する。

~~~
istioctl kube-inject -f webapl-1.yaml | kubectl apply -f -
kubectl apply -f virtualhost-gateway-1.yaml
~~~

もう一つのアプリとIsito gw設定を起動する。

~~~
istioctl kube-inject -f webapl-2.yaml | kubectl apply -f -
kubectl apply -f virtualhost-gateway-2.yaml
~~~


これで、以下のように、DNS名を変えるだけでルーティングするアプリケーションを変更できる。

svc1.labo.local -> webapl1
svc2.labo.local -> webapl2



