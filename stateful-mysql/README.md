# ステートフルなアプリケーションのテスト

環境設定

~~~
kubectl create ns mysql
kubectl config set-context mysql --namespace=mysql --cluster=kubernetes --user=admin
kubectl config use-context mysql
kubectl config get-contexts
~~~

MySQLの設定ファイルを名前空間へ保存

~~~
$ kubectl create configmap mysql-config --from-file=conf.d
~~~

認証情報をネームスペースへ保存


~~~
$ kubectl apply -f mysql-auth.yaml 
~~~


MySQLサーバーのデプロイ

~~~
$ kubectl apply -f mysql-db.yaml
service/mysql created
persistentvolumeclaim/mysql-vol created
deployment.apps/mysql created
~~~

エンドポイントの確認

~~~
$ kubectl get svc
NAME    TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
mysql   ClusterIP   None         <none>        3306/TCP   154m

$ kubectl get ep
NAME    ENDPOINTS           AGE
mysql   10.244.5.120:3306   154m

$ kubectl get pod -o wide
NAME                     READY   STATUS    RESTARTS   AGE    IP           
mysql-85b6f949cd-lxtjz   1/1     Running   0          156m   10.244.5.120 
~~~




MySQLサーバーへのログイン

~~~
$ kubectl run -it client --image maho/my-ubuntu:0.1 -- bash
If you don't see a command prompt, try pressing enter.
root@client:/# apt-get update -y
root@client:/# apt install -y mysql-client
root@client:/# mysql -h mysql -u root -ppassw0rd
mysql> show databases;
+---------------------+
| Database            |
+---------------------+
| information_schema  |
| #mysql50#lost+found |
| mysql               |
| performance_schema  |
+---------------------+
4 rows in set (0.00 sec)
~~~

