pipeline {
    agent any

    environment {
        GIT_CRED_ID    = 'github-credentials'        // update if your GitHub credential ID differs
        DOCKER_CRED_ID = 'dockerhub-credentials'     // must match Jenkins credential ID you created
        IMAGE_NAME     = 'pavanbandi07/flask-app'
        IMAGE_TAG      = 'latest'
        PYTHON_BIN     = 'C:\\Users\\goudp\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
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
                echo "Running unit tests (capture output + exit code)..."
                dir('flask-ci-cd') {
                    script {
                        bat script: 'if exist test_output.txt del test_output.txt', returnStatus: true

                        // Run tests and append the return code to the same file
                        bat script: "cmd /c \"\"${PYTHON_BIN}\" -m unittest discover -s tests -p \"*.py\" > test_output.txt 2>&1 || (echo RETURNED:%ERRORLEVEL% >> test_output.txt)\""

                        def out = readFile('test_output.txt').trim()
                        echo "---- unittest output start ----"
                        echo out
                        echo "---- unittest output end ----"

                        def rc = 0
                        def m = out =~ /RETURNED:(\d+)/
                        if (m) { rc = (m[0][1] as Integer) }

                        if (out.contains('Ran 0 tests') || out.contains('NO TESTS RAN')) {
                            echo "No tests found — continuing."
                        } else if (rc == 0) {
                            echo "Tests passed."
                        } else {
                            error "Unit tests failed (exit ${rc})."
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
                echo "Login to Docker Hub and push image..."
                withCredentials([usernamePassword(credentialsId: "${env.DOCKER_CRED_ID}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PSW')]) {
                    // Login (masked)
                    bat "docker login -u %DOCKER_USER% -p %DOCKER_PSW%"
                    bat "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Deploy Locally') {
            steps {
                echo "Deploying container locally (stop/remove old if present)..."
                dir('flask-ci-cd') {
                    script {
                        // stop if running (capture non-zero and continue)
                        def stopRc = bat(script: 'docker stop flask-app', returnStatus: true)
                        if (stopRc != 0) {
                            echo "No running container to stop (exit ${stopRc}). Continuing..."
                        } else {
                            echo "Stopped existing container."
                        }

                        // remove if exists (capture non-zero and continue)
                        def rmRc = bat(script: 'docker rm flask-app', returnStatus: true)
                        if (rmRc != 0) {
                            echo "No container to remove (exit ${rmRc}). Continuing..."
                        } else {
                            echo "Removed existing container."
                        }

                        // run the container (this should error/exit non-zero if docker daemon problems exist)
                        def runRc = bat(script: "docker run -d -p 5000:5000 --name flask-app ${IMAGE_NAME}:${IMAGE_TAG}", returnStatus: true)
                        if (runRc != 0) {
                            error "Failed to start container (docker run exit ${runRc})."
                        } else {
                            echo "Container started successfully."
                        }
                    }
                }
            }
        }
    }

    post {
        success { echo "Pipeline completed successfully." }
        failure { echo "Pipeline FAILED — check console output for details." }
    }
}
