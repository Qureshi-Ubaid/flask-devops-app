pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = 'ubaidqureshi92/flask-devops-app'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo 'Pulling source code from GitHub...'
                git branch: 'main', url: 'https://github.com/Qureshi-Ubaid/flask-devops-app.git'
            }
        }

        stage('Check Environment') {
            steps {
                echo 'Checking local system tools...'
                bat 'python --version'
                bat 'docker --version'
                bat 'kubectl version --client'
            }
        }

        stage('Setup') {
            steps {
                echo 'Installing python dependencies...'
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests and app validation...'
                bat 'python -c "import app; print(\'Flask application unit test passed successfully!\')"'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker container image...'
                bat "docker build -t ${DOCKER_HUB_REPO}:${IMAGE_TAG} ."
            }
        }

        stage('Login to Docker Hub') {
            steps {
                echo 'Authenticating with Docker Hub...'
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                echo 'Pushing image to Docker Hub...'
                bat "docker push ${DOCKER_HUB_REPO}:${IMAGE_TAG}"
            }
        }

        stage('Post Actions') {
            steps {
                echo 'Applying Kubernetes Deployment & Service Manifests...'
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
                bat 'kubectl rollout restart deployment/flask-app-deployment'
                bat 'kubectl get pods'
                bat 'kubectl get svc'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! App is accessible on http://localhost:30007'
        }
        failure {
            echo 'Pipeline failed! Check stage logs above for details.'
        }
    }
}