import json
import os

from pathlib import Path

from cd4ml.model_tracking.tracking import Track


def test_tracking_dictionaries_only(tmp_path):
    os.environ["CD4ML_DATA_DIR"] = str(tmp_path)
    tracking = Track("unit_test")
    tracking.log_param("my_param", 1)
    tracking.log_metrics({"my_metric": 2})
    tracking.save_results()
    files = os.listdir(Path(tmp_path, 'results', 'uncommitted-work'))
    assert set(files) == {"metrics.json", "parameters.json"}
    metrics_json = json.loads(Path(tmp_path, 'results', 'uncommitted-work', "metrics.json").read_text())
    assert metrics_json["my_metric"] == 2
    params_json = json.loads(Path(tmp_path, 'results', 'uncommitted-work', "parameters.json").read_text())
    assert params_json["my_param"] == 1


def test_writing_bokeh_plot(tmp_path):
    os.environ["CD4ML_DATA_DIR"] = str(tmp_path)
    tracking = Track("unit_test")
    tracking.log_param("my_param", 1)
    tracking.log_metrics({"my_metric": 2})
    tracking.save_results()
    files = os.listdir(Path(tmp_path, 'results', 'uncommitted-work'))
    assert set(files) == {"metrics.json", "parameters.json"}
    metrics_json = json.loads(Path(tmp_path, 'results', 'uncommitted-work', "metrics.json").read_text())
    assert metrics_json["my_metric"] == 2
    params_json = json.loads(Path(tmp_path, 'results', 'uncommitted-work', "parameters.json").read_text())
    assert params_json["my_param"] == 1
