pipeline {
    agent any

 environment {
    PYTHON = "C:\\Users\\goudp\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
    DOCKERHUB = credentials('dockerhub-credentials')
}


    stages {
        stage('Checkout SCM') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/PavanBand/Flask-ci-cd.git',
                        credentialsId: 'github-credentials'
                    ]]
                ])
            }
        }

stage('Install Dependencies') {
    steps {
        echo "Installing Python dependencies..."
        dir('flask-ci-cd') {
            bat "C:\\Users\\goudp\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -m pip install --upgrade pip"
            bat "C:\\Users\\goudp\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -m pip install -r requirements.txt"
        }
    }
}


        stage('Run Tests') {
            steps {
                echo 'Running Tests...'
                bat "${env.PYTHON} -m unittest discover"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                bat "docker build -t ${DOCKERHUB_USR}/flask-ci-cd:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                bat "docker login -u ${DOCKERHUB_USR} -p ${DOCKERHUB_PSW}"
                bat "docker push ${DOCKERHUB_USR}/flask-ci-cd:latest"
            }
        }

        stage('Deploy Locally') {
            steps {
                echo 'Deploying locally...'
                bat "docker run -d -p 5000:5000 ${DOCKERHUB_USR}/flask-ci-cd:latest"
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
