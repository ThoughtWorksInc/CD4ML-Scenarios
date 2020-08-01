pipeline {
    agent any
    parameters {
        choice(name: 'problem_name', choices: ['houses', 'groceries'], description: 'Choose the problem name')
        string(name: 'feature_set_name', defaultValue: 'default', description: 'Specify the feature_set name/file')
        string(name: 'problem_params_name', defaultValue: 'default', description: 'Specify the problem_params file')
        string(name: 'ml_model_params', defaultValue: 'default', description: 'Specify the ml_model_params file')
        string(name: 'algorithm_name', defaultValue: 'default', description: 'Specify the algorithm (overrides problem_params)')
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
                sh 'python3 run_python_script.py pipeline ${problem_name} ${feature_set_name} ${problem_params_name} ${ml_model_params} ${algorithm_name}'
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
                 sh 'python3 run_python_script.py deploy_model http://model:5005 ${problem_name} ${feature_set_name}'
            }
        }
    }
}
