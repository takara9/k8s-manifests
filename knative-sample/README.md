# Knative サービングのテスト

Knatvieに

~~~
$ kn service create helloworld-go --image gcr.io/knative-samples/helloworld-go --env TARGET="Go Sample v1"
~~~


~~~
$ kn service list
NAME            URL                                            LATEST                  AGE     CONDITIONS   READY   REASON
helloworld-go   http://helloworld-go.default.k8s1.labo.local   helloworld-go-dhvjj-1   2m37s   3 OK / 3     True    
~~~


~~~
$ kn service describe helloworld-go
Name:       helloworld-go
Namespace:  default
Age:        29s
URL:        http://helloworld-go.default.k8s1.labo.local

Revisions:  
  100%  @latest (helloworld-go-rgngf-1) [1] (29s)
        Image:  gcr.io/knative-samples/helloworld-go (pinned to 5ea96b)

Conditions:  
  OK TYPE                   AGE REASON
  ++ Ready                  20s 
  ++ ConfigurationsReady    20s 
  ++ RoutesReady            20s
~~~



~~~
$ hey -n 10000 -c 1000 http://helloworld-go.default.k8s1.labo.local

Summary:
  Total:	4.9033 secs
  Slowest:	2.6807 secs
  Fastest:	0.0042 secs
  Average:	0.4684 secs
  Requests/sec:	2039.4575
  
  Total data:	200000 bytes
  Size/request:	20 bytes

Response time histogram:
  0.004 [1]	|
  0.272 [5346]	|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.539 [3590]	|■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.807 [63]	|
  1.075 [0]	|
  1.342 [0]	|
  1.610 [0]	|
  1.878 [0]	|
  2.145 [0]	|
  2.413 [424]	|■■■
  2.681 [576]	|■■■■


Latency distribution:
  10% in 0.1106 secs
  25% in 0.1911 secs
  50% in 0.2622 secs
  75% in 0.3459 secs
  90% in 2.1693 secs
  95% in 2.4406 secs
  99% in 2.5632 secs

Details (average, fastest, slowest):
  DNS+dialup:	0.0237 secs, 0.0042 secs, 2.6807 secs
  DNS-lookup:	0.0122 secs, 0.0000 secs, 0.1265 secs
  req write:	0.0000 secs, 0.0000 secs, 0.0020 secs
  resp wait:	0.4438 secs, 0.0040 secs, 2.5041 secs
  resp read:	0.0002 secs, 0.0000 secs, 0.0600 secs

Status code distribution:
  [200]	10000 responses
~~~



~~~
kn service delete helloworld-go
~~~

