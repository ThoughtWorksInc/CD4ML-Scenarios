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
            stage("Build"){
                dir("python"){
                    steps {
                        sh 'dvc repro model.pkl.dvc'
                    }
                }
            }
            stage('Evaluate/Test') {
                dir("python"){
                    steps {
                        sh 'python3 test/test.py'
                    }
                }
            }
            stage('Deploy') {
                dir {
                    steps {
                        sh 'curl --request POST --data-binary "@data/decision_tree/model.pkl" http://model:5005/replacemodel'
                    }
                }
            }
    }
}