pipeline {
    agent any

    environment {
        // Docker Hub credentials
        DOCKERHUB_CRED = credentials('dockerhub-password')
        IMAGE_NAME = "pavanbandi07/flask-ci-cd"
        PYTHON_PATH = "C:\\Users\\goudp\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo "Checking out from GitHub..."
                git url: 'https://github.com/PavanBand/Flask-ci-cd.git', branch: 'main', credentialsId: 'github-credentials'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                bat "${env.PYTHON_PATH} -m pip install --upgrade pip"
                bat "${env.PYTHON_PATH} -m pip install -r requirements.txt"
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running unit tests..."
                // Make sure you are in the correct directory
                dir('flask-ci-cd') {
                    bat "${env.PYTHON_PATH} -m unittest discover -s tests -p '*.py'"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                bat "docker build -t ${env.IMAGE_NAME}:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Logging in and pushing to Docker Hub..."
                bat "docker login -u ${env.DOCKERHUB_CRED_USR} -p ${env.DOCKERHUB_CRED_PSW}"
                bat "docker push ${env.IMAGE_NAME}:latest"
            }
        }

        stage('Deploy Locally') {
            steps {
                echo "Running Docker container locally..."
                bat "docker run -d -p 5000:5000 ${env.IMAGE_NAME}:latest"
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
        failure {
            echo "Pipeline failed. Check logs for details."
        }
        success {
            echo "Pipeline succeeded!"
        }
    }
}
