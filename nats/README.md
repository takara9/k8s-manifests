# NATS

~~~
kubectl create ns nats
kubectl config set-context nats --namespace=nats --cluster=kubernetes --user=admin
kubectl config use-context nats
kubectl config get-contexts
~~~



$ kubectl get sc
NAME                   PROVISIONER           RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
csi-cephfs-sc          cephfs.csi.ceph.com   Delete          Immediate           true                   24h
csi-rbd-sc (default)   rbd.csi.ceph.com      Delete          Immediate           true                   24h

$ helm repo add nats https://nats-io.github.io/k8s/helm/charts/
"nats" has been added to your repositories

$ helm install my-nats nats/nats
NAME: my-nats
LAST DEPLOYED: Sat Feb 12 13:41:22 2022
NAMESPACE: nats
STATUS: deployed
REVISION: 1
NOTES:
You can find more information about running NATS on Kubernetes
in the NATS documentation website:

  https://docs.nats.io/nats-on-kubernetes/nats-kubernetes

NATS Box has been deployed into your cluster, you can
now use the NATS tools within the container as follows:

  kubectl exec -n nats -it deployment/my-nats-box -- /bin/sh -l

  nats-box:~# nats-sub test &
  nats-box:~# nats-pub test hi
  nats-box:~# nc my-nats 4222

Thanks for using NATS!

~~~