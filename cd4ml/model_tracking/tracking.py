import json
import os
import logging

from cd4ml.filenames import get_filenames


class Track:
    def __init__(self, base_metrics_recording_folder, problem_name):
        self.base_metrics_recording_folder = base_metrics_recording_folder
        self.problem_name = problem_name
        self.logger = logging.getLogger(__name__)
        self.model = None
        self.params = dict()
        self.metrics = dict()
        self.plot = None

    def save_results(self):
        folder_name = os.environ.get("GIT_COMMIT", "uncommitted-work")
        filenames = get_filenames(self.problem_name, folder_name)
        self.logger.info("Recording run information to {}".format(filenames['results_dir']))

        if self.model is not None:
            self.model.save(filenames.get('full_model'))

        if self.plot is not None:
            import bokeh.plotting as bokeh_saver
            bokeh_saver.save(obj=self.plot,
                             filename=filenames.get('validation_plot'),
                             title='Validation Plot')

        self._write_dictionary_to_file(self.params, filenames.get('parameters'))
        self._write_dictionary_to_file(self.metrics, filenames.get('metrics'))

    def log_param(self, key, val):
        self.params[key] = val

    def log_ml_params(self, ml_params):
        for key, val in ml_params.items():
            self.log_param(key, val)

    def log_pipeline_params(self, pipeline_params):
        excluded_keys = ['download_data_info']
        for key, val in pipeline_params.items():
            if key not in excluded_keys:
                self.log_param(key, val.__repr__())

    def log_metrics(self, metrics):
        for key, val in metrics.items():
            self.metrics[key] = val

    def log_model(self, model):
        self.model = model

    def log_validation_plot(self, plot):
        self.plot = plot

    def _write_dictionary_to_file(self, dict_to_write, output_file_name):
        with open(output_file_name, 'w') as file:
            json.dump(dict_to_write, file, indent=4)
