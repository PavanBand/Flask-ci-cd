pipeline {
    agent any

    environment {
        DOCKER_USER = credentials('dockerhub-username')   // Jenkins credential ID for Docker username
        DOCKER_PSW  = credentials('dockerhub-password')   // Jenkins credential ID for Docker password
        IMAGE_NAME  = 'pavanbandi07/flask-app'
        IMAGE_TAG   = 'latest'
        PYTHON_BIN  = 'C:\\Users\\goudp\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
    }

    stages {

        stage('Checkout SCM') {
            steps {
                echo 'Checking out from GitHub...'
                git url: 'https://github.com/PavanBand/Flask-ci-cd.git', branch: 'main', credentialsId: 'github-credentiales'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                dir('flask-ci-cd') {
                    bat "${env.PYTHON_BIN} -m pip install --upgrade pip"
                    bat "${env.PYTHON_BIN} -m pip install -r requirements.txt"
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Tests...'
                dir('flask-ci-cd') {
                    script {
                        def status = bat(script: "${env.PYTHON_BIN} -m unittest discover -s tests -p '*.py'", returnStatus: true)
                        if (status != 0 && status != 1) {
                            error "Unit tests failed!"
                        } else if (status == 1) {
                            echo "No tests found, continuing..."
                        } else {
                            echo "Tests passed successfully!"
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
                echo 'Logging into Docker Hub and pushing image...'
                bat "docker login -u ${DOCKER_USER} -p ${DOCKER_PSW}"
                bat "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Deploy Locally') {
            steps {
                echo 'Deploying Flask app locally using Docker...'
                bat "docker stop flask-app || echo 'Container not running'"
                bat "docker rm flask-app || echo 'Container not found'"
                bat "docker run -d -p 5000:5000 --name flask-app ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check console output for details.'
        }
    }
}
