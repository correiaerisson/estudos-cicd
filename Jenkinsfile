pipeline {
    agent any
    stages {
        stage ('Inicial'){
            steps {
                echo 'Iniciando a pipeline'
            }
        }
        stage ('Build Image'){
            steps {
                script {
                    dockerapp = docker.build("pulsemanchaotix/phpdemo", '-f ./Dockerfile .')
                }
            }
        }
        stage ('Push Image'){
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com','dockerhub') {
                        dockerapp.push('latest')
                    }
                }
            }
        }
    }
}