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
        zip_lookup = get_zip_lookup()
        if self.feature_set is not None:
            self.feature_set.zip_lookup = zip_lookup

        train_data = self.training_stream()

        sum_price_by_zip = defaultdict(float)
        n_by_zip = defaultdict(int)

        for row in train_data:
            zipcode = row['zipcode']
            price = row['price']
            sum_price_by_zip[zipcode] += price
            n_by_zip[zipcode] += 1

        zipcodes = list(sum_price_by_zip.keys())

        avg_price_prior = 350000.0
        alpha_prior = 5

        avg_look = {z: (sum_price_by_zip[z] + alpha_prior * avg_price_prior)/(alpha_prior + n_by_zip[z])
                    for z in zipcodes}

        avg_look_exact = {z: sum_price_by_zip[z] / n_by_zip[z] for z in zipcodes}

        for k, v in self.feature_set.zip_lookup.items():
            v['avg_price_in_zip'] = avg_look.get(k, avg_price_prior)
            v['avg_price_in_zip_no_smooth'] = avg_look_exact.get(k, avg_price_prior)
            v['num_in_zip'] = n_by_zip.get(k, 0)
