pipeline {
    agent any
    parameters {
        choice(name: 'problem_name', choices: ['houses', 'groceries'], description: 'Choose the problem name')
    }
    triggers { 
        // Poll SCM every minute for new changes
        pollSCM('* * * * *')
    }
    options {
       // add timestamps to output
       timestamps()
    }
    environment { 
        MLFLOW_TRACKING_URL = 'http://mlflow:5000'
    }
    stages {
        stage('Install dependencies') {
            steps {
                echo 'Starting Build'
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Run tests') {
            steps {
                sh './run_tests.sh'
            }
        }
        stage('Run ML pipeline') {
            steps {
                sh 'python3 run_python_script.py pipeline ${problem_name}'
            }
        }
//         stage('Acceptance test') {
//             steps {
//                 sh 'python3 run_python_script.py acceptance'
//             }
//         }
        stage('Deploy model') {
            steps {
                // sh 'curl --request POST --data-binary "@data/models/full_model.pkl" http://model:5005/replace_model'
                 sh 'python3 run_python_script.py deploy_model http://model:5005 ${problem_name}'
            }
        }
    }
}
