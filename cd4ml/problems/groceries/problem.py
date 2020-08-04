from cd4ml.problem import ProblemBase
from cd4ml.utils import create_lookup
from cd4ml.utils import import_relative_module

stream_data = import_relative_module(__file__, 'readers', 'stream_data').stream_data
splitting = import_relative_module(__file__, '.', 'splitting')
get_training_validation_filters = splitting.get_training_validation_filters


class Problem(ProblemBase):
    def __init__(self,
                 problem_name,
                 feature_set_name='default',
                 ml_pipeline_params_name='default',
                 algorithm_name='default',
                 algorithm_params_name='default'):

        super(Problem, self).__init__(problem_name,
                                      feature_set_name=feature_set_name,
                                      ml_pipeline_params_name=ml_pipeline_params_name,
                                      algorithm_name=algorithm_name,
                                      algorithm_params_name=algorithm_params_name)

        self._stream_data = stream_data

        self.date_lookup = None
        self.item_nbr_lookup = None

        self.training_filter, self.validation_filter = get_training_validation_filters(self.ml_pipeline_params)

    def prepare_feature_data(self):
        print('Preparing feature data')
        train_data = self.training_stream()
        date_lookup = create_lookup(train_data,
                                    ['dayofweek', 'days_til_end_of_data', 'dayoff', 'transactions'],
                                    'date')

        train_data = self.training_stream()
        item_nbr_lookup = create_lookup(train_data, ['class', 'family'], 'item_nbr')

        if self.feature_set is not None:
            self.feature_set.info['date_lookup'] = date_lookup
            self.feature_set.info['item_nbr_lookup'] = item_nbr_lookup
