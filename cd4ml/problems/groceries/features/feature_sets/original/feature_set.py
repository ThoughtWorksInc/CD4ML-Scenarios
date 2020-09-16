from cd4ml.feature_set import FeatureSetBase
import cd4ml.problems.groceries.features.feature_functions.feature_functions as ff
from cd4ml.utils.feature_utils import get_feature_params, get_generic_feature_set


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
    def __init__(self, identifier_field, target_field, info, feature_set_params):
        super(FeatureSet, self).__init__(identifier_field, target_field)
        self.info = info
        self.params = feature_set_params

    def derived_features_categorical(self, base_features):
        # some of these might not selected above
        date = base_features['date']
        year, month, day = ff.date_to_ymd(date)
        day_of_week = ff.date_to_day_of_week(base_features, self.info['date_lookup'])

        product_class = ff.item_nbr_to_product_class(base_features, self.info['item_nbr_lookup'])
        product_family = ff.item_nbr_to_product_family(base_features, self.info['item_nbr_lookup'])

        features = {'year': year,
                    'month': month,
                    'day_of_week': day_of_week,
                    'product_class': product_class,
                    'product_family': product_family}

        return {k: features[k] for k in self.params['derived_categorical_n_levels_dict'].keys()}

    def derived_features_numerical(self, base_features):
        # some of these might not selected above

        date = base_features['date']
        year, month, day = ff.date_to_ymd(date)
        day_off = ff.date_to_day_off(base_features, self.info['date_lookup'])
        days_until_end = ff.date_to_days_until_end(base_features, self.info['date_lookup'])

        features = {'day': day,
                    'day_off': day_off,
                    'days_until_end': days_until_end}

        return {k: features[k] for k in self.params['derived_fields_numerical']}
