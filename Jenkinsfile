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
          sh 'docker build -t \/kubewise-backend:latest ./backend'
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          sh 'docker login -u \ -p \'
          sh 'docker push \/kubewise-backend:latest'
        }
      }
    }

    stage('Load into Kind') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          sh 'kind load docker-image \/kubewise-backend:latest --name kubewise'
        }
      }
    }

    stage('Helm Deploy') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          sh 'helm upgrade kubewise /var/jenkins_home/workspace/kubewise-pipeline/kubewise-chart --set image.repository=\/kubewise-backend --set image.pullPolicy=Always'
        }
      }
    }

    stage('Verify Deployment') {
      steps {
        sh 'kubectl rollout status deployment/kubewise-backend'
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
