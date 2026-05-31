content = """pipeline {
  agent any

  environment {
    IMAGE_NAME = "DOCKER_PLACEHOLDER/kubewise-backend:latest"
  }

  stages {
    stage("Checkout") {
      steps {
        checkout scm
      }
    }

    stage("Build Docker Image") {
      steps {
        withCredentials([usernamePassword(credentialsId: "dockerhub-creds", usernameVariable: "DOCKER_USER", passwordVariable: "DOCKER_PASS")]) {
          sh "docker build -t ${IMAGE_NAME} ./backend"
        }
      }
    }

    stage("Push to Docker Hub") {
      steps {
        withCredentials([usernamePassword(credentialsId: "dockerhub-creds", usernameVariable: "DOCKER_USER", passwordVariable: "DOCKER_PASS")]) {
          sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
          sh "docker push ${IMAGE_NAME}"
        }
      }
    }

    stage("Load into Kind") {
      steps {
        sh "kind load docker-image ${IMAGE_NAME} --name kubewise"
      }
    }

    stage("Helm Deploy") {
      steps {
        withCredentials([usernamePassword(credentialsId: "dockerhub-creds", usernameVariable: "DOCKER_USER", passwordVariable: "DOCKER_PASS")]) {
          sh "helm upgrade --install kubewise ./kubewise-chart --set image.repository=$DOCKER_USER/kubewise-backend --set image.tag=latest --set image.pullPolicy=Always"
        }
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
"""

with open("Jenkinsfile", "w", newline="\n") as f:
    f.write(content)

print("Done - Jenkinsfile written cleanly")
