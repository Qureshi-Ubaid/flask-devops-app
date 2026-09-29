pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Qureshi-Ubaid/flask-devops-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t ubaidqureshi92/flask-devops-app:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                    bat 'docker push ubaidqureshi92/flask-devops-app:latest'
                }
            }
        }
    }
}
