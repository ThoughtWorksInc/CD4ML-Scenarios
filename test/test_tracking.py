import json
import os
from tempfile import NamedTemporaryFile
from cd4ml.model_tracking.tracking import Track
from cd4ml.filenames import get_model_files

# TODO: might want to pass in temp paths rather than change env variable
# TODO: that could potentially have side effects on other tests


def get_json(filename):
    return json.load(open(filename, 'r'))


class TestTracking:
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
        filenames = get_model_files('unit-test-id', base_data_dir=tmp_path)
        model_dir = filenames['results_folder']
        files = os.listdir(model_dir)
        assert set(files) == {"validation_plot.html", "model_specification.json"}

    def test_tracking_dictionaries_only(self, tmp_path):
        specification = {'problem_name': "foo_problem"}
        os.environ["CD4ML_DATA_DIR"] = str(tmp_path)
        tracking = Track("unit-test-id", specification)
        tracking.log_param("my_param", 1)
        tracking.log_metrics({"my_metric": 2})
        tracking.save_results()

        filenames = get_model_files('unit-test-id', base_data_dir=tmp_path)
        model_dir = filenames['results_folder']
        files = os.listdir(model_dir)

        assert set(files) == {"model_metrics.json", "ml_pipeline_params.json", "model_specification.json"}
        metrics_json = get_json(filenames['model_metrics'])
        assert metrics_json["my_metric"] == 2
        params_json = get_json(filenames['ml_pipeline_params'])
        assert params_json["my_param"] == 1
