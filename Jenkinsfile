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
                // sh 'docker stop $(docker ps -q)'
                sh 'docker system prune -a'
            }
        }
        stage ('Start container'){
            steps{
                sh 'docker-compose up --build -d'
                sh 'docker ps'
            }
        }
        stage ('Run tests'){
            steps{
                sh 'curl http://localhost:8080/admin'
            }
        }
    }
    post {
        // Clean after build
        always {
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true,
                    patterns: [[pattern: '.gitignore', type: 'INCLUDE'],
                               [pattern: '.propsfile', type: 'EXCLUDE']])
        }
    }
}