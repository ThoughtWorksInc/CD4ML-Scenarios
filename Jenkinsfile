pipeline {
    agent any
    parameters {
        choice(name: 'problem_name', choices: ['houses', 'groceries'], description: 'Choose the problem name')
        string(name: 'ml_pipeline_params_name', defaultValue: 'default', description: 'Specify the ml_pipeline_params file')
        string(name: 'feature_set_name', defaultValue: 'default', description: 'Specify the feature_set name/file')
        string(name: 'algorithm_name', defaultValue: 'default', description: 'Specify the algorithm (overrides problem_params)')
        string(name: 'algorithm_params_name', defaultValue: 'default', description: 'Specify the algorithm (overrides the default)')
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
        MLFLOW_S3_ENDPOINT_URL = 'http://minio:9000'
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
                sh 'python3 run_python_script.py pipeline ${problem_name} ${ml_pipeline_params_name} ${feature_set_name} ${algorithm_name} ${algorithm_params_name}'
            }
        }
//         stage('Acceptance test') {
//             steps {
//                 sh 'python3 run_python_script.py acceptance'
//             }
//         }
        stage('Deploy model') {
            steps {
                 sh 'python3 run_python_script.py deploy_model http://mlflow:5000 ${problem_name} ${ml_pipeline_params_name} ${feature_set_name} ${algorithm_name} ${algorithm_params_name} yes'
            }
        }
    }
}
