from cd4ml.problems.houses_alt.config.problem_params import problem_params
from cd4ml.problems.houses_alt.config.ml_model_params import model_parameters
from cd4ml.problems.houses_alt.readers.stream_data import stream_data
from cd4ml.problems.houses_alt.readers.zip_lookup import get_zip_lookup
from cd4ml.splitter import splitter
from cd4ml.problem import Problem
from cd4ml.utils import average_by
from cd4ml.feature_set import get_feature_set_class


def get_params():
    return {'problem_name': 'houses_alt',
            'problem_params': problem_params,
            'model_params': model_parameters}


class HousesProblemAlt(Problem):
    def __init__(self, feature_set_name='default'):
        super(HousesProblemAlt, self).__init__()
        self.pipeline_params = get_params()
        self.problem_name = self.pipeline_params['problem_name']

        self._stream_data = stream_data
        self.training_filter, self.validation_filter = splitter(self.pipeline_params)

        if feature_set_name == 'default':
            feature_set_name = 'feature_set_alt_1'

        feature_set_class = get_feature_set_class(feature_set_name, __file__)
        self.feature_set = feature_set_class({})

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
                              prior_num=prior_num,
                              prior_value=avg_price_prior)

        train_data = self.training_stream()

        def zipcode_to_state(zipcode):
            state = self.feature_set.zip_lookup[zipcode]['state']
            return state

        averages_state = average_by(train_data, 'price', 'zipcode',
                                    prior_num=prior_num,
                                    prior_value=avg_price_prior,
                                    transform=zipcode_to_state)

        for k, v in self.feature_set.zip_lookup.items():
            # modify the zip_lookup values in place
            average_count = averages.get(k)
            values = self.feature_set.zip_lookup.get(k)
            state = values.get('state', 'not a state')
            average_count_state = averages_state.get(state)

            if average_count is None:
                v['avg_price_in_zip'] = avg_price_prior
                v['num_in_zip'] = 0
                v['avg_price_in_state'] = avg_price_prior
                v['num_in_state'] = 0

            else:
                average, count = average_count
                average_state, count_state = average_count_state
                v['avg_price_in_zip'] = average
                v['num_in_zip'] = count
                v['avg_price_in_state'] = average_state
                v['num_in_state'] = count_state
