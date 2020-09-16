from cd4ml.feature_set import FeatureSetBase
import cd4ml.problems.houses.features.feature_functions.feature_functions as ff
from cd4ml.utils.feature_utils import get_generic_feature_set, get_feature_params


def get_feature_set_params():
    return get_feature_params(__file__)


def get_feature_set(identifier_field,
                    target_field,
                    info):

    return get_generic_feature_set(identifier_field,
                                   target_field,
                                   info,
                                   __file__,
                                   FeatureSet)


class FeatureSet(FeatureSetBase):
    def __init__(self, identifier_field,
                 target_field,
                 info,
                 feature_set_params):

        super(FeatureSet, self).__init__(identifier_field, target_field)
        self.info = info
        self.params = feature_set_params.copy()

    # actually derive the fields

    def derived_features_categorical(self, base_features):
        # some of these might not selected above
        zipcode = base_features['zipcode']
        features = {'state': ff.zipcode_to_state(zipcode, self.info['zip_lookup'])}
        return {k: features[k] for k in self.params['derived_categorical_n_levels_dict'].keys()}

    def derived_features_numerical(self, base_features):
        # some of these might not selected above
        zipcode = base_features['zipcode']

        features = {'avg_price_in_zip': ff.avg_price_by_zipcode(zipcode, self.info['zip_lookup']),
                    'num_in_zip': ff.num_in_zipcode(zipcode, self.info['zip_lookup']),
                    'avg_price_in_state': ff.avg_price_by_state(zipcode, self.info['zip_lookup']),
                    'num_in_state': ff.num_in_state(zipcode, self.info['zip_lookup'])}

        return {k: features[k] for k in self.params['derived_fields_numerical']}
