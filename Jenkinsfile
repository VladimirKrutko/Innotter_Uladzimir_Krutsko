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
                sh 'docker system prune -f -a --volumes'
            }
        }
        stage ('Start container'){
            steps{
                sh 'docker-compose up -d --no-color --wait'
                sh 'dcocker ps'
            }
        }
    post 
    always{
        sh 'curl http://localhost:8080/admin'
    }
    }
}