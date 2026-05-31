pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          bat 'docker build -t %USER%/kubewise-backend:latest ./backend'
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          bat 'docker login -u %USER% -p %PASS%'
          bat 'docker push %USER%/kubewise-backend:latest'
        }
      }
    }

    stage('Load into Kind') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          bat 'kind load docker-image %USER%/kubewise-backend:latest --name kubewise'
        }
      }
    }

    stage('Helm Deploy') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          bat 'helm upgrade kubewise D:\\kubewise\\kubewise-chart --set image.repository=%USER%/kubewise-backend --set image.pullPolicy=Always'
        }
      }
    }

    stage('Verify Deployment') {
      steps {
        bat 'kubectl rollout status deployment/kubewise-backend'
      }
    }
  }

  post {
    success {
      echo 'KubeWise deployed successfully!'
    }
    failure {
      echo 'Pipeline failed - check logs'
    }
  }
}
