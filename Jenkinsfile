pipeline {
    agent any

    environment {
        // Docker Hub credentials stored in Jenkins
        DOCKERHUB = credentials('dockerhub-credentials')
        IMAGE_NAME = 'flask-app'
        DOCKER_USERNAME = 'pavanbandi07'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                bat 'C:\Users\Pavan\AppData\Local\Microsoft\WindowsApps\python.exe -r requirements.txt'
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
                bat """
                docker build -t %IMAGE_NAME%:latest .
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Logging in to Docker Hub and pushing image...'
                bat """
                docker login -u %DOCKER_USERNAME% -p %DOCKERHUB_PSW%
                docker tag %IMAGE_NAME%:latest %DOCKER_USERNAME%/%IMAGE_NAME%:latest
                docker push %DOCKER_USERNAME%/%IMAGE_NAME%:latest
                """
            }
        }

        stage('Deploy Locally') {
            steps {
                echo 'Running Docker container locally...'
                bat """
                docker stop %IMAGE_NAME% || echo Container not running
                docker rm %IMAGE_NAME% || echo Container removed
                docker run -d -p 5000:5000 --name %IMAGE_NAME% %DOCKER_USERNAME%/%IMAGE_NAME%:latest
                """
            }
        }
    }

    post {
        success { echo 'Pipeline completed successfully!' }
        failure { echo 'Pipeline failed. Check console output for errors.' }
    }
}
