pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials') // Your Docker Hub credentials in Jenkins
    } 

    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running unit tests...'
                bat 'pytest tests\\'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                bat 'docker build -t flask-app:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                bat """
                docker login -u %DOCKERHUB_USERNAME% -p %DOCKERHUB_PASSWORD%
                docker tag flask-app:latest yourdockerhubusername/flask-app:latest
                docker push yourdockerhubusername/flask-app:latest
                """
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deployment step placeholder...'
                // Add your deployment commands here (e.g., docker run, ECS task, etc.)
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the console output for errors.'
        }
    }
}
