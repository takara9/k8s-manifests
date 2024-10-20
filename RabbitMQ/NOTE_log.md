tkr@hmc:~/k8s1$ cd manifests/RabbitMQ/
tkr@hmc:~/k8s1/manifests/RabbitMQ$ ls -la
total 20
drwxr-xr-x  3 tkr docker 4096  2月 24 07:04 .
drwxr-xr-x 63 tkr docker 4096  2月 22 14:58 ..
-rw-r--r--  1 tkr docker 1247  2月 24 07:04 README.md
drwxr-xr-x  3 tkr docker 4096  2月 24 07:11 sample-go
-rw-r--r--  1 tkr docker  238  2月 23 08:50 sample-rmq.yaml

tkr@hmc:~/k8s1/manifests/RabbitMQ$ kubectl krew install rabbitmq
Updated the local copy of plugin index.
  New plugins available:
    * ice
    * nsenter
  Upgrades available for installed plugins:
    * rabbitmq v1.12.0 -> v1.12.1
Installing plugin: rabbitmq
W0315 19:55:25.313821  220646 install.go:160] Skipping plugin "rabbitmq", it is already installed


tkr@hmc:~/k8s1/manifests/RabbitMQ$ kubectl rabbitmq install-cluster-operator
namespace/rabbitmq-system created
customresourcedefinition.apiextensions.k8s.io/rabbitmqclusters.rabbitmq.com created
serviceaccount/rabbitmq-cluster-operator created
role.rbac.authorization.k8s.io/rabbitmq-cluster-leader-election-role created
clusterrole.rbac.authorization.k8s.io/rabbitmq-cluster-operator-role created
rolebinding.rbac.authorization.k8s.io/rabbitmq-cluster-leader-election-rolebinding created
clusterrolebinding.rbac.authorization.k8s.io/rabbitmq-cluster-operator-rolebinding created
deployment.apps/rabbitmq-cluster-operator created



tkr@hmc:~/k8s1/manifests/RabbitMQ$ kubectl get po -n rabbitmq-system
NAME                                         READY   STATUS    RESTARTS   AGE
rabbitmq-cluster-operator-755c76fc56-272c7   1/1     Running   0          63s


tkr@hmc:~/k8s1/manifests/RabbitMQ$ kubectl config get-contexts
CURRENT   NAME      CLUSTER      AUTHINFO   NAMESPACE
*         ceph      kubernetes   admin      ceph-csi
          default   kubernetes   admin      
tkr@hmc:~/k8s1/manifests/RabbitMQ$ kubectl config use-context default
Switched to context "default".



tkr@hmc:~/k8s1/manifests/RabbitMQ$ kubectl apply -f sample-rmq.yaml 
rabbitmqcluster.rabbitmq.com/rmq created
tkr@hmc:~/k8s1/manifests/RabbitMQ$ kubectl get po
NAME           READY   STATUS     RESTARTS   AGE
rmq-server-0   0/1     Init:0/1   0          6s
rmq-server-1   0/1     Init:0/1   0          6s
rmq-server-2   0/1     Init:0/1   0          6s
tkr@hmc:~/k8s1/manifests/RabbitMQ$ kubectl get po
NAME           READY   STATUS    RESTARTS   AGE
rmq-server-0   0/1     Running   0          28s
rmq-server-1   0/1     Running   0          28s
rmq-server-2   0/1     Running   0          28s
tkr@hmc:~/k8s1/manifests/RabbitMQ$ kubectl get po
NAME           READY   STATUS    RESTARTS   AGE
rmq-server-0   1/1     Running   0          51s
rmq-server-1   1/1     Running   0          51s
rmq-server-2   1/1     Running   0          51s
tkr@hmc:~/k8s1/manifests/RabbitMQ$ kubectl get svc
NAME         TYPE           CLUSTER-IP    EXTERNAL-IP    PORT(S)                                          AGE
kubernetes   ClusterIP      10.32.0.1     <none>         443/TCP                                          22m
rmq          LoadBalancer   10.32.0.237   192.168.1.84   15672:32365/TCP,15692:30043/TCP,5672:32374/TCP   56s
rmq-nodes    ClusterIP      None          <none>         4369/TCP,25672/TCP                               56s
tkr@hmc:~/k8s1/manifests/RabbitMQ$ kubectl get rabbitmqcluster
NAME   ALLREPLICASREADY   RECONCILESUCCESS   AGE
rmq    True               True               69s
tkr@hmc:~/k8s1/manifests/RabbitMQ$ kubectl get pvc
NAME                       STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
persistence-rmq-server-0   Bound    pvc-911b3145-a3e7-4786-9fc7-cfa58022c655   10Gi       RWO            csi-rbd-sc     74s
persistence-rmq-server-1   Bound    pvc-ac42b554-f4c4-4a18-9df0-d65bc3ea4f96   10Gi       RWO            csi-rbd-sc     74s
persistence-rmq-server-2   Bound    pvc-37f535ef-c2da-4ef4-a99c-4d8111d4cd73   10Gi       RWO            csi-rbd-sc     74s
tkr@hmc:~/k8s1/manifests/RabbitMQ$ kubectl get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                              STORAGECLASS   REASON   AGE
pvc-37f535ef-c2da-4ef4-a99c-4d8111d4cd73   10Gi       RWO            Delete           Bound    default/persistence-rmq-server-2   csi-rbd-sc              77s
pvc-911b3145-a3e7-4786-9fc7-cfa58022c655   10Gi       RWO            Delete           Bound    default/persistence-rmq-server-0   csi-rbd-sc              77s
pvc-ac42b554-f4c4-4a18-9df0-d65bc3ea4f96   10Gi       RWO            Delete           Bound    default/persistence-rmq-server-1   csi-rbd-sc              77s
tkr@hmc:~/k8s1/manifests/RabbitMQ$


tkr@hmc:~/k8s1/manifests/RabbitMQ/sample-go$ kubectl -n default get secret rmq-default-user -o jsonpath="{.data.username}" | base64 --decode;echo
default_user_y-AeFQQk8iGfRxbiU2C
tkr@hmc:~/k8s1/manifests/RabbitMQ/sample-go$ kubectl -n default get secret rmq-default-user -o jsonpath="{.data.password}" | base64 --decode;echo
8cysQGZK_FvmbKX_svRzVbUeFabp9r09




送信側
tkr@hmc:~/k8s1/manifests/RabbitMQ/sample-go$ go run send.go default_user_y-AeFQQk8iGfRxbiU2C 8cysQGZK_FvmbKX_svRzVbUeFabp9r09 192.168.1.84
> hello
2022/03/15 21:48:05  [x] Sent hello


受信側
tkr@hmc:~/k8s1/manifests/RabbitMQ/sample-go$ go run receive.go default_user_y-AeFQQk8iGfRxbiU2C 8cysQGZK_FvmbKX_svRzVbUeFabp9r09 192.168.1.84
2022/03/15 21:47:50  [*] Waiting for messages. To exit press CTRL+C
2022/03/15 21:48:05 Received a message: hello


