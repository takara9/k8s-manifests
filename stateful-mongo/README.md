# Mongoデータベースのデプロイ


## 専用のネームスペース作成と変更

~~~
kubectl create ns mongodb
kubectl config set-context mongo --namespace=mongodb --cluster=kubernetes --user=admin
kubectl config use-context mongo
kubectl config get-contexts
~~~


## MongoDBの設定ファイルをコンフィグマップへ登録

~~~
$ kubectl create configmap mongodb-config --from-file=mongod.conf
~~~


## ルートパスワード、ユーザーとパスワードの設定

~~~
$ kubectl apply -f userid-passwd.yaml 
secret/mongodb-auth created

$ kubectl get secret mongodb-auth
NAME                  TYPE                                  DATA   AGE
mongodb-auth          kubernetes.io/basic-auth              2      4s
~~~


## MongoDBのデプロイ

~~~
$ kubectl apply -f mongodb-server.yaml
persistentvolumeclaim/mongodb-data created
persistentvolumeclaim/mongodb-log created
deployment.apps/mongodb created
service/mongodb created
~~~

~~~
$ kubectl get po
NAME                       READY   STATUS              RESTARTS   AGE
mongodb-84577b794c-7g9st   1/1     Running             0          7s
~~~



## MongodDBへユーザー登録

~~~
$ kubectl get pod
NAME                       READY   STATUS    RESTARTS   AGE
mongodb-84577b794c-s4mlf   1/1     Running   0          5h35m

$ kubectl exec -it mongodb-84577b794c-s4mlf -- bash
root@mongodb-84577b794c-s4mlf:/# env
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_SERVICE_PORT=443
HOSTNAME=mongodb-84577b794c-s4mlf
MONGODB_PORT_27017_TCP=tcp://10.32.0.247:27017
MONGODB_SERVICE_PORT=27017
PWD=/
MONGO_INITDB_ROOT_PASSWORD=t0p-Secret
MONGO_INITDB_ROOT_USERNAME=root
<省略
~~~

MongoDBのrootで、ログインしてユーザーを作成

~~~
root@mongodb-84577b794c-s4mlf:/# mongo -u root -p t0p-Secret
MongoDB shell version v4.4.10
<省略>
> use admin
> db.createUser(
... {
... user: "t001",
... pwd: "password",
... roles: [
...   { role: "readWrite", db: "testdb" },
... ]
... }
... )
Successfully added user: {
	"user" : "t001",
	"roles" : [
		{
			"role" : "readWrite",
			"db" : "testdb"
		}
	]
}
~~~


## クライアントポッドからのアクセス

対話型でポッドを起動して、mongodb-clientsをインストール

~~~
$ kubectl run -it mongo-client --image=maho/my-ubuntu:0.1 -- bash
root@mongo-client:/# apt-get update -y
root@mongo-client:/# apt install -y mongodb-clients
~~~

クライアントのポッドで、前述で作成したユーザーでログインして、既存データを検索

~~~
root@mongo-client:/# mongo --host mongodb -u t001 -p --authenticationDatabase "admin"
MongoDB shell version v3.6.3
Enter password: 
connecting to: mongodb://mongodb:27017/
MongoDB server version: 4.4.10
WARNING: shell and server versions do not match
> use testdb
switched to db testdb
> db.things.find()
{ "_id" : ObjectId("616be1610fc90f63e158e3b3"), "first_name" : "Keisuke", "email" : "dadosan@keicode.com" }
~~~




以上







