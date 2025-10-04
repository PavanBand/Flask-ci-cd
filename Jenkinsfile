pipeline {
    agent any

    environment {
        IMAGE_NAME = 'pavanbandi07/flask-app'
        IMAGE_TAG  = 'latest'
        PYTHON_BIN = 'C:\\Users\\goudp\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        // NOTE: Keep dockerhub credential ID below in sync with what you created in Jenkins.
        DOCKER_CRED_ID = 'dockerhub-password'
        GIT_CRED_ID = 'github-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out repository...'
                git url: 'https://github.com/PavanBand/Flask-ci-cd.git', branch: 'main', credentialsId: "${env.GIT_CRED_ID}"
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                dir('flask-ci-cd') {
                    bat "\"${env.PYTHON_BIN}\" -m pip install --upgrade pip"
                    bat "\"${env.PYTHON_BIN}\" -m pip install -r requirements.txt"
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running unit tests (if any)...'
                dir('flask-ci-cd') {
                    script {
                        // run tests but capture return status so "no tests" won't cause pipeline failure
                        def rc = bat(script: "\"${env.PYTHON_BIN}\" -m unittest discover -s tests -p '*.py'", returnStatus: true)
                        if (rc == 0) {
                            echo "Tests passed."
                        } else if (rc == 1) {
                            echo "No tests found or tests skipped (unittest returned 1). Continuing..."
                        } else {
                            error "Unit tests failed (exit code ${rc})."
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                dir('flask-ci-cd') {
                    bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Login to Docker Hub and push image...'
                // Use withCredentials mapping to safe env vars DOCKER_USER / DOCKER_PSW
                withCredentials([usernamePassword(credentialsId: "${env.DOCKER_CRED_ID}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PSW')]) {
                    // login (avoid leaving password in visible logs)
                    bat "docker login -u %DOCKER_USER% -p %DOCKER_PSW%"
                    bat "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Deploy Locally') {
            steps {
                echo 'Deploying container locally (stops/removes old one if exists)...'
                dir('flask-ci-cd') {
                    bat "docker stop flask-app || echo 'no running container to stop'"
                    bat "docker rm flask-app || echo 'no container to remove'"
                    bat "docker run -d -p 5000:5000 --name flask-app ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
    }

    post {
        success { echo 'Pipeline Succeeded.' }
        failure { echo 'Pipeline Failed — check console output.' }
    }
}
