pipeline {
    agent any

    environment {
        PYTHON = "C:\\Users\\goudp\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
        DOCKERHUB = credentials('dockerhub-username')      // Replace with your Docker Hub credential ID
        DOCKERHUB_PSW = credentials('dockerhub-password')  // Replace with your Docker Hub password ID
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                bat "\"${env.PYTHON}\" -m pip install --upgrade pip"
                bat "\"${env.PYTHON}\" -m pip install -r requirements.txt"
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running Python Unit Tests..."
                // Use full Python path to avoid PATH issues
                bat "\"${env.PYTHON}\" -m unittest discover -s tests -p \"*.py\""
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image..."
                bat "docker build -t flask-ci-cd:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Logging into Docker Hub..."
                bat "docker login -u ${DOCKERHUB} -p ${DOCKERHUB_PSW}"
                bat "docker tag flask-ci-cd:latest ${DOCKERHUB}/flask-ci-cd:latest"
                bat "docker push ${DOCKERHUB}/flask-ci-cd:latest"
            }
        }

        stage('Deploy Locally') {
            steps {
                echo "Deploying locally using Docker..."
                bat "docker stop flask-ci-cd || echo No container to stop"
                bat "docker rm flask-ci-cd || echo No container to remove"
                bat "docker run -d -p 5000:5000 --name flask-ci-cd ${DOCKERHUB}/flask-ci-cd:latest"
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
        success {
            echo "Pipeline succeeded!"
        }
        failure {
            echo "Pipeline failed. Check logs for details."
        }
    }
}
