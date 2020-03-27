pipeline {
    agent any
    environment { 
        MLFLOW_TRACKING_URL = 'http://mlflow:5000'
    }
    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Starting Build'
                sh 'mkdir -p python/data/raw/'
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('tests') {
            steps {
                sh './run_tests.sh'
            }
        }
        stage('Build') {
            steps {
                sh 'python3 run_python_script.py pipeline'
            }
        }
        stage('Deploy') {
            steps {
                sh 'curl --request POST --data-binary "@data/models/model.pkl" http://model:5005/replace_model'
                sh 'curl --request POST --data-binary "@data/models/encoder.json" http://model:5005/replace_encoder'
            }
        }
    }
}
