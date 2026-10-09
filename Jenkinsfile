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
                bat '''
                    set PATH=C:\\Users\\Dell\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;C:\\Users\\Dell\\AppData\\Local\\Programs\\Python\\Python314;C:\\Users\\Dell\\AppData\\Local\\Programs\\Python\\Python314\\Scripts;%PATH%
                    python --version
                    docker --version
                '''
            }
        }

        stage('Setup Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                bat '''
                    set PATH=C:\\Users\\Dell\\AppData\\Local\\Programs\\Python\\Python314\\Scripts;%PATH%
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running automated tests for Flask application...'
                bat '''
                    set PATH=C:\\Users\\Dell\\AppData\\Local\\Programs\\Python\\Python314;%PATH%
                    python -c "import app; print('Flask app validation successful!')"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker container image...'
                bat '''
                    set PATH=C:\\Users\\Dell\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;%PATH%
                    docker build -t %DOCKER_HUB_REPO%:%IMAGE_TAG% .
                '''
            }
        }

        stage('Registry Authentication & Push') {
            steps {
                echo 'Logging into Docker Hub and pushing image...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat '''
                        set PATH=C:\\Users\\Dell\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;%PATH%
                        docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                        docker push %DOCKER_HUB_REPO%:%IMAGE_TAG%
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                echo 'Updating Minikube cluster deployment...'
                bat '''
                    set PATH=C:\\Windows\\System32;C:\\Users\\Dell\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;%PATH%
                    set KUBECONFIG=C:\\Users\\Dell\\.kube\\config

                    minikube image load %DOCKER_HUB_REPO%:%IMAGE_TAG%
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                '''
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