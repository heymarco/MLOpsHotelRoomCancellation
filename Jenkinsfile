pipeline {
    agent any

    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                echo 'Cloning Github repo to Jenkins...'
                checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/heymarco/MLOpsHotelRoomCancellation.git']])
            }
        }
        stage('Setting up virtual environment') {
            steps {
                echo 'Setting up virtual environment...'
                sh '''
                apt install pipx
                pipx install --user pipenv
                pipenv install -e .
                pipenv shell
                '''
            }
        }
    }
}