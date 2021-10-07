pipeline {

  environment {
    PROJECT_DIR = "/app"
    REGISTRY = "greengiant77/calc_api"
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
        git 'https://github.com/GScabbage/secure_rest_api'
      }
    }
  }

}
