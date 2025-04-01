pipeline {
    agent any

    environment {
        VENV_DIR='venv'
        GCP_PROJECT='bold-lantern-454416-b5'
        GCP_ARTIFACT_REPO='europe-west3-docker.pkg.dev/bold-lantern-454416-b5/hotel-reservations'
        GCLOUD_PATH='/var/jenkins_home/google-cloud-sdk/bin'
    }

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
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -e .
                '''
            }
        }
        stage('Building and pushing docker image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script {
                        echo 'Building and pushing docker image to GCR'
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCLOUD_PROJECT}
                            gcloud auth configure-docker --quiet

                            # Build and Push Docker Image
                            gcloud builds submit --tag ${GCP_ARTIFACT_REPO}/${CLOUD_RUN_SERVICE}:latest

                        '''
                    }
                }
            }
        }
//         stage('Deploying on Google Cloud Run') {
//             steps {
//                 withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
//                     script {
//                         echo 'Deploying on Google Cloud Run'
//                         sh '''
//                             export PATH=$PATH:${GCLOUD_PATH}
//                             gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
//                             gcloud config set project ${GCP_PROJECT}
//
//                             gcloud run deploy mlops-p1 \
//                                 --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
//                                 --platform=managed \
//                                 --region=us-central1 \
//                                 --allow-unauthenticated
//                         '''
//                     }
//                 }
//             }
//         }
    }
}