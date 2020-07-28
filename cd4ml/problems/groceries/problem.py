from cd4ml.problems.groceries.config.problem_params import problem_params
from cd4ml.problems.groceries.config.ml_model_params import model_parameters
from cd4ml.problems.groceries.readers.stream_data import stream_data
from cd4ml.problems.groceries.splitting import get_training_validation_filters
from cd4ml.problem import Problem
from cd4ml.utils import create_lookup


def get_params():
    return {'problem_name': 'groceries',
            'problem_params': problem_params,
            'model_params': model_parameters}


class GroceriesProblem(Problem):
    def __init__(self):
        super(GroceriesProblem, self).__init__()
        self.pipeline_params = get_params()
        self.problem_name = self.pipeline_params['problem_name']

        self._stream_data = stream_data
        self.training_filter, self.validation_filter = get_training_validation_filters(self.pipeline_params)
        self.date_lookup = None
        self.item_nbr_lookup = None

        if self.pipeline_params['problem_params']['feature_set_name'] == 'feature_set_1':
            from cd4ml.problems.groceries.features.feature_set_1 import FeatureSet1 as FeatureSet
            self.feature_set = FeatureSet({}, {})
        else:
            self.feature_set = None

    def prepare_feature_data(self):
        print('Preparing feature data')
        train_data = self.training_stream()
        date_lookup = create_lookup(train_data,
                                    ['dayofweek', 'days_til_end_of_data', 'dayoff', 'transactions'],
                                    'date')

        train_data = self.training_stream()
        item_nbr_lookup = create_lookup(train_data, ['class', 'family'], 'item_nbr')

        if self.feature_set is not None:
            self.feature_set.date_lookup = date_lookup
            self.feature_set.item_nbr_lookup = item_nbr_lookup
