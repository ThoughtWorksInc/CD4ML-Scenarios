import json
import os

from pathlib import Path

from wickedhot import OneHotEncoder

from cd4ml.feature_set import FeatureSetBase
from cd4ml.ml_model import MLModel
from cd4ml.model_tracking.tracking import Track


class TestTracking:
    def test_tracking_dictionaries_only(self, tmp_path):
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

    def test_writing_bokeh_plot(self, tmp_path):
        from bokeh.plotting import figure
        from bokeh.sampledata.iris import flowers

        colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
        colors = [colormap[x] for x in flowers['species']]

        p = figure(title="Iris Morphology")
        p.xaxis.axis_label = 'Petal Length'
        p.yaxis.axis_label = 'Petal Width'

        p.circle(flowers["petal_length"], flowers["petal_width"], color=colors, fill_alpha=0.2, size=10)

        os.environ["CD4ML_DATA_DIR"] = str(tmp_path)
        tracking = Track("unit_test")
        tracking.log_validation_plot(p)
        tracking.save_results()
        files = os.listdir(Path(tmp_path, 'results', 'uncommitted-work'))
        assert set(files) == {"validation_plot.html"}

