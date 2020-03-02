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
        dir("python"){
            stage("Build"){
                steps {
                    sh 'dvc repro model.pkl.dvc'
                }
            }
            stage('Evaluate/Test') {
                steps {
                    sh 'python3 test/test.py'
                }
            }
            stage('Deploy') {
                steps {
                    sh 'curl --request POST --data-binary "@data/decision_tree/model.pkl" http://model:5005/replacemodel'
                }
            }
        }
    }
}