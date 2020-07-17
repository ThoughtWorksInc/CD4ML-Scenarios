from cd4ml.problems.houses.config.problem_params import problem_params
from cd4ml.problems.houses.config.ml_model_params import model_parameters
from cd4ml.problems.houses.readers.stream_data import stream_data
from cd4ml.problems.houses.readers.zip_lookup import get_zip_lookup
from cd4ml.splitter import splitter
from cd4ml.problem import Problem
from collections import defaultdict


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

    def prepare_feature_data(self):
        # do the work required to look up derived features
        if self.feature_set is not None:
            self.feature_set.zip_lookup = get_zip_lookup()

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


def average_by(stream, averaged_field, by_field, prior_num=0, prior_value=0.0):
    """
    Average a value by some other field and return a dict of the averages
    Uses Laplace smoothing to deal with the noise from low numbers
    per group to reduce over-fitting
    :param stream: stream of data
    :param averaged_field: field to be averaged
    :param by_field: fields to be grouped by
    :param prior_num: Laplace smoothing, number of synthetic samples
    :param prior_value: Laplace smoothing, prior estimate of average
    :return: dict of (average, count) pairs
    """
    summation = defaultdict(float)
    count = defaultdict(int)

    for row in stream:
        by = row[by_field]
        value = row[averaged_field]
        summation[by] += value
        count[by] += 1

    keys = summation.keys()
    prior_summation = prior_num * prior_value
    averages = {k: ((summation[k] + prior_summation)/(count[k] + prior_num), count[k]) for k in keys}

    return averages
