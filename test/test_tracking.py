import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from cd4ml.model_tracking.tracking import Track


class TestTracking:
    def test_tracking_dictionaries_only(self, tmp_path):
        specification = {'problem_name': "foo_problem"}
        os.environ["CD4ML_DATA_DIR"] = str(tmp_path)
        tracking = Track("unit-test-id", specification)
        tracking.log_param("my_param", 1)
        tracking.log_metrics({"my_metric": 2})
        tracking.save_results()

        files = os.listdir(Path(tmp_path, 'results', 'unit-test-id'))
        assert set(files) == {"metrics.json", "parameters.json", "specification.json"}
        metrics_json = json.loads(Path(tmp_path, 'results', 'unit-test-id', "metrics.json").read_text())
        assert metrics_json["my_metric"] == 2
        params_json = json.loads(Path(tmp_path, 'results', 'unit-test-id', "parameters.json").read_text())
        assert params_json["my_param"] == 1

    def test_writing_bokeh_plot(self, tmp_path):
        from bokeh.plotting import figure, output_file
        from bokeh.sampledata.iris import flowers
        specification = {'problem_name': "foo_problem"}

        colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
        colors = [colormap[x] for x in flowers['species']]

        output_file(NamedTemporaryFile().name)
        p = figure(title="Iris Morphology")
        p.xaxis.axis_label = 'Petal Length'
        p.yaxis.axis_label = 'Petal Width'

        p.circle(flowers["petal_length"], flowers["petal_width"], color=colors, fill_alpha=0.2, size=10)

        os.environ["CD4ML_DATA_DIR"] = str(tmp_path)
        tracking = Track("unit-test-id", specification)
        tracking.log_validation_plot(p)
        tracking.save_results()
        files = os.listdir(Path(tmp_path, 'results', 'unit-test-id'))
        assert set(files) == {"validation_plot.html", "specification.json"}

