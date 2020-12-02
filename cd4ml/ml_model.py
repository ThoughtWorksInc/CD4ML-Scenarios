import joblib
from wickedhot import OneHotEncoder
from cd4ml.train import get_trained_model
from cd4ml.model_utils import get_target_id_features_lists
import logging
from cd4ml.utils.utils import mini_batch_eval
from cd4ml.available_models import get_model_type


class MLModel:
    def __init__(self, algorithm_name,
                 algorithm_params,
                 feature_set,
                 encoder,
                 random_seed):

        self.logger = logging.getLogger(__name__)
        self.algorithm_name = algorithm_name
        self.algorithm_params = algorithm_params
        self.random_seed = random_seed
        self.trained_model = None
        self.encoder = encoder
        self.feature_set = feature_set
        self.packaged_encoder = None
        self.model_type = get_model_type(self.algorithm_name)

    def load_encoder_from_package(self):
        self.logger.info('loading encoder from packaging')
        self.encoder = OneHotEncoder([], [])
        self.encoder.load_from_packaged_data(self.packaged_encoder)

    def predict_encoded_rows(self, encoded_row_list):
        # needs a list not a stream
        # for batch or mini-batch calls
        # eliminates model scoring overhead

        preds = self.trained_model.predict(encoded_row_list)
        if self.model_type == 'regressor':
            return [float(pred) for pred in preds]
        else:
            return [str(pred) for pred in preds]

    def predict_prob_encoded_rows(self, encoded_row_list):
        # needs a list not a stream
        # for batch or mini-batch calls
        # eliminates model scoring overhead
        if self.model_type == 'regressor':
            raise NotImplementedError('predict_prob_encoded_rows not implemented for regressor models')

        pred_probs = self.trained_model.predict_proba(encoded_row_list)
        return pred_probs

    def predict_single_processed_row(self, processed_row):
        # don't call this on each element of a stream or list
        # call it when you really only have one to predict
        # not performant when called many times
        # use predict_processed_rows for that instead
        self.logger.debug('processed_row', processed_row)
        return list(self.predict_processed_rows([processed_row]))[0]

    def predict_prob_single_processed_row(self, processed_row):
        # same for prob
        self.logger.debug('processed_row', processed_row)
        return list(self.predict_prob_processed_rows([processed_row]))[0]

    def predict_processed_rows(self, processed_row_stream, prob=False):
        # minibatch prediction is much faster because of overhead
        # of model scoring call

        if self.encoder is None:
            # in case it has been packaged
            self.load_encoder_from_package()
            self.packaged_encoder = None

        batch_size = 1000

        feature_row_stream = (self.feature_set.features(row) for row in processed_row_stream)
        encoded_row_stream = (self.encoder.encode_row(feature_row) for feature_row in feature_row_stream)

        if prob:
            function = self.predict_prob_encoded_rows
        else:
            function = self.predict_encoded_rows

        return mini_batch_eval(encoded_row_stream, batch_size, function)

    def _get_target_id_features_lists_training(self, training_processed_stream):

        return get_target_id_features_lists(self.feature_set.identifier_field,
                                            self.feature_set.target_field,
                                            self.feature_set,
                                            training_processed_stream)

    def train(self, training_processed_stream):
        # reads in the streams to lists of dicts, trains model and then
        # deletes the data to free up memory
        target_data, identifiers, features = self._get_target_id_features_lists_training(training_processed_stream)
        encoded_training_data = [self.encoder.encode_row(feature_row) for feature_row in features]
        del features, identifiers

        self.trained_model = get_trained_model(self.algorithm_name,
                                               self.algorithm_params,
                                               encoded_training_data,
                                               target_data,
                                               self.random_seed)

        del encoded_training_data

    def save(self, filename):
        # The encoder apparently is not pickleable.
        # No problem. The encoder has built in serialization
        # so make use if it.
        self.packaged_encoder = self.encoder.package_data()
        self.encoder = None
        joblib.dump(self, filename)
