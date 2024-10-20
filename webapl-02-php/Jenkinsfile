pipeline {

  environment {
    registry = "harbor.labo.local/tkr/webapl2"
    dockerImage = ""
    KUBECONFIG = credentials('kubeconfig')    
  }

  agent any
  stages {

    stage('gitlab') {
      steps {
        echo 'Notify GitLab'
        updateGitlabCommitStatus name: 'build', state: 'pending'
        updateGitlabCommitStatus name: 'build', state: 'success'
      }
    }

    stage('コンテナイメージのビルド') {
      steps {
        script {
          dockerImage = docker.build registry + ":$BUILD_NUMBER"
        }
      }
    }
      
    stage('コンテナレジストリへプッシュ') {
      steps {
        script {
          docker.withRegistry("https://harbor.labo.local","harbor.labo.local") {
            dockerImage.push()
          }
        }
      }
    }

    stage('K8sクラスタへのデプロイ') {
      steps {
        script {
          sh 'kubectl cluster-info --kubeconfig $KUBECONFIG'
          sh 'sed s/__BUILDNUMBER__/$BUILD_NUMBER/ webapl2.yaml > webapl2-build.yaml'
          sh 'kubectl apply -f webapl2-build.yaml --kubeconfig $KUBECONFIG'
        }
      }
    }

  }

}

