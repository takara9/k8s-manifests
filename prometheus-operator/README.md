# Perometheus Operator

## 事前に名前空間monitoringを作成して、デフォルトにしておく。

~~~
kubectl create ns monitoring
kubectl config set-context mon --namespace=monitoring --cluster=kubernetes --user=admin
kubectl config use-context mon
kubectl config get-contexts
~~~

## プロメテウスオペレーターのクローンとデプロイ

~~~
git clone -b release-0.10 https://github.com/prometheus-operator/kube-prometheus
cd kube-prometheus/
kubectl apply --server-side -f manifests/setup
kubectl apply -f manifests/
~~~


## 永続ボリュームの設定

prometheus-prometheus.yaml 以下のようにspec.storage以下を追加

~~~
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  labels:
    app.kubernetes.io/component: prometheus
    app.kubernetes.io/instance: k8s
    app.kubernetes.io/name: prometheus
    app.kubernetes.io/part-of: kube-prometheus
    app.kubernetes.io/version: 2.32.1
  name: k8s
  namespace: monitoring
spec:
  storage:
    volumeClaimTemplate:
      spec:
        storageClassName: csi-rbd-sc
        resources:
          requests:
            storage: 40Gi
  alerting:
    alertmanagers:
...
~~~

参考資料: https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/user-guides/storage.md


## 起動完了状態

~~~
$ kubectl get po -n monitoring
NAME                                   READY   STATUS    RESTARTS   AGE
alertmanager-main-0                    2/2     Running   0          69s
alertmanager-main-1                    2/2     Running   0          68s
alertmanager-main-2                    2/2     Running   0          68s
blackbox-exporter-6798fb5bb4-pcv6j     3/3     Running   0          98s
grafana-78d8cfccff-htkd9               1/1     Running   0          97s
kube-state-metrics-5fcb7d6fcb-lnnld    3/3     Running   0          97s
node-exporter-bfmkh                    2/2     Running   0          96s
node-exporter-c9sbn                    2/2     Running   0          96s
node-exporter-g9tzk                    2/2     Running   0          96s
node-exporter-r6sh8                    2/2     Running   0          96s
prometheus-adapter-7dc46dd46d-9kpn2    1/1     Running   0          96s
prometheus-adapter-7dc46dd46d-gbhqz    1/1     Running   0          96s
prometheus-k8s-0                       2/2     Running   0          68s
prometheus-k8s-1                       2/2     Running   0          68s
prometheus-operator-7ddc6877d5-97c49   2/2     Running   0          96s
~~~



## ポートフォワードでアクセスする時のコマンド

~~~
kubectl --namespace monitoring port-forward svc/prometheus-k8s 9090
kubectl --namespace monitoring port-forward svc/grafana 3000
kubectl --namespace monitoring port-forward svc/alertmanager-main 9093
~~~
