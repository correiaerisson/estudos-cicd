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
                    dockerapp = docker.build("correiaerisson/phpdemo", '-f ./Dockerfile .')
                }
            }
        }
    }
}