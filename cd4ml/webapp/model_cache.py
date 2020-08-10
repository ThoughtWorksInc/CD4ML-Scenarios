import logging
import os
import mlflow

from pathlib import Path

import requests

from cd4ml.filenames import get_filenames
from cd4ml.model_utils import load_deployed_model_from_local_file
from cd4ml.problems import list_available_scenarios


class ModelCache:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.known_problems = list_available_scenarios()
        self.mlflow = mlflow
        self.columns_of_interest = {
            'run_id': 'run_id',
            'end_time': 'time',
            'params.MLPipelineParamsName': 'ml_pipeline_params_name',
            'params.FeatureSetName': 'feature_set_name',
            'params.AlgorithmName': 'algorithm_name',
            'params.AlgorithmParamsName': 'algorithm_params_name',
            'tags.DidPassAcceptanceTest': 'passed_acceptance_test'
        }
        mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URL"])


    def get_loaded_model_for_scenario_and_run_id(self, scenario, run_id):
        base_scenario_folder_path = get_filenames(scenario, run_id)['model_cache_dir']
        model_path = Path(base_scenario_folder_path, "full_model.pkl")

        if not model_path.exists():
            self.download_and_save_from_ml_flow(model_path, run_id)

        return load_deployed_model_from_local_file(model_path)


    def list_available_models_from_ml_flow(self):
        returning_dictionary = dict()
        for scenario in self.known_problems:
            experiment = mlflow.get_experiment_by_name(scenario)
            if experiment is None:
                continue
            runs = mlflow.search_runs(experiment_ids=experiment.experiment_id)
            dataframe_with_columns_of_interest = runs[list(self.columns_of_interest.keys())]
            dataframe_with_columns_renamed = dataframe_with_columns_of_interest.rename(columns=self.columns_of_interest)
            returning_dictionary[scenario] = dataframe_with_columns_renamed.to_dict(orient="rows")

        return returning_dictionary


    def download_and_save_from_ml_flow(self, path, run_id):
        path.parent.mkdir(parents=True, exist_ok=True)
        results = requests.get("{}/get-artifact?path=full_model.pkl&run_uuid={}"
                               .format(mlflow.get_tracking_uri(), run_id))
        with open(path, "wb") as f:
            f.write(results.content)