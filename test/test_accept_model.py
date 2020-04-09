import os

import mlflow
import mlflow.tracking

threshold = 0.65


def get_latest_executed_run(df_of_runs):
    filtered_dataframe = df_of_runs[df_of_runs["tags.mlflow.runName"] == os.environ["BUILD_NUMBER"]]
    assert len(filtered_dataframe) == 1
    return filtered_dataframe


def get_r2_score(df_of_single_run):
    return df_of_single_run["metrics.r2_score"][0]


def test_model_performance():
    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URL"])
    experiment = mlflow.get_experiment_by_name("local")
    runs = mlflow.search_runs(experiment_ids=experiment.experiment_id)
    last_run_record = get_latest_executed_run(runs)
    r2_score = get_r2_score(last_run_record)
    run_name = last_run_record["tags.mlflow.runName"][0]
    assert r2_score > threshold, "R2 Score for Run '{}' was too low for model acceptance, r2_score:{}  threshold:{}"\
        .format(run_name, r2_score, threshold)
