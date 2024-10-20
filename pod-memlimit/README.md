# メモリ制限の注意

メモリのリソースリミットを以下に設定する。

~~~
      resources:
        requests:
          memory: "128Mi"
          cpu: "500m"
        limits:
          memory: "128Mi"
          cpu: "500m"
~~~

コンテナ内のコマンドが見えているメモリサイズを確認する。
つまり、コンテナ上のプロセスは、ワーカーノードのメモリサイズを見ている。

~~~
$ kubectl apply -f pod.yaml
pod/test-mem-limit created

$ kubectl get po test-mem-limit 
NAME             READY   STATUS    RESTARTS   AGE
test-mem-limit   1/1     Running   0          22s

$ kubectl exec -it test-mem-limit -- free -h
              total        used        free      shared  buff/cache   available
Mem:            15G        2.8G        5.6G        3.9M        7.3G         12G
Swap:            0B          0B          0B
~~~


参考資料:
* Kubernetes: Assign Memory Resources and Limits to Containers, https://www.alibabacloud.com/blog/kubernetes-assign-memory-resources-and-limits-to-containers_594830
* Sizing Kubernetes pods for JVM apps without fearing the OOM Killer, https://srvaroa.github.io/jvm/kubernetes/memory/docker/oomkiller/2019/05/29/k8s-and-java.html

