pipeline{
    agent any
    stages{
        stage("verify tooloing"){
            steps{
                sh '''
                docker version
                docker info
                docker-compose version
                curl --version
                '''
            }
        }
        stage ('Prune Dokce data'){
            steps{
                sh 'docker stop $(docker ps -q)'
                sh 'docker system prune -a'
            }
        }
        stage ('Start container'){
            steps{
                sh 'docker-compose up -d'
                sh 'docker ps'
            }
        }
        stage ('Run tests'){
            steps{
                sh 'curl http://localhost:8080/admin'
            }
        }
    }
}