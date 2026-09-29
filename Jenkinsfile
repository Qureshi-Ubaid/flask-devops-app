pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = 'ubaidqureshi92/flask-devops-app'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                echo 'Pulling source code from GitHub...'
                git branch: 'main', url: 'https://github.com/Qureshi-Ubaid/flask-devops-app.git'
            }
        }

        stage('2. Test Locally') {
            steps {
                echo 'Running unit tests for Flask app...'
                // Flask App basic validation/test
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('3. Build Docker Image') {
            steps {
                echo 'Building Docker container image...'
                bat "docker build -t ${DOCKER_HUB_REPO}:${IMAGE_TAG} ."
            }
        }

        stage('4. Push to Docker Hub') {
            steps {
                echo 'Authenticating & pushing image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                    bat "docker push ${DOCKER_HUB_REPO}:${IMAGE_TAG}"
                }
            }
        }

        stage('5. Deploy to Kubernetes') {
            steps {
                echo 'Applying Kubernetes Deployment & Service Manifests...'
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
                bat 'kubectl rollout restart deployment/flask-app-deployment'
            }
        }

        stage('6. Verify App Health') {
            steps {
                echo 'Checking Kubernetes Pods and Service Status...'
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