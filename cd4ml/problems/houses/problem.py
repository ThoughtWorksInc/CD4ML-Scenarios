from cd4ml.problem import ProblemBase
from cd4ml.utils import average_by
from cd4ml.utils import import_relative_module

stream_data = import_relative_module(__file__, 'readers', 'stream_data').stream_data
get_zip_lookup = import_relative_module(__file__, 'readers', 'zip_lookup').get_zip_lookup


def get_ml_pipeline_params(ml_pipeline_params_name):
    module = import_relative_module(__file__, 'ml_pipelines', ml_pipeline_params_name)
    return module.ml_pipeline_params


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

    def prepare_feature_data(self):
        # do the work required to look up derived features
        if self.feature_set is not None:
            prob_name = self.specification.spec['problem_name']
            self.feature_set.info['zip_lookup'] = get_zip_lookup(prob_name)

        train_data = self.training_stream()
        avg_price_prior = 350000.0
        prior_num = 5

        averages = average_by(train_data, 'price', 'zipcode',
                              prior_num=prior_num,
                              prior_value=avg_price_prior)

        train_data = self.training_stream()

        def zipcode_to_state(zipcode):
            state = self.feature_set.info['zip_lookup'][zipcode]['state']
            return state

        averages_state = average_by(train_data, 'price', 'zipcode',
                                    prior_num=prior_num,
                                    prior_value=avg_price_prior,
                                    transform=zipcode_to_state)

        for k, v in self.feature_set.info['zip_lookup'].items():
            # modify the zip_lookup values in place
            average_count = averages.get(k)
            values = self.feature_set.info['zip_lookup'].get(k)
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
