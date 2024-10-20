$ kubectl get customresourcedefinitions.apiextensions.k8s.io
NAME                                                  CREATED AT
bgpconfigurations.crd.projectcalico.org               2022-03-15T10:42:01Z
bgppeers.crd.projectcalico.org                        2022-03-15T10:42:01Z
blockaffinities.crd.projectcalico.org                 2022-03-15T10:42:01Z
caliconodestatuses.crd.projectcalico.org              2022-03-15T10:42:01Z
clusterinformations.crd.projectcalico.org             2022-03-15T10:42:01Z
felixconfigurations.crd.projectcalico.org             2022-03-15T10:42:01Z
globalnetworkpolicies.crd.projectcalico.org           2022-03-15T10:42:01Z
globalnetworksets.crd.projectcalico.org               2022-03-15T10:42:01Z
hostendpoints.crd.projectcalico.org                   2022-03-15T10:42:01Z
ipamblocks.crd.projectcalico.org                      2022-03-15T10:42:01Z
ipamconfigs.crd.projectcalico.org                     2022-03-15T10:42:01Z
ipamhandles.crd.projectcalico.org                     2022-03-15T10:42:01Z
ippools.crd.projectcalico.org                         2022-03-15T10:42:01Z
ipreservations.crd.projectcalico.org                  2022-03-15T10:42:01Z
kubecontrollersconfigurations.crd.projectcalico.org   2022-03-15T10:42:01Z
networkpolicies.crd.projectcalico.org                 2022-03-15T10:42:01Z
networksets.crd.projectcalico.org                     2022-03-15T10:42:01Z
rabbitmqclusters.rabbitmq.com                         2022-03-15T10:55:48Z



$ kubectl get all -l app.kubernetes.io/name=rmq
NAME               READY   STATUS    RESTARTS       AGE
pod/rmq-server-0   1/1     Running   1 (157m ago)   157m
pod/rmq-server-1   1/1     Running   1 (148m ago)   148m
pod/rmq-server-2   1/1     Running   1 (151m ago)   151m

NAME                TYPE           CLUSTER-IP   EXTERNAL-IP    PORT(S)                                          AGE
service/rmq         LoadBalancer   10.32.0.20   192.168.1.84   5672:30988/TCP,15672:30105/TCP,15692:30955/TCP   12h
service/rmq-nodes   ClusterIP      None         <none>         4369/TCP,25672/TCP                               12h

NAME                          READY   AGE
statefulset.apps/rmq-server   3/3     12h


