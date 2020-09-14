import json
import logging
import os
import mlflow
from mlflow import log_param, log_metric, log_artifacts, set_tag
from cd4ml.filenames import get_model_files
from cd4ml.utils.utils import get_json


def log_model_metrics_file(file_path):
    with open(file_path, "r") as f:
        json_content = json.load(f)
        for key, val in json_content.items():
            log_metric(key, val)


def log_ml_pipeline_params_file(file_path):
    with open(file_path, "r") as f:
        json_content = json.load(f)
        for key, val in json_content.items():
            log_param(key, val)


def register_model(model_id, host_name, did_pass_acceptance_test):
    logger = logging.getLogger(__name__)
    mlflow.set_tracking_uri(uri=host_name)

    logger.info(f"Reporting data for model {model_id}")

    file_names = get_model_files(model_id)
    specification = get_json(file_names['model_specification'])

    mlflow.set_experiment(specification['problem_name'])

    with mlflow.start_run(run_name=model_id):
        log_param("ProblemName", specification['problem_name'])
        log_param("MLPipelineParamsName", specification['ml_pipeline_params_name'])
        log_param("FeatureSetName", specification['feature_set_name'])
        log_param("AlgorithmName", specification['algorithm_name'])
        log_param("AlgorithmParamsName", specification['algorithm_params_name'])

        set_tag("DidPassAcceptanceTest", did_pass_acceptance_test)
        set_tag("BuildNumber", os.getenv('BUILD_NUMBER'))

        log_model_metrics_file(file_names["model_metrics"])
        log_ml_pipeline_params_file(file_names["ml_pipeline_params"])
        log_artifacts(file_names['results_folder'])
