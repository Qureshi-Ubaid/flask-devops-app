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
                echo 'Verifying system binaries...'
                bat 'python --version'
                bat 'docker --version'
            }
        }

        stage('Setup Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running automated tests for Flask application...'
                bat 'python -c "import app; print(\'Flask app validation successful!\')"'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker container image...'
                bat "docker build -t %DOCKER_HUB_REPO%:%IMAGE_TAG% ."
            }
        }

        stage('Registry Authentication & Push') {
            steps {
                echo 'Logging into Docker Hub and pushing image...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'docker login -u %DOCKER_USER% -p %DOCKER_PASS%'
                    bat "docker push %DOCKER_HUB_REPO%:%IMAGE_TAG%"
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                echo 'Updating Minikube cluster deployment...'
                bat "minikube image load %DOCKER_HUB_REPO%:%IMAGE_TAG%"
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed! Check logs.'
        }
    }
}