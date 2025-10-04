pipeline {
    agent any

    environment {
        // Adjust these IDs/paths if your setup differs
        GIT_CRED_ID   = 'github-credentiales'        // your GitHub credential id
        DOCKER_CRED_ID= 'dockerhub-password'     // your Docker Hub credential id (username/password)
        IMAGE_NAME    = 'pavanbandi07/flask-app'
        IMAGE_TAG     = 'latest'
        PYTHON_BIN    = 'C:\\Users\\goudp\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out repository..."
                git url: 'https://github.com/PavanBand/Flask-ci-cd.git', branch: 'main', credentialsId: "${env.GIT_CRED_ID}"
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                dir('flask-ci-cd') {
                    bat "\"${PYTHON_BIN}\" -m pip install --upgrade pip"
                    bat "\"${PYTHON_BIN}\" -m pip install -r requirements.txt"
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running unit tests (capture output and status)..."
                dir('flask-ci-cd') {
                    script {
                        def cmd = "\"${PYTHON_BIN}\" -m unittest discover -s tests -p \"*.py\""

                        // 1) run and get status (so non-zero won't auto-fail)
                        def rc = bat(script: cmd, returnStatus: true)

                        // 2) capture stdout for diagnosis (run again to get output)
                        def out = bat(script: cmd, returnStdout: true).trim()

                        echo "unittest exit code: ${rc}"
                        echo "---- unittest output start ----"
                        echo out
                        echo "---- unittest output end ----"

                        // Decision logic:
                        if (out.contains("NO TESTS RAN") || out =~ /Ran 0 tests/) {
                            echo "No tests detected — continuing pipeline."
                        } else if (rc == 0) {
                            echo "Tests passed."
                        } else {
                            // any other non-zero + not 'no tests' -> fail
                            error "Unit tests failed (exit code ${rc}). See output above."
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                dir('flask-ci-cd') {
                    bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Logging in to Docker Hub and pushing image..."
                withCredentials([usernamePassword(credentialsId: "${env.DOCKER_CRED_ID}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PSW')]) {
                    // login
                    bat "docker login -u %DOCKER_USER% -p %DOCKER_PSW%"
                    bat "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Deploy Locally') {
            steps {
                echo "Deploying container locally (stop/remove old if present)..."
                dir('flask-ci-cd') {
                    bat "docker stop flask-app || echo 'no running container to stop'"
                    bat "docker rm flask-app || echo 'no container to remove'"
                    bat "docker run -d -p 5000:5000 --name flask-app ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
    }

    post {
        success { echo "Pipeline succeeded." }
        failure { echo "Pipeline failed — check console output for details." }
    }
}
