from cd4ml.problems.problem_base import ProblemBase
from cd4ml.problems.houses.download_data.download_data import download
import cd4ml.problems.houses.readers.stream_data as stream_data
import cd4ml.problems.houses.readers.zip_lookup as zip_lookup
from cd4ml.utils.utils import average_by


class Problem(ProblemBase):
    def __init__(self,
                 problem_name,
                 data_downloader='default',
                 ml_pipeline_params_name='default',
                 feature_set_name='default',
                 algorithm_name='default',
                 algorithm_params_name='default'):

        super(Problem, self).__init__(problem_name,
                                      data_downloader=data_downloader,
                                      feature_set_name=feature_set_name,
                                      ml_pipeline_params_name=ml_pipeline_params_name,
                                      algorithm_name=algorithm_name,
                                      algorithm_params_name=algorithm_params_name)
        self.zip_lookup = zip_lookup.get_zip_lookup

        self._stream_data = stream_data.stream_data

    @staticmethod
    def get_feature_set_constructor(feature_set_name):
        if feature_set_name == 'default':
            import cd4ml.problems.houses.features.feature_sets.default.feature_set as default_features
            return default_features.get_feature_set
        elif feature_set_name == 'simple':
            import cd4ml.problems.houses.features.feature_sets.simple.feature_set as default_features
            return default_features.get_feature_set
        else:
            raise ValueError("Featureset name {} is not valid".format(feature_set_name))

    def prepare_feature_data(self):
        # do the work required to look up derived features
        if self.feature_set is not None:
            self.feature_set.info['zip_lookup'] = zip_lookup.get_zip_lookup(self.problem_name)

        train_data = self.training_stream()
        avg_price_prior = 350000.0
        prior_num = 5

        averages = average_by(train_data, 'price', 'zipcode',
                              prior_num=prior_num,
                              prior_value=avg_price_prior)

        train_data = self.training_stream()

        def zipcode_to_state(zipcode):
            return self.feature_set.info['zip_lookup'][zipcode]['state']

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

    def download_data(self):
        download()
