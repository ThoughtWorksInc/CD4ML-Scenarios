from cd4ml.problems.problem_base import ProblemBase
import cd4ml.problems.groceries.splitting as splitting
import cd4ml.problems.groceries.readers.stream_data as data_streamer
import cd4ml.problems.groceries.download_data.download_data as dd
import logging

from cd4ml.utils.utils import create_lookup


class Problem(ProblemBase):
    def __init__(self,
                 problem_name,
                 data_downloader='default',
                 ml_pipeline_params_name='default',
                 feature_set_name='default',
                 algorithm_name='default',
                 algorithm_params_name='default'):

        super(Problem, self).__init__(problem_name,
                                      data_downloader,
                                      feature_set_name=feature_set_name,
                                      ml_pipeline_params_name=ml_pipeline_params_name,
                                      algorithm_name=algorithm_name,
                                      algorithm_params_name=algorithm_params_name)

        self.logger = logging.getLogger(__name__)
        get_training_validation_filters = splitting.get_training_validation_filters
        self._stream_data = data_streamer.stream_data

        self.date_lookup = None
        self.item_nbr_lookup = None

        self.training_filter, self.validation_filter = get_training_validation_filters(self.ml_pipeline_params)

    def prepare_feature_data(self):
        self.logger.info('Preparing feature data')
        train_data = self.training_stream()
        date_lookup = create_lookup(train_data,
                                    ['dayofweek', 'days_til_end_of_data', 'dayoff'],
                                    'date')

        train_data = self.training_stream()
        item_nbr_lookup = create_lookup(train_data, ['class', 'family'], 'item_nbr')

        if self.feature_set is not None:
            self.feature_set.info['date_lookup'] = date_lookup
            self.feature_set.info['item_nbr_lookup'] = item_nbr_lookup

    @staticmethod
    def get_feature_set_constructor(feature_set_name):
        if feature_set_name == "default":
            from cd4ml.problems.groceries.features.feature_sets.default import feature_set as fs
            return fs.get_feature_set
        elif feature_set_name == "original":
            from cd4ml.problems.groceries.features.feature_sets.original import feature_set as fs
            return fs.get_feature_set
        else:
            raise ValueError("feature_set_name '{}' is invalid. Please check your groceries configuration"
                             .format(feature_set_name))
        pass

    def download_data(self):
        dd.download(self.problem_name)
