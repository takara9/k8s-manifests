pipeline {

  environment {
    registry = "harbor.labo.local/tkr/webapl1"
    dockerImage = ""
    KUBECONFIG = credentials('kubeconfig')    
  }

  agent any
  stages {
    stage("test") {
      steps {
              sh 'ls -al'
              sh 'env'
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
          sh 'sed s/__BUILDNUMBER__/$BUILD_NUMBER/ webapl1.yaml > webapl1-build.yaml'
          sh 'kubectl apply -f webapl1-build.yaml --kubeconfig $KUBECONFIG'
        }
      }
    }

  }

}

