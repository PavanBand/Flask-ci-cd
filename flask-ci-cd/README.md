# Flask CI/CD Pipeline with Jenkins & Docker

This project demonstrates a CI/CD pipeline integrating:
- 🐍 Python + Flask
- 🐳 Docker
- ⚙️ Jenkins
- 💻 GitHub for version control

## Setup
1. Build and run locally:
   ```bash
   docker build -t flask-ci .
   docker run -p 5000:5000 flask-ci
   ```
   Visit [http://localhost:5000/health](http://localhost:5000/health).

2. Jenkins Pipeline stages:
   - Checkout code
   - Install dependencies
   - Run tests
   - Build Docker image
   - Push image to Docker Hub
   - Deploy container

## Docker Hub & Credentials
- Create Docker Hub credentials in Jenkins (`dockerhub-creds`).
- Update `yourdockerhubusername` in Jenkinsfile.
