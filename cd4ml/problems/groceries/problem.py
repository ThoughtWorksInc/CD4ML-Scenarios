from cd4ml.problem import ProblemBase
from cd4ml.utils import create_lookup
from cd4ml.feature_set import get_feature_set_class
from cd4ml.get_problem import get_pipeline_params
from cd4ml.utils import import_relative_module
from .splitting import get_training_validation_filters

ff = import_relative_module(__file__, 'features', 'feature_functions')
stream_data = import_relative_module(__file__, 'readers', 'stream_data').stream_data


class Problem(ProblemBase):
    def __init__(self,
                 feature_set_name='default',
                 problem_params_name='default',
                 ml_params_name='default',
                 algorithm_name='default'):

        super(Problem, self).__init__(feature_set_name=feature_set_name,
                                      problem_params_name=problem_params_name,
                                      ml_params_name=ml_params_name,
                                      algorithm_name=algorithm_name)

        self.problem_name = 'groceries'

        self.pipeline_params = get_pipeline_params(self.problem_name,
                                                   problem_params_name,
                                                   ml_params_name,
                                                   algorithm_name,
                                                   __file__)

        self._stream_data = stream_data
        self.training_filter, self.validation_filter = get_training_validation_filters(self.pipeline_params)
        self.date_lookup = None
        self.item_nbr_lookup = None

        # feature set
        if self.feature_set_name == 'default':
            self.feature_set_name = 'feature_set_1'

        feature_set_class = get_feature_set_class(self.feature_set_name, __file__)
        self.feature_set = feature_set_class({}, {})

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
