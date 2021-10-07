pipeline {

  environment {
    PROJECT_DIR = "/app"
    REGISTRY = "greengiant77/calc_api" + ":" + "$BUILD_NUMBER"
    DOCKER_CREDENTIALS = "docker_auth"
    DOCKER_IMAGE = ""
  }

  agent any

  options {
    skipStagesAfterUnstable()
  }

  stages {
    stage('Cloning the code from Git') {
      steps {
        git branch: 'main',
        url: 'https://github.com/GScabbage/secure_rest_api'
      }
    }

    stage('Build Image') {
      steps {
        script {
          DOCKER_IMAGE = docker.build REGISTRY
        }
      }
    }

    stage('Deploy to Docker Hub') {
      steps {
        script {
          docker.withRegistry('', DOCKER_CREDENTIALS){
            DOCKER_IMAGE.push()
          }
        }
      }
    }

    stage('Purging Docker Image') {
      steps {
        sh "docker rmi $REGISTRY"
      }
    }
  }

}
