import json
import logging
from pathlib import Path
import os
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


def register_model(model_id, host_name=None, did_pass_acceptance_test='not-checked'):
    logger = logging.getLogger(__name__)
    mlflow.set_tracking_uri(uri=host_name)

    file_names = get_filenames('', '')
    results_dir = file_names['results_dir']
    results_folder = Path(results_dir, model_id)

    logger.info("Reporting data from from folder {}".format(results_folder))

    file_names = get_filenames('', model_id)
    specification = json.load(open(file_names['specification'], 'r'))
    mlflow.set_experiment(specification['problem_name'])

    with mlflow.start_run(run_name=model_id):
        log_param("ProblemName", specification['problem_name'])
        log_param("MLPipelineParamsName", specification['ml_pipeline_params_name'])
        log_param("FeatureSetName", specification['feature_set_name'])
        log_param("AlgorithmName", specification['algorithm_name'])
        log_param("AlgorithmParamsName", specification['algorithm_params_name'])

        set_tag("DidPassAcceptanceTest", did_pass_acceptance_test)
        set_tag("BuildNumber", os.getenv('BUILD_NUMBER'))

        log_metrics_file(Path(results_folder, "metrics.json"))
        log_parameters_file(Path(results_folder, "parameters.json"))
        log_artifacts(results_folder)
