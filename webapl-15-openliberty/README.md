# OpenLiberty microprofile のサンプルプログラム

OpenLibery の MicroProfile で作った REST-API の Javaプログラムについて
以下を実行する。

* Eclipseへのインポート
* mavenでビルドとテスト、コンテナのビルド
* Kubernetesへのデプロイ
* JenkinsのCICDパイプラインの設定


## Eclipseのプロジェクトにインポート

ターミナルから、ワークスペース用のディレクトリを作成して移動、git clone する。

~~~
mkdir workspace-liberty
cd workspace-liberty
git clone ssh://git@gitlab.labo.local:2224/tkr/web-apl-openliberty.git
cd web-apl-openliberty
~~~

Eclipseの起動時に、上記で作成した workspace-liberty を指定して起動する。

Eclipse の表示画面から以下の操作により、Mavenbプロジェクトをインポートする。

1. Package Explorer -> Import Project -> Maven -> Existing Maven Projects
2. Next をクリック
3. Root Directory に web-apl-openliberty を指定
4. Finish をクリック




## Mavenコマンドを使った操作

Liberty microprofile を使ったJavaソースからのwarビルド

~~~
mvn package
~~~


ビルドの生成物つまりtarget以下を消去する。

~~~
mvn clean
~~~


ローカルでのテスト用に、開発用サーバー(Liberty)でサーブレット起動

~~~
mvn liberty:dev
~~~


コンテナ内でJavaアプリを起動する。

~~~
mvn liberty:devc
~~~




## Dockerコマンドを利用した操作 


コンテナのビルドには、Dockerfileの存在するフォルダで以下を実行する。

~~~
docker build -t maho/webapl-9:0.2 .
~~~

DockerHubへ登録する。

~~~
docker push maho/webapl-9:0.2 
~~~

コンテナの単体テスト

~~~
docker run -it --rm --name test -p 9080:9080 maho/webapl-9:0.2
~~~


## コンテナやmavenでのアクセステスト

curlで以下のURLをアクセスする

* http://localhost:9080/rest/system/properties/ Liberyのプロパティ
* http://localhost:9080/rest/system/personList/ リストJSON
* http://localhost:9080/rest/system/person/ 個別JSON
* http://localhost:9080/health/ ヘルスチェック
* http://localhost:9080/health/ready　レディネス（準備状態）
* http://localhost:9080/health/live　ライブネス（稼働状態）
* http://localhost:9080/metrics/　メトリクス


プロパティの取得例

~~~
$ curl -s http://localhost:9080/rest/system/properties|jq
{
  "osgi.checkConfiguration": "false",
  "awt.toolkit": "sun.awt.X11.XToolkit",
  "file.encoding.pkg": "sun.io",
  "java.specification.version": "11",
  "jdk.extensions.version": "11.0.12.0",
~~~



## Kubernetesデプロイ

専用の名前空間を作成する設定

~~~
kubectl create ns liberty9
kubectl config set-context liberty9 --namespace=liberty9 --cluster=kubernetes --user=admin
kubectl config use-context liberty9
kubectl config get-contexts
~~~

YAMLファイルはJenkinsfile用に設定されているので、21行目をコメントにする。
22行目のコメントマークを削除して有効化

~~~
    18	    spec:
    19	      containers:
    20	      - name: webjava
    21	        image: harbor.labo.local/tkr/web-apl-openliberty:__BUILDNUMBER__        
    22	        #image: maho/webapl-9:0.2
    23	        ports:
~~~


コンテナレジストリに、コンテナイメージが登録されている状態で、以下を実行する。

~~~
kubectl apply -f k8s-yaml/deploy.yaml
~~~

Readiness Probe が UPになるまで30秒かかるので、その後、アクセスできるようになる。



## Jenkinsの新規ジョブ作成

Jenkinsのダッシュボード画面から、Gitクローン、ビルド、デプロイまでを自動化する。


### Kubernetesクラスタの認証情報を登録

Kuberneteへデプロイするために上記で設定したkubeconfigファイルをJenkinsに登録する。
この設定は、以下のJenkinsfileで設定されている。

~~~
    KUBECONFIG = credentials('admin.kubeconfig-k8s1-liberty9')
~~~

登録方法は、
ダッシュボード -> Jenkinsの管理 -> Manage Credentials -> Stores scoped to Jenkins -> Domains (global) -> 認証情報の追加

* 種類: Secret file 
* スコープ: グローバル
* File: kubeconfigファイルを選択
* ID: Jenkinsfileから指定するキーワードを指定する（上記参照）



### ソースコードリポジトリ(GitLab)の認証情報登録

ジョブの設定から参照する。

ダッシュボード -> Jenkinsの管理 -> Manage Credentials -> Stores scoped to Jenkins -> Domains (global) -> 認証情報の追加

* 種類: ユーザー名とパスワード
* スコープ: グローバル
* ユーザー名: GitLabのユーザーID
* パスワード: 同パスワード
* ID: 識別用の文字列
* 説明: 後で解らなくならないように、記述しておく。



### コンテナレジストリ(Harbor)の認証情報登録

下記Jenkinsfile の中から参照する。49行目の"harbor"が認証情報を登録する。

~~~
    46	    stage('コンテナレジストリへプッシュ') {
    47	      steps {
    48	        script {
    49	          docker.withRegistry("https://harbor.labo.local","harbor") {
    50	            dockerImage.push()
    51	          }
    52	        }
    53	      }
    54	    }
~~~


ダッシュボード -> Jenkinsの管理 -> Manage Credentials -> Stores scoped to Jenkins -> Domains (global) -> 認証情報の追加

* 種類: ユーザー名とパスワード
* スコープ: グローバル
* ユーザー名: HarborのユーザーID
* パスワード: 同パスワード
* ID: 識別用の文字列（上記49行目 "harbor"）
* 説明: 後で解らなくならないように、記述しておく。




### Jenkinsのジョブ登録


設定手順は、
ダッシュボード -> 新規ジョブ作成 ->  ジョブ名をインプット -> パイプライン -> OKクリック

GitLab Connectionに GitLab-Localが設定されていることを確認
もしなければ、プラグインを確認する。

* パイプラインの定義を"Pipeline script from SCM"を設定
* SCM に Git を選択
* リポジトリURLに GitLabのアドレスを設定する。
　　https://gitlab.labo.local/tkr/web-apl-openliberty
* 認証情報に GitLab のユーザーIDとパスワードを設定
* ビルドするブランチに "*/main" を設定
* Script Path に Jenkinsfile を設定する。
* 最後に保存をクリック

上記の操作で、準備が出来たので、ダッシュボードから登録したジョブを指定して、
ビルド実行をクリックする。





