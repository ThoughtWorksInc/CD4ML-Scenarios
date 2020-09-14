import os
import mlflow
import mlflow.tracking

TENANT = os.getenv('TENANT', 'local')

# TODO: delete this file?


def get_latest_executed_run(df_of_runs):
    filtered_dataframe = df_of_runs[df_of_runs["tags.mlflow.runName"] == os.environ["BUILD_NUMBER"]]
    assert len(filtered_dataframe) == 1
    return filtered_dataframe


def get_metric(metric_name, df_of_single_run):
    return df_of_single_run["metrics.%s" % metric_name].head().values[0]


def check_model_performance_deprecated(metric_name, threshold_min, threshold_max):
    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URL"])
    experiment = mlflow.get_experiment_by_name(TENANT)
    runs = mlflow.search_runs(experiment_ids=experiment.experiment_id)
    last_run_record = get_latest_executed_run(runs)
    metric_value = get_metric(metric_name, last_run_record)
    run_name = last_run_record["tags.mlflow.runName"].head().values[0]
    template = "Metric: {metric_name} for Run: {run_name} was not accepted, " \
               "value: {metric_value}, " \
               "threshold_min: {threshold_min}, threshold_max: {threshold_max}"
    message = template.format(run_name=run_name,
                              metric_name=metric_name,
                              metric_value=metric_value,
                              threshold_min=threshold_min,
                              threshold_max=threshold_max)

    assert threshold_min <= metric_value <= threshold_max, message
