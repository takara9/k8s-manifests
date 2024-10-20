# Java Webアプリ Spring Boot

Spring Boot アクチュエータによる Liveness Prove と Readiness Prove の実装
Java Webアプリ コンテナ　コンテナ化アプリの雛形


OpenJDK 14、Spring Boot 2.3.1、Spring Boot アクチュエーターを利用したLivenessプローブとReadinessプローブへの応答例


## 模擬アプリケーションの機能

Spring Boot Actuator を利用して、Kubernetes の Livness Prove と Readiness Prove に対応する実装を検証したコードしたコードである。以下のYAML構成ファイルに対応する

~~~yaml:
    spec:
      containers:
      - name: java
        image: maho/web-java:0.1
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 30
          timeoutSeconds: 5
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 30
          timeoutSeconds: 10
          failureThreshold: 3
~~~

* アプリケーションのコンテンが起動して30秒後に、Readinessプローブへ HTTPレスポンス 200 (OK) を返すようになる。それまでの間は、503 (Service Unavailable:サービス利用不可)を返す。
* http://hostname:8080/greeting をGETでアクセスすると、HTMLで応答を返す。
* http://hostname:8080/bug をGETアクセスでは、Livenessプローブが、BROKENに変わり時期にコンテナがキルされ新しいコンテンが起動される。
* http://hostname:8080/crash をGETでアクセスすると、Nullポインタ例外が発生して、スタックトレースが表示される。



## コンテナイメージのDocker Hub への登録

~~~
docker build -t <dockerid>/webapl-4 .
docker push <dockerid>/webapl-4:1.0
~~~

## K8sへのデプロイ


環境設定

~~~
kubectl create ns webapl-java
kubectl config set-context webapl-java --namespace=webapl-java --cluster=kubernetes --user=admin
kubectl config use-context webapl-java
kubectl config get-contexts
~~~

### LoadBalanser で spring boot のサービスを公開する





### Istio配下で/greetingを公開する場合

~~~
cd k8s-yaml/base
kubectl apply -k ./
~~~


