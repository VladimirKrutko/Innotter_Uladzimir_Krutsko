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
    }
}