# マイクロサービスの多層アプリケーション


## アプリケーションv1のデプロイ

~~~
$ kubectl apply -f ml-namespace.yaml
$ kubectl apply -f ml-deployment-v1.yaml
~~~

デプロイの確認結果

~~~
$ kubectl get pod -n istio-mla
NAME                          READY   STATUS      RESTARTS   AGE
ml-cache-766c59686c-qmg5m     2/2     Running     0          41s
ml-head-v1-5cbfdb99c9-dhqdn   2/2     Running     0          41s
ml-head-v1-5cbfdb99c9-hmnk7   2/2     Running     0          41s
ml-load-56kf5                 0/1     Completed   2          41s
~~~


## Istioによるサービスの公開


~~~
$ kubectl apply -f istio-gateway.yaml
$ kubectl apply -f istio-vs-v1.yaml
~~~


デプロイの確認結果

~~~
$ kubectl get gw -n istio-mla
NAME         AGE
ml-gateway   88s

$ kubectl get vs -n istio-mla
NAME         GATEWAYS         HOSTS                 AGE
ml-head-vs   ["ml-gateway"]   ["svc4.labo.local"]   82s

$ kubectl get dr -n istio-mla
NAME    HOST      AGE
ml-dr   ml-head   88s
~~~

アクセステスト

~~~
$ curl svc4.labo.local/phrase
{
    "id": 1032,
    "phrase": "Peace begins with a smile."
}
~~~


Kialiへのアクセス

~~~
$ kubectl get svc -n istio-system kiali
NAME    TYPE       CLUSTER-IP    EXTERNAL-IP   PORT(S)                          AGE
kiali   NodePort   10.32.0.159   <none>        20001:32001/TCP,9090:32090/TCP   4h3m
~~~

~~~
$ hv-status
<中略>

=== 仮想サーバーのリスト ===
VM-Name           HV-Host           vCPU      RAM(MB)   Pub-IP            Pri-IP          
master1-k8s3      akatsuki          2         2048      10.0.3.141        172.16.3.141    
master2-k8s3      aoba              2         2048      10.0.3.142        172.16.3.142    
master3-k8s3      nagato            2         2048      10.0.3.143        172.16.3.143    
~~~

ブラウザから次のアドレスをアクセス

http://10.0.3.141:32001/



## バージョンアップ

~~~
$ kubectl apply -f ml-counter-v1.yaml 
deployment.apps/ml-counter-v1 created
service/ml-counter created
deployment.apps/ml-head-v2 created
~~~

~~~
$ kubectl get pod -n istio-mla
NAME                             READY   STATUS      RESTARTS   AGE
ml-cache-766c59686c-qmg5m        2/2     Running     0          25m
ml-counter-v1-6cfc99bf97-9g7ph   2/2     Running     0          16s
ml-head-v1-5cbfdb99c9-dhqdn      2/2     Running     0          25m
ml-head-v1-5cbfdb99c9-hmnk7      2/2     Running     0          25m
ml-head-v2-646d8b6568-p66jw      2/2     Running     0          16s
ml-head-v2-646d8b6568-pvxdq      2/2     Running     0          16s
ml-load-56kf5                    0/1     Completed   2          25m
~~~


Istio Virtual Serviceの設定を変更

~~~
$ kubectl apply -f istio-vs-w.yaml 
virtualservice.networking.istio.io/ml-head-vs configured
destinationrule.networking.istio.io/ml-dr configured
~~~


アクセステスト
v1:v2 = 80:20

~~~
$ while true; do curl svc4.labo.local/phrase; sleep 1;done
{
    "id": 1019,
    "phrase": "Happiness depends upon ourselves.",
    "count": 1
}
{
    "id": 1023,
    "phrase": "Happiness depends upon ourselves."
}
{
    "id": 1035,
    "phrase": "Darkness cannot drive out darkness; only light can do that. Hate cannot drive out hate; only love can do that."
}
{
    "id": 1031,
    "phrase": "The meaning of life is to give life meaning.",
    "count": 1
}
{
    "id": 1005,
    "phrase": "Kites rise highest against the wind - not with it."
}
{
    "id": 1007,
    "phrase": "Our greatest glory is not in never failing, but in rising up every time we fail."
}
{
    "id": 1029,
    "phrase": "The time is always right to do what is right."
}
{
    "id": 1027,
    "phrase": "Never regret anything that made you smile."
}
{
    "id": 1066,
    "phrase": "The only way to do great work is to love what you do. If you haven`t found it yet, keep looking. Don`t settl.",
    "count": 1
}
~~~


Istio Virtual Serviceの設定を変更 v2だけに変更


~~~
$ kubectl apply -f istio-vs-v2.yaml
~~~


アクセステスト

~~~
maho:~ maho$ while true; do curl svc4.labo.local/phrase; sleep 1;done
{
    "id": 1032,
    "phrase": "Peace begins with a smile.",
    "count": 1
}
{
    "id": 1008,
    "phrase": "Failure is a detour, not a dead-end street.",
    "count": 1
}
{
    "id": 1059,
    "phrase": "Don`t find fault, find a remedy; anybody can complain.",
    "count": 1
}
{
    "id": 1001,
    "phrase": "Without haste, but without rest.",
    "count": 1
}
{
    "id": 1001,
    "phrase": "Without haste, but without rest.",
    "count": 2
}
{
    "id": 1047,
    "phrase": "A goal without a plan is just a wish.",
    "count": 1
}
{
    "id": 1062,
    "phrase": "Your time is limited, so don`t waste it living someone eles life.",
    "count": 1
}
{
    "id": 1016,
    "phrase": "Change the world by being yourself.",
    "count": 1
}
{
    "id": 1004,
    "phrase": "All your dreams can come true if you have the courage to pursue them.",
    "count": 1
}

~~~


## Counterのバージョン変更

カウンターアプリをバージョンアップする前に、VSでv1へルートを固定する。

~~~
$ kubectl apply -f istio-vs-counter-v1.yaml 
~~~


カウンターv2 をデプロイする。

~~~
$ kubectl apply -f ml-counter-v2.yaml 
~~~

ルートをv2へ100％にする。

~~~
$ kubectl apply -f istio-vs-counter-v2.yaml 
~~~


# サーキットブレーカー

これによりサーキットブレーカーが適用される。Kialiのアイコンが増えるので確認すると良い。

~~~
$ kubectl apply -f istio-vs-w-cb.yaml
~~~


