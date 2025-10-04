pipeline {
    agent any

    environment {
        GIT_CRED_ID    = 'github-credentials'        // adjust if different
        DOCKER_CRED_ID = 'dockerhub-credentials'     // must match Jenkins credential ID
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
                        // ensure no stale file
                        bat script: 'if exist test_output.txt del test_output.txt', returnStatus: true

                        // Run unittest once, capture output to test_output.txt, and ensure we append the ERRORLEVEL so we can read it.
                        // The nested cmd /c and quoting ensures it runs properly on Windows agents.
                        bat script: "cmd /c \"\"${PYTHON_BIN}\" -m unittest discover -s tests -p \"*.py\" > test_output.txt 2>&1 || (echo RETURNED:%ERRORLEVEL% >> test_output.txt)\""

                        // Read the file back
                        def out = readFile('test_output.txt').trim()
                        echo "---- unittest output start ----"
                        echo out
                        echo "---- unittest output end ----"

                        // Look for RETURNED:<code>
                        def rc = 0
                        def m = out =~ /RETURNED:(\\d+)/
                        if (m) {
                            rc = (m[0][1] as Integer)
                        } else {
                            // If not present, assume 0 (success) — but still check text for "Ran 0 tests"
                            rc = 0
                        }

                        // Decide what to do:
                        if (out.contains('Ran 0 tests') || out.contains('NO TESTS RAN')) {
                            echo "No tests were found. Continuing pipeline."
                        } else if (rc == 0) {
                            echo "Unit tests passed (exit 0)."
                        } else {
                            error "Unit tests failed with exit code ${rc}. See test_output.txt content above."
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
                    // use variables in Windows bat
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
        failure { echo "Pipeline failed. Check console output and test_output.txt for details." }
    }
}
