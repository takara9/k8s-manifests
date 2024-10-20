# How to setup ArgoCD

https://argo-cd.readthedocs.io/en/stable/getting_started/

kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'


$ k get svc -n argocd
NAME                                      TYPE           CLUSTER-IP       EXTERNAL-IP    PORT(S)                      AGE
argocd-applicationset-controller          ClusterIP      10.102.82.217    <none>         7000/TCP                     25s
argocd-dex-server                         ClusterIP      10.103.243.246   <none>         5556/TCP,5557/TCP,5558/TCP   25s
argocd-metrics                            ClusterIP      10.105.178.6     <none>         8082/TCP                     25s
argocd-notifications-controller-metrics   ClusterIP      10.108.121.34    <none>         9001/TCP                     25s
argocd-redis                              ClusterIP      10.101.194.137   <none>         6379/TCP                     25s
argocd-repo-server                        ClusterIP      10.107.71.53     <none>         8081/TCP,8084/TCP            25s
argocd-server                             LoadBalancer   10.100.3.215     192.168.1.87   80:30197/TCP,443:31636/TCP   25s
argocd-server-metrics                     ClusterIP      10.109.6.160     <none>         8083/TCP                     24s


https://argocd-server.argocd.k8s1.labo.local


kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo