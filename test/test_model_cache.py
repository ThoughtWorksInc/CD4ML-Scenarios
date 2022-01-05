import os
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import mlflow
import pandas as pd
import pytest
import requests_mock

from cd4ml.webapp.model_cache import ModelCache


class TestModelCache:
    @classmethod
    def setup_class(cls):
        uri_ = "http://test-tracking-uri:8080"
        mlflow.set_tracking_uri(uri_)
        os.environ["MLFLOW_TRACKING_URL"] = "http://test-tracking-uri:8080"

    def test_is_latest_deployable_model(self):
        row = {
            "ml_pipeline_params_name": 'default',
            "feature_set_name": 'default',
            "algorithm_name": 'default',
            "algorithm_params_name": 'default',
            "passed_acceptance_test": 'yes'
        }
        assert ModelCache.is_latest_deployable_model(row)

    def test_is_not_latest_deployable_model(self):
        row = {
            "ml_pipeline_params_name": 'default',
            "feature_set_name": 'default',
            "algorithm_name": 'my_params',
            "algorithm_params_name": 'default',
            "passed_acceptance_test": 'yes'
        }
        assert not ModelCache.is_latest_deployable_model(row)

    def test_download_and_save_from_mlflow(self, tmp_path):
        saving_path = Path(tmp_path, "file.txt")
        with requests_mock.Mocker() as mocked_req:
            mocked_req.get("http://test-tracking-uri:8080/get-artifact?path=full_model.pkl&run_uuid=123-abc",
                           text="Hello World")
            ModelCache.download_and_save_from_ml_flow(saving_path, "123-abc")
            assert saving_path.read_text() == "Hello World"

    def test_list_no_models_available(self):
        cache = ModelCache()

        def get_search_return_values(experiment_ids, *args, **kwargs):
            df = pd.DataFrame(columns=list(cache.columns_of_interest.keys()))
            df["end_time"] = pd.to_datetime(df["end_time"])
            return df

        def get_experiment_id(scenario, *args, **kwargs):
            return SimpleNamespace(**{'experiment_id': "id_" + scenario})

        mlflow.get_experiment_by_name = MagicMock(side_effect=get_experiment_id)
        mlflow.search_runs = MagicMock(side_effect=get_search_return_values)

        available_models = cache.list_available_models_from_ml_flow()
        assert available_models == {"groceries": [], "houses": [], "iris": []}

    def test_list_no_houses_experiment_not_available(self):
        cache = ModelCache()

        def get_search_return_values(experiment_ids, *args, **kwargs):
            df = pd.DataFrame(columns=list(cache.columns_of_interest.keys()))
            df["end_time"] = pd.to_datetime(df["end_time"])
            return df

        def get_experiment_id(scenario, *args, **kwargs):
            if scenario == "houses":
                return None
            else:
                return SimpleNamespace(**{'experiment_id': "id_" + scenario})

        mlflow.get_experiment_by_name = MagicMock(side_effect=get_experiment_id)
        mlflow.search_runs = MagicMock(side_effect=get_search_return_values)

        available_models = cache.list_available_models_from_ml_flow()
        assert available_models == {"groceries": [], "iris": []}

    def test_return_a_couple_models(self):
        cache = ModelCache()

        def get_search_return_values(experiment_ids, *args, **kwargs):
            df = pd.DataFrame(columns=list(cache.columns_of_interest.keys()), data=[{
                'run_id': "123",
                'tags.mlflow.runName': 'my_run',
                'tags.mlflow.BuildNumber': '4',
                'end_time': datetime(2020, 8, 29, 8, 0, 0),
                'params.MLPipelineParamsName': 'default',
                'params.FeatureSetName': 'default',
                'params.AlgorithmName': 'default',
                'params.AlgorithmParamsName': 'default',
                'tags.DidPassAcceptanceTest': 'no'
            }, {
                'run_id': "456",
                'tags.mlflow.runName': 'my_second_run',
                'tags.mlflow.BuildNumber': '5',
                'end_time': datetime(2020, 8, 29, 9, 0, 0),
                'params.MLPipelineParamsName': 'default',
                'params.FeatureSetName': 'default',
                'params.AlgorithmName': 'default',
                'params.AlgorithmParamsName': 'default',
                'tags.DidPassAcceptanceTest': 'yes'
            }])
            df["end_time"] = pd.to_datetime(df["end_time"])
            return df

        def get_experiment_id(scenario, *args, **kwargs):
            if scenario == "houses":
                return None
            else:
                return SimpleNamespace(**{'experiment_id': "id_" + scenario})

        mlflow.get_experiment_by_name = MagicMock(side_effect=get_experiment_id)
        mlflow.search_runs = MagicMock(side_effect=get_search_return_values)

        available_models = cache.list_available_models_from_ml_flow()
        assert set(available_models.keys()) == {"groceries", "iris"}
        assert len(available_models["groceries"]) == 2
        assert [x["run_id"] for x in available_models["groceries"]] == ['123', '456']
        assert [x["is_latest"] for x in available_models["groceries"] if x["run_id"] == "456"][0]
        assert not [x["is_latest"] for x in available_models["groceries"] if x["run_id"] == "123"][0]

    def test_get_model_by_name(self, tmp_path):
        cache = ModelCache(tmp_path)

        def get_search_return_values(experiment_ids, *args, **kwargs):
            df = pd.DataFrame(columns=list(cache.columns_of_interest.keys()), data=[{
                'run_id': "123",
                'tags.mlflow.runName': '1',
                'end_time': datetime(2020, 8, 29, 8, 0, 0),
                'params.MLPipelineParamsName': 'default',
                'params.FeatureSetName': 'default',
                'params.AlgorithmName': 'default',
                'params.AlgorithmParamsName': 'default',
                'tags.DidPassAcceptanceTest': 'no'
            }, {
                'run_id': "456",
                'tags.mlflow.runName': '2',
                'end_time': datetime(2020, 8, 29, 9, 0, 0),
                'params.MLPipelineParamsName': 'default',
                'params.FeatureSetName': 'default',
                'params.AlgorithmName': 'default',
                'params.AlgorithmParamsName': 'default',
                'tags.DidPassAcceptanceTest': 'yes'
            }])
            df["end_time"] = pd.to_datetime(df["end_time"])
            return df

        def get_experiment_id(scenario, *args, **kwargs):
            if scenario == "houses":
                return None
            else:
                return SimpleNamespace(**{'experiment_id': "id_" + scenario})

        model_as_bytes = self.get_sample_model_path().read_bytes()
        with requests_mock.Mocker() as mocked_req:
            mocked_req.get("http://test-tracking-uri:8080/get-artifact?path=full_model.pkl&run_uuid=123",
                           content=model_as_bytes)
            mlflow.get_experiment_by_name = MagicMock(side_effect=get_experiment_id)
            mlflow.search_runs = MagicMock(side_effect=get_search_return_values)
            loaded_model = cache.get_loaded_model_for_scenario_and_run_id("groceries", "123")
            assert loaded_model is not None

        assert Path(tmp_path, "groceries", "123").exists()

    def test_get_latest_model_no_latest(self, tmp_path):
        cache = ModelCache(tmp_path)

        def get_search_return_values(experiment_ids, *args, **kwargs):
            df = pd.DataFrame(columns=list(cache.columns_of_interest.keys()), data=[{
                'run_id': "123",
                'tags.mlflow.runName': '1',
                'end_time': datetime(2020, 8, 29, 8, 0, 0),
                'params.MLPipelineParamsName': 'default',
                'params.FeatureSetName': 'default',
                'params.AlgorithmName': 'default',
                'params.AlgorithmParamsName': 'default',
                'tags.DidPassAcceptanceTest': 'no'
            }])
            df["end_time"] = pd.to_datetime(df["end_time"])
            return df

        def get_experiment_id(scenario, *args, **kwargs):
            if scenario == "houses":
                return None
            else:
                return SimpleNamespace(**{'experiment_id': "id_" + scenario})

        model_as_bytes = self.get_sample_model_path().read_bytes()
        with requests_mock.Mocker() as mocked_req:
            mocked_req.get("http://test-tracking-uri:8080/get-artifact?path=full_model.pkl&run_uuid=123",
                           content=model_as_bytes)
            mlflow.get_experiment_by_name = MagicMock(side_effect=get_experiment_id)
            mlflow.search_runs = MagicMock(side_effect=get_search_return_values)
            loaded_model = cache.get_loaded_model_for_scenario_and_run_id("groceries", "latest")
            assert loaded_model is None

    def test_get_latest_model_with_latest(self, tmp_path):
        cache = ModelCache(tmp_path)

        def get_search_return_values(experiment_ids, *args, **kwargs):
            df = pd.DataFrame(columns=list(cache.columns_of_interest.keys()), data=[
                {
                    'run_id': "123",
                    'tags.mlflow.runName': '1',
                    'end_time': datetime(2020, 8, 29, 8, 0, 0),
                    'params.MLPipelineParamsName': 'default',
                    'params.FeatureSetName': 'default',
                    'params.AlgorithmName': 'default',
                    'params.AlgorithmParamsName': 'default',
                    'tags.DidPassAcceptanceTest': 'no'
                },
                {
                    'run_id': "456",
                    'tags.mlflow.runName': '1',
                    'end_time': datetime(2020, 8, 29, 8, 0, 0),
                    'params.MLPipelineParamsName': 'default',
                    'params.FeatureSetName': 'default',
                    'params.AlgorithmName': 'default',
                    'params.AlgorithmParamsName': 'default',
                    'tags.DidPassAcceptanceTest': 'yes'
                }])
            df["end_time"] = pd.to_datetime(df["end_time"])
            return df

        def get_experiment_id(scenario, *args, **kwargs):
            if scenario == "houses":
                return None
            else:
                return SimpleNamespace(**{'experiment_id': "id_" + scenario})

        model_as_bytes = self.get_sample_model_path().read_bytes()
        with requests_mock.Mocker() as mocked_req:
            mocked_req.get("http://test-tracking-uri:8080/get-artifact?path=full_model.pkl&run_uuid=456",
                           content=model_as_bytes)
            mlflow.get_experiment_by_name = MagicMock(side_effect=get_experiment_id)
            mlflow.search_runs = MagicMock(side_effect=get_search_return_values)
            loaded_model = cache.get_loaded_model_for_scenario_and_run_id("groceries", "latest")
            assert loaded_model is not None

        assert Path(tmp_path, "groceries", "456").exists()
        assert not Path(tmp_path, "groceries", "123").exists()

    def get_sample_model_path(self):
        return Path(Path(__file__).parent, "resources", "full_model.pkl")
