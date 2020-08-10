import json
import os
from pathlib import Path

import mlflow
from mlflow import log_param, log_metric, log_artifacts, set_tag

from cd4ml.filenames import get_filenames


def log_metrics_file(file_path):
    with open(file_path, "r") as f:
        json_content = json.load(f)
        for key, val in json_content.items():
            log_metric(key, val)


def log_parameters_file(file_path):
    with open(file_path, "r") as f:
        json_content = json.load(f)
        for key, val in json_content.items():
            log_param(key, val)


def deploy_model(problem_name,
                 ml_pipeline_params_name,
                 feature_set_name,
                 algorithm_name,
                 algorithm_params_name,
                 did_pass_acceptance_test,
                 host_name=None):
    mlflow.set_registry_uri(uri=host_name)
    mlflow.set_experiment(problem_name)
    run_name = os.environ["BUILD_NUMBER"]

    results_folder = Path(get_filenames(problem_name, problem_name).get('results_dir'))

    with mlflow.start_run(run_name=run_name):
        log_param("ProblemName", problem_name)
        log_param("MLPipelineParamsName", ml_pipeline_params_name)
        log_param("FeatureSetName", feature_set_name)
        log_param("AlgorithmName", algorithm_name)
        log_param("AlgorithmParamsName", algorithm_params_name)
        set_tag("DidPassAcceptanceTest", did_pass_acceptance_test)
        log_metrics_file(Path(results_folder, "metrics.json"))
        log_parameters_file(Path(results_folder, "parameters.json"))
        log_artifacts(results_folder)
