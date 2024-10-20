# webapl-2

シンプルなPHP Webアプリケーション

## ローカルでビルドして実行する


~~~
docker build -t webapl2:1.0 .
docker run -it -p 8080:8080 --rm --name test webapl2:1.0
~~~

~~~
docker tag webapl2:1 harbor.labo.local/tkr/webapl2:1
docker push harbor.labo.local/tkr/webapl2:1
~~~


## Jenkinsパイプラインの自動実行

Jenkinsから変更をポーリングして変更を検知してジョブを実行する方法と
git push を実行したタイミングでビルドのジョブが走る方法の二つの設定を記述する。
これらの設定をしなくても、Jenkinsの管理画面からパイプラインのジョブを実行できる。

### 自動実行のJenkins側の前提条件は以下
* Harbor が起動していること
* Harbor の CA証明書が JenkinsサーバーのLinuxにインポートされていること
* GitLab が起動していること
* GitLan の CA証明書が JenkinsサーバーのLinixにインポートされていること
* JenkinsにGitLab Plugin がインストールされていること
* Jenkins設定でGitLabのパラメーターが設定されていること。
   * Connection name
   * Gitlab host URL
   * Credentials
   * Test Connection が成功すること

### GitLab側の前提条件は以下
* rootでログインして、スパナマークのアイコン(Admin Area) の Setting -> Network -> Outbound requests -> Allow requests to the local network from web hooks and services にチェックが入っていること
* Jenkingと連携するユーザーでログインして、Settings -> Webhooks に設定がされていること。
   1. URL に Jenkins プロジェクトのURL
   1. 秘密トークンに、Jenkins のプロジェクト、ビルドトリガーの高度な設定で生成したSercret Tokenがセットされていること。
   1. SSL証明書検証の有効化のチェックが外されていること（無効になっていること）
   1. テストボタンをクリックして、連携が成功すること


### GitLabリポジトリを5分間隔でポーリングして変更があった場合にビルドを実行する

1.「新規ジョブ作成」をクリック
1. ジョブの名前（日本語でもOK)をインプット
1. 全体のタブ
    1. GitLab Connection にコネクション名をセット（事前登録必要）
    1. GitLab Repository Name にリポジトリ名をセット
1. ビルドトリガのタブをクリック、
    1. SCMをポーリングにチェック
    1. "H/5 * * * *" をインプット 毎時*5分でポーリング
1. パイプラインのタブをクリック
    1. Pipeline script from SCMを選択
    1. SCM: Git を選択
        1. リポジトリURL: https://gitlab.labo.local/tkr/webapl-2.git
        1. 認証情報: https://gitlab.labo.local/　のユーザーID/パスワードを追加して選択
        1. ビルドするブランチ "*/master" -> "*/main"へ変更
    1. Script Path:  Jenkinsfile
1. 「保存」をクリック



### GitLabへpushされた時に、ビルドを実行する設定

1.「新規ジョブ作成」をクリック
1. ジョブの名前（日本語でもOK)をインプット
1. 全体のタブ
    1. GitLab Connection にコネクション名をセット（事前登録必要）
    1. GitLab Repository Name にリポジトリ名をセット
1. ビルドトリガのタブをクリック
    1. Build when a change is pushed to GitLab. GitLab webhook にチェック
    1. Enabled GitLab triggersのPush Eventsにチェック
    1. Rebuild open Merge Requests で On push to source brance を選択
    1. 高度な設定をクリック
        1. Secret token をクリック
        1. Generate クリックして、トークンを生成
1. パイプラインのタブをクリック
    1. Pipeline script from SCMを選択
    1. SCM: Git を選択
        1. リポジトリURL: https://gitlab.labo.local/tkr/webapl-2.git
        1. 認証情報: https://gitlab.labo.local/　のユーザーID/パスワードを追加して選択
        1. ビルドするブランチ "*/master" -> "*/main"へ変更
    1. Script Path:  Jenkinsfile
1. 「保存」をクリック






 　　
  



