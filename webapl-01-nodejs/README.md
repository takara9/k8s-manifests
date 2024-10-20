# webapl-1

## 概要

挿絵の入ったウェブページを返すだけのシンプルなアプリケーションです。

1. コンテナのビルド
1. プライベート コンテナレジストリサービスへの登録
1. パブリック コンテナレジストリサービスへの登録
1. コードリポジトリ パブリックGitHubから、プライベートGitLabへ登録
1. パブリック GitHub へもPushする方法
1. 両方のコードリポジトリへ反映させる場合
1. Kubernetesへデプロイする方法


## リンク情報

* GitHubリポジトリ: https://github.com/takara9/webapl-1
* サブモジュールリンク: https://github.com/takara9/marmot-k8s/tree/master/manifests/webapl-01-nodejs

marmot-k8sをクローンした後に、サブモジュールの更新するには、'git submodule update -i'を実行する。



## コンテナのビルド方法

~~~
docker build -t webapl1:1.0 .
~~~

## ローカル環境でのテストやデバッグ

~~~
docker run -it -p 3000:3000 --rm --name test webapl1:1.0
~~~


## Harbor のコンテナレジストリへ登録

harborレジストリへのdocker login は、毎回実施する必要は無いので、省略可能できます。
docker imagesコマンドも、対象となるイメージの存在を確認するためなので、省略可能です。
タグの付与は、登録対象のレジストリごとに必要です。

~~~
docker login -u tkr harbor.labo.local
docker images
docker tag webapl1:1.0 harbor.labo.local/tkr/webapl1:1.0
docker push harbor.labo.local/tkr/webapl1:1.0
~~~

docker login で harborレジストリへログインする場合、harborのサイト証明書を署名した
認証局（CA)の証明書が、macOSのキーチェーンに登録され、Docker Desktopが再起動されて
いる必要があります。これが実施されていないと docker login は、以下のエラーを表示して
ログインは失敗します。

~~~
Error response from daemon: Get https://harbor.labo.local/v2/: x509: certificate signed by unknown authority
~~~





## Docker Hub レジストリサービスへ登録

Docker Hubへ登録するときは、サーバー名は省略可能で、ユーザー名だけで指定できます。
もちろん、アカウントを持っていなければなりません。

~~~
docker tag webapl1:1.0 maho/webapl1:1.0
docker push maho/webapl1:1.0
~~~




## パブリック GitHub からクローンして、プライベート GitLab へプッシュする方法

git コマンドで、ローカルのGitLabにアクセスできる設定を実施しておく。
それから、以下を実施することで、ローカルのGitLabを利用できる。

~~~
git clone https://github.com/takara9/webapl-1
cd webapl-1

git remote -v
origin	ssh://git@github.com/takara9/webapl-1 (fetch)
origin	ssh://git@github.com/takara9/webapl-1 (push)

git remote rename origin old-origin
git remote -v
old-origin	ssh://git@github.com/takara9/webapl-1 (fetch)
old-origin	ssh://git@github.com/takara9/webapl-1 (push)

git remote add origin ssh://git@gitlab.labo.local:2224/tkr/webapl-1.git
git push -u origin --all
~~~


## パブリック GitHub へもPushする方法

ローカルだけではなく、パブリックGitHubへ変更を反映するには、old-origin へプッシュすれば良い

~~~
git push -u old-origin

git remote -v
old-origin	https://github.com/takara9/webapl-1 (fetch)
old-origin	https://github.com/takara9/webapl-1 (push)
origin	ssh://git@gitlab.labo.local:2224/tkr/webapl-1.git (fetch)
origin	ssh://git@gitlab.labo.local:2224/tkr/webapl-1.git (push)
~~~


## 全てに反映させる場合

~~~
cd webapl-1
git status
git add README.md 
git commit -m "update "
git push -u origin --all
git push -u old-origin --all
~~~


## Kubernetesへデプロイする方法

デプロイ後に、service/webapl1 列の EXTERNAL-IPにアクセスすることで、ウェブページへアクセスできる。



~~~
cd webapl-1/k8s-yaml

kubectl apply -f webapl1.yaml


kubectl get all
NAME                           READY   STATUS    RESTARTS   AGE
pod/webapl1-768f6779cf-x2xx5   1/1     Running   0          6m28s

NAME                 TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)        AGE
service/kubernetes   ClusterIP      10.32.0.1     <none>          443/TCP        15h
service/webapl1      LoadBalancer   10.32.0.233   192.168.1.183   80:31525/TCP   6m28s

NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/webapl1   1/1     1            1           6m28s

NAME                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/webapl1-768f6779cf   1         1         1       6m28s
~~~



## プライベートレジストリに登録、K8sへのデプロイ

プライベートプロジェクトのタグを付与して、レジストリへ登録する。

~~~
docker tag webapl1:1.0 harbor.labo.local/x/webapl1:1.0
docker push harbor.labo.local/x/webapl1:1.0
~~~

アクセスに必要なシークレットを設定する。

~~~
kubectl create secret docker-registry regcred --docker-server=harbor.labo.local --docker-username=tkr --docker-password='***********' --docker-email='tkr@labo.local'
~~~

レジストリのクレデンシャル情報を追加したYAMLを適用する。

~~~
cd k8s-yaml
kubectl apply -f webapl1-private.yaml
~~~

## Jenkins,GitLab,Harborの連動

Jenkinsでジョブをスタートすると、GitLabからクローンして、コンテナをビルド、Harborへプッシュ、続いて、K8sへデプロイする。仕掛けを作成する。

Jenkinsのブラウザ画面 https://jenkins.labo.local/ にログインする。


Jenkinsの管理 -> プラグインマネージャー -> 利用可能 -> GitLab をサーチ
GitLabプラグインをインストールして、Jenkins再起動を選択


新規ジョブ作成
名前 webapl-1
パイプライン

https://gitlab.labo.local/tkr/webapl-1



