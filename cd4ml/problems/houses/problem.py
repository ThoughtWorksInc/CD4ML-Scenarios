from cd4ml.problems.houses.config.problem_params import problem_params
from cd4ml.problems.houses.config.ml_model_params import model_parameters
from cd4ml.problems.houses.readers.stream_data import stream_data
from cd4ml.problems.houses.readers.zip_lookup import get_zip_lookup
from cd4ml.splitter import splitter
from cd4ml.problem import Problem
from cd4ml.utils import average_by


def get_params():
    return {'problem_name': 'houses',
            'problem_params': problem_params,
            'model_params': model_parameters}


class HousesProblem(Problem):
    def __init__(self):
        super(HousesProblem, self).__init__()
        self.pipeline_params = get_params()
        self.problem_name = self.pipeline_params['problem_name']

        self._stream_data = stream_data
        self.training_filter, self.validation_filter = splitter(self.pipeline_params)

        if self.pipeline_params['problem_params']['feature_set_name'] == 'feature_set_1':
            from cd4ml.problems.houses.features.feature_set_1 import FeatureSet1 as FeatureSet
            self.feature_set = FeatureSet({})
        else:
            self.feature_set = None

        # this will call whatever generic steps should be done after derived class init
        self._post_init()

    def prepare_feature_data(self):
        # do the work required to look up derived features
        if self.feature_set is not None:
            self.feature_set.zip_lookup = get_zip_lookup(self.pipeline_params)

        train_data = self.training_stream()

        avg_price_prior = 350000.0
        prior_num = 5

        averages = average_by(train_data, 'price', 'zipcode',
                              prior_num=prior_num, prior_value=avg_price_prior)

        for k, v in self.feature_set.zip_lookup.items():
            # modify the zip_lookup values in place
            average_count = averages.get(k)
            if average_count is None:
                v['avg_price_in_zip'] = avg_price_prior
                v['num_in_zip'] = 0
            else:
                average, count = average_count
                v['avg_price_in_zip'] = average
                v['num_in_zip'] = count
