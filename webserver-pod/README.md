# Pad サンプルコード

このコードは、ポッドをコントローラー抜きでサービスのセレクターとマッチさせて公開するサンプルコードです。

コントローラーが入っていないので、ポッドを削除すると、復活する事はありません。


## 準備

テスト用に専用の名前空間を作成

~~~
kubectl create ns apl-pod-test
kubectl config set-context apl-pod --namespace=apl-pod-test --cluster=kubernetes --user=admin
kubectl config use-context apl-pod
kubectl config get-contexts
~~


使用法

~~~
kubectl apply -f pod.yaml
~~~


