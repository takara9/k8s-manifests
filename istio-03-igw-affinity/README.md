# セッションアフィニティ機能の確認

## アプリケーションのデプロイ

セッションカウンタのアプリケーションをデプロイする。このケースではマニュアルでIstioプロキシを
ポッドへ注入する。ここでは、istioctl kube-inject コマンドが、ポッドテンプレートを判別して、そ
のポッドに、Istioプロキシーのポッドを追加している。

~~~
$ kubectl apply -f <(istioctl kube-inject -f session.yaml)

$ kubectl get pod
NAME                                  READY   STATUS    RESTARTS   AGE
session-deployment-58b4547d8d-hkn75   2/2     Running   0          11s
~~~

セッションアフィニティのテストのために、ポッド数を増やしておく。

~~~
$ kubectl scale deployment.v1.apps/session-deployment --replicas=5
$ kubectl get deploy
NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
session-deployment   5/5     5            5           5m
~~~


##　Istio イングレスゲートウェイとバーチャルサーバーのデプロイ

次のように、ゲートウェイとバーチャルサービスのYAMLを適用して、オブジェクトを生成する。

~~~
$ kubectl apply -f session-gateway.yaml

$ kubectl get gw
NAME              AGE
session-gateway   2m

$ kubectl get vs
NAME      GATEWAYS            HOSTS   AGE
session   [session-gateway]   [*]     2m
~~~

この状態でアクセステストすると、Hostnameがランダムに変わっていることから、
複数のポッドへ、リクエストが分散していることが読み取れる。

~~~
$ curl -c cookie.dat http://istio-ingressgateway.istio-system.k8s1.labs.local/user
Hostname: session-deployment-7d9db8c579-fjjn2<br>
1th time access.
$ curl -b cookie.dat http://istio-ingressgateway.istio-system.k8s1.labs.local/user
Hostname: session-deployment-7d9db8c579-mjltp<br>
1th time access.
$ curl -b cookie.dat http://istio-ingressgateway.istio-system.k8s1.labs.local/user
Hostname: session-deployment-7d9db8c579-rngkt<br>
1th time access.
$ curl -b cookie.dat http://istio-ingressgateway.istio-system.k8s1.labs.local/user
Hostname: session-deployment-7d9db8c579-jpjmm<br>
1th time access.
$ curl -b cookie.dat http://istio-ingressgateway.istio-system.k8s1.labs.local/user
Hostname: session-deployment-7d9db8c579-fjjn2<br>
~~~


## Istioディステネーションルールによって、セッションアフィニティを実施する。

~~~
$ kubectl apply -f session-affinity.yaml

$ kubectl get dr
NAME      HOST          AGE
session   session-svc   7s
~~~

アクセステストの結果では、Hostnameの値、すなわち、同じポッドへ、リクエストが転送されている
ことが解る。しかし、カウンタの値は更新されない。つまり、セッションの情報はHTTPヘッダーに保存
するのではなく、ポッドのメモリ上またはデータストアに保持することが求められる。

~~~
$ curl -c cookie http://istio-ingressgateway.istio-system.k8s1.labs.local/user
Hostname: session-deployment-58b4547d8d-hxwxk<br>
1th time access.

$ curl -b cookie http://istio-ingressgateway.istio-system.k8s1.labs.local/user
Hostname: session-deployment-58b4547d8d-hxwxk<br>
1th time access.

$ curl -b cookie http://istio-ingressgateway.istio-system.k8s1.labs.local/user
Hostname: session-deployment-58b4547d8d-hxwxk<br>
1th time access.

$ curl -b cookie http://istio-ingressgateway.istio-system.k8s1.labs.local/user
Hostname: session-deployment-58b4547d8d-hxwxk<br>
1th time access.

$ curl -b cookie http://istio-ingressgateway.istio-system.k8s1.labs.local/user
Hostname: session-deployment-58b4547d8d-hxwxk<br>
1th time access.

$ curl -b cookie http://istio-ingressgateway.istio-system.k8s1.labs.local/user
Hostname: session-deployment-58b4547d8d-hxwxk<br>
1th time access.
~~~



