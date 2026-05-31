pipeline {
  agent any

  stages {
    stage("Checkout") {
      steps {
        checkout scm
      }
    }

    stage("Build Docker Image") {
      steps {
        withCredentials([usernamePassword(credentialsId: "dockerhub-creds", usernameVariable: "DOCKER_USER", passwordVariable: "DOCKER_PASS")]) {
          sh "docker build -t ${DOCKER_USER}/kubewise-backend:latest ./backend"
        }
      }
    }

    stage("Push to Docker Hub") {
      steps {
        withCredentials([usernamePassword(credentialsId: "dockerhub-creds", usernameVariable: "DOCKER_USER", passwordVariable: "DOCKER_PASS")]) {
          sh "docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}"
          sh "docker push ${DOCKER_USER}/kubewise-backend:latest"
        }
      }
    }

    stage("Helm Deploy") {
      steps {
        sh "helm upgrade --install kubewise ./kubewise-chart --set image.repository=sivashankari19/kubewise-backend --set image.tag=latest --set image.pullPolicy=Always"
      }
    }

    stage("Verify Deployment") {
      steps {
        sh "kubectl rollout status deployment/kubewise-backend"
      }
    }
  }

  post {
    success {
      echo "KubeWise deployed successfully!"
    }
    failure {
      echo "Pipeline failed - check logs"
    }
  }
}