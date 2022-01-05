import datetime
import logging
import os
from functools import lru_cache
from pathlib import Path

import mlflow
import requests
from cd4ml.model_utils import load_deployed_model_from_local_file
from cd4ml.problems import list_available_scenarios


class ModelCache:
    def __init__(self, cache_location=Path("mlflow_cache")):
        self.logger = logging.getLogger(__name__)
        self.known_problems = list_available_scenarios()
        self.columns_of_interest = {
            'run_id': 'run_id',
            'tags.BuildNumber': 'build_number',
            'tags.mlflow.runName': 'run_number',
            'end_time': 'time',
            'params.MLPipelineParamsName': 'ml_pipeline_params_name',
            'params.FeatureSetName': 'feature_set_name',
            'params.AlgorithmName': 'algorithm_name',
            'params.AlgorithmParamsName': 'algorithm_params_name',
            'tags.DidPassAcceptanceTest': 'passed_acceptance_test'
        }
        self.base_model_directory = cache_location
        mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URL"])

    def _get_id_for_latest_model(self, all_models_for_scenario):
        possible_deployable_models = [row for row in all_models_for_scenario
                                      if self.is_latest_deployable_model(row)]
        if len(possible_deployable_models) == 0:
            return None

        last_deployment_model = sorted(possible_deployable_models,
                                       key=lambda row: datetime.datetime.strptime(row['time'], "%c"),
                                       reverse=True)
        return last_deployment_model[0]['run_id']

    def get_loaded_model_for_scenario_and_run_id(self, scenario, run_id):
        if run_id == "latest":
            all_models_for_scenario = self.list_available_models_from_ml_flow().get(scenario)

            if all_models_for_scenario is None:
                return None

            latest_item = [item for item in all_models_for_scenario if item['is_latest']]
            if len(latest_item) == 0:
                return None
            return self.get_loaded_model_for_scenario_and_run_id(scenario, latest_item[0]['run_id'])

        model_path = Path(self.base_model_directory, scenario, run_id, "full_model.pkl")

        if not model_path.exists():
            self.download_and_save_from_ml_flow(model_path, run_id)

        return self.read_model(model_path)

    @lru_cache(maxsize=64)
    def read_model(self, model_path):
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
            dataframe_with_columns_renamed['time'] = dataframe_with_columns_renamed['time'].dt.strftime("%c")
            list_of_dictionaries = dataframe_with_columns_renamed.to_dict("records")
            id_of_latest = self._get_id_for_latest_model(list_of_dictionaries)
            for d in list_of_dictionaries:
                d['is_latest'] = d['run_id'] == id_of_latest

            returning_dictionary[scenario] = list_of_dictionaries

        return returning_dictionary

    @staticmethod
    def download_and_save_from_ml_flow(path, run_id):
        path.parent.mkdir(parents=True, exist_ok=True)
        results = requests.get("{}/get-artifact?path=full_model.pkl&run_uuid={}"
                               .format(mlflow.get_tracking_uri(), run_id))
        with open(path, "wb") as f:
            f.write(results.content)

    @staticmethod
    def is_latest_deployable_model(row):
        return row['ml_pipeline_params_name'] == 'default' and \
               row['feature_set_name'] == 'default' and \
               row['algorithm_name'] == 'default' and \
               row['algorithm_params_name'] == 'default' and \
               row['passed_acceptance_test'] == 'yes'
