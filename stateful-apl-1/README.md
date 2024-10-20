# ステートフルなアプリケーションのテスト

環境設定

~~~
kubectl create ns apl-stateful-pvc
kubectl config set-context apl-sta-1 --namespace=apl-stateful-pvc --cluster=kubernetes --user=admin
kubectl config use-context apl-sta-1
kubectl config get-contexts
~~~

構成ファイルをコンフィグマップに保存する

~~~
$ kubectl create configmap datastore-config --from-file=datastore.conf

$ kubectl get cm
NAME                 DATA   AGE
datastore-config     1      8s
~~~

ユーザーIDとパスワードをシークレットに保存する

~~~
$ kubectl apply -f userid-password.yaml 
secret/datastore-auth created

$ kubectl get secret
NAME                  TYPE                                  DATA   AGE
datastore-auth        kubernetes.io/basic-auth              2      7s
default-token-6ndnk   kubernetes.io/service-account-token   3      12h

$ kubectl get secret -o yaml datastore-auth
apiVersion: v1
data:
  password: dDBwLVNlY3JldA==
  username: YWRtaW4=
kind: Secret
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Secret","metadata":{"annotations":{},"name":"datastore-auth","namespace":"apl-stateful-pvc"},"stringData":{"password":"t0p-Secret","username":"admin"},"type":"kubernetes.io/basic-auth"}
  creationTimestamp: "2021-10-10T14:39:19Z"
  managedFields:
  - apiVersion: v1
    fieldsType: FieldsV1
    fieldsV1:
      f:data:
        .: {}
        f:password: {}
        f:username: {}
      f:metadata:
        f:annotations:
          .: {}
          f:kubectl.kubernetes.io/last-applied-configuration: {}
      f:type: {}
    manager: kubectl-client-side-apply
    operation: Update
    time: "2021-10-10T14:39:19Z"
  name: datastore-auth
  namespace: apl-stateful-pvc
  resourceVersion: "5182727"
  uid: db08d73d-f2f6-4ce1-baa7-98cd022f0351
type: kubernetes.io/basic-auth
~~~

pvd, deployment, service をデプロイする


~~~
$ kubectl apply -f stateful-server.yaml 
persistentvolumeclaim/rook-rbd-pvc created
deployment.apps/data-server1 created
service/data-server1 created

$ kubectl get pod
NAME                            READY   STATUS    RESTARTS   AGE
data-server1-54cbb874b9-fpz64   1/1     Running   0          23s
~~~


シークレットの環境変数が渡っていることの確認として、
ポッドの環境変数を調べる。

~~~
$ kubectl exec -it data-server1-54cbb874b9-fpz64 -- bash
root@data-server1-54cbb874b9-fpz64:/# echo $SECRET_USERNAME
admin
root@data-server1-54cbb874b9-fpz64:/# echo $SECRET_PASSWORD
t0p-Secret
~~~