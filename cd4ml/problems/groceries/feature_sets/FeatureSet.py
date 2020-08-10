from cd4ml.feature_set import FeatureSetBase
from cd4ml.problems import read_json_file_as_dict as read_json_file

from pathlib import Path
import cd4ml.problems.groceries.feature_sets.feature_functions as ff

class FeatureSet(FeatureSetBase):
    def __init__(self, identifier_field, target_field, info):
        super(FeatureSet, self).__init__(identifier_field, target_field)
        self.info = info
        self.params = read_json_file(Path(Path(__file__).parent, "params", "feature_set_1_params.json"))

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
        trans = ff.date_to_transactions(base_features, self.info['date_lookup'])

        features = {'day': day,
                    'day_off': day_off,
                    'days_until_end': days_until_end,
                    'transactions_in_day': trans}

        return {k: features[k] for k in self.params['derived_fields_numerical']}
