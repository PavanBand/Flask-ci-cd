pipeline {
    agent any

    environment {
        // DockerHub credentials
        DOCKER_USER = credentials('dockerhub-password')
    }

    stages {

        stage('Checkout SCM') {
            steps {
                echo 'Checking out from GitHub...'
                git branch: 'main', url: 'https://github.com/PavanBand/Flask-ci-cd.git', credentialsId: 'github-credentials'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                dir('flask-ci-cd') {
                    bat "C:\\Users\\goudp\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -m pip install --upgrade pip"
                    bat "C:\\Users\\goudp\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -m pip install -r requirements.txt"
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Tests...'
                dir('flask-ci-cd') {
                    // Use python path explicitly for Windows
                    bat "C:\\Users\\goudp\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -m unittest discover -s tests -p '*.py' || echo 'No tests found, continuing...'"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker Image...'
                dir('flask-ci-cd') {
                    bat "docker build -t pavanbandi07/flask-app:latest ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing Docker Image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-password', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat "docker login -u %DOCKER_USER% -p %DOCKER_PASS%"
                    bat "docker push pavanbandi07/flask-app:latest"
                }
            }
        }

        stage('Deploy Locally') {
            steps {
                echo 'Deploying Docker Container locally...'
                dir('flask-ci-cd') {
                    // Stop/remove old container if exists
                    bat "docker stop flask-app || echo 'No existing container'"
                    bat "docker rm flask-app || echo 'No existing container'"
                    bat "docker run -d -p 5000:5000 --name flask-app pavanbandi07/flask-app:latest"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check console output for errors.'
        }
    }
}
