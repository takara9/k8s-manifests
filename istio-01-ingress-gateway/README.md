# Istioのテスト用サンプル

目的は、IstioのIngress Gatewayを利用して、K8sクラスタの外部からのリクエストトラフィックを、特定のサービスへ繋ぐ方法を確認する。

このマニフェストは、https://httpbin.org/ で公開されるhttpbinをIstioサービスとして実行します。このhttpbin は、あらゆる種類のIstio機能の実験に使用できるよく知られたHTTPテストサービスです。



## httpbin アプリケーションのデプロイ方法

httpbinアプリケーションのデプロイは、次の2つの方法から選択できる。


名前空間が、Istioのサイドカー自動インジェクション機能が有効になっている場合は、次のコマンドで実行する。

~~~
$ kubectl apply -f httpbin.yaml
~~~

名前空間 default などで、マニュアルでIstioプロキシを注入するには、次のコマンドを実行する。

~~~
istioctl kube-inject -f httpbin.yaml | kubectl apply -f -
~~~

ここ迄で、サービスとポッドがデプロイされていることが読み取れる。それから、ポッドのREADY列の2/2は、Istioプロキシが注入されているためである。

~~~
$ kubectl get svc
NAME         TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
httpbin      ClusterIP   10.32.0.219   <none>        8000/TCP   6h28m
kubernetes   ClusterIP   10.32.0.1     <none>        443/TCP    7h24m

$ kubectl get pod
NAME                       READY   STATUS    RESTARTS   AGE
httpbin-585687bd86-7tpjr   2/2     Running   0          6h28m
~~~



## ゲートウェイとバーチャルサービスのデプロイ


K8sクラスタの外部からのリクエストを受けるために、IstioのAPIオブジェクト Gateway と VirtualServiceをデプロイする。
Gatewayは、Istioのingressgatewayのリクエストを取得し、VirtualServiceは、Gatewayで受けたリクエストをK8s APIオブジェクトのサービス httpbin へ転送する。

~~~
$ kubectl apply -f httpbin-gateway.yaml
~~~

これで、ゲートウェイとバーチャルサービスが生成されているのが読み取れる。
バーチャルサービスは、ゲートウェイhttpbin-gateway を参照していることがわかる。

~~~
$ kubectl get gateway
NAME              AGE
httpbin-gateway   6h27m

$ kubectl get virtualservice
NAME      GATEWAYS            HOSTS   AGE
httpbin   [httpbin-gateway]   [*]     6h28m
~~~

httpbin-gatewayが、どのistio-ingressgatewayを参照するかを調べるには、次のコマンドでjsonpathを指定する。

~~~
$ kubectl get gw -o jsonpath='{.items[*].spec.selector}';echo
map[istio:ingressgateway]
~~~

istio:ingressgatewayのIPアドレスを知るには、名前空間istio-systemの中で、istio-ingressgateway を探す。

~~~
$ kubectl get svc -n istio-system istio-ingressgateway 
NAME                   TYPE           CLUSTER-IP   EXTERNAL-IP     PORT(S)                                                      AGE
istio-ingressgateway   LoadBalancer   10.32.0.79   192.168.1.202   15021:30109/TCP,80:31696/TCP,443:31185/TCP,15443:31192/TCP   7h35m
~~~

## アクセステスト

IPアドレスによるアクセステスト

~~~
$ curl -i -s 192.168.1.202 |head -n 2
HTTP/1.1 200 OK
server: istio-envoy
~~~

DNSによるアクセステストでは、URLは「サービス名.名前空間名.クラスタ名.ドメイン」となる。
このラボ環境では以下になる。

* サービス名: istio-ingressgateway 
* 名前空間名: istio-system
* K8sクラスタ名: k8s3
* ドメイン: labs.local

これからURLを組み立てて、次のようにアクセスできる。

~~~
$ curl -is http://istio-ingressgateway.istio-system.k8s3.labo.local |head -n 2
HTTP/1.1 200 OK
server: istio-envoy
~~~

httpbinのアプリケーションをAPIの一つ /html アクセスすると、次の結果が得られる。

~~~
$ curl http://istio-ingressgateway.istio-system.k8s3.labo.local/html
<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
      <h1>Herman Melville - Moby-Dick</h1>
      <div>
        <p>
          Availing himself of the mild, summer-cool weather that now reigned in these latitudes, and in preparation for the peculiarly active pursuits shortly to be anticipated, Perth, the begrimed, blistered old blacksmith
~~~

もう一つ、/get でヘッダー情報を表示できる。

~~~
$ curl http://istio-ingressgateway.istio-system.k8s3.labo.local/get
{
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Content-Length": "0", 
    "Host": "istio-ingressgateway.istio-system.k8s1.labs.local", 
    "User-Agent": "curl/7.64.1", 
    "X-B3-Parentspanid": "0f14610164d3cdf1", 
    "X-B3-Sampled": "0", 
    "X-B3-Spanid": "7a9055faea285195", 
    "X-B3-Traceid": "adbc2f309e9895320f14610164d3cdf1", 
    "X-Envoy-Attempt-Count": "1", 
    "X-Envoy-Internal": "true", 
    "X-Forwarded-Client-Cert": "By=spiffe://cluster.local/ns/default/sa/httpbin;Hash=def38a9e7e828649a1812804586875a4814bff884c080946a6374e17884e1acb;Subject=\"\";URI=spiffe://cluster.local/ns/istio-system/sa/istio-ingressgateway-service-account"
  }, 
  "origin": "192.168.122.231", 
  "url": "http://istio-ingressgateway.istio-system.k8s1.labs.local/get"
}
~~~





