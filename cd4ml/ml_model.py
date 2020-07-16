import joblib
from wickedhot import OneHotEncoder
from cd4ml.utils import mini_batch_eval


class MLModel:
    def __init__(self, pipeline_params, trained_model, encoder):
        self.pipeline_params = pipeline_params
        self.trained_model = trained_model
        self.encoder = encoder
        self.packaged_encoder = None

    def predict_encoded_row(self, encoded_row):
        pred = self.trained_model.predict([encoded_row])[0]
        return float(pred)

    def predict_encoded_rows(self, encoded_rows):
        preds = self.trained_model.predict(encoded_rows)
        return [float(pred) for pred in preds]

    def load_encoder_from_package(self):
        print('loading encoder from packaging')
        self.encoder = OneHotEncoder([], [])
        self.encoder.load_from_packaged_data(self.packaged_encoder)

    def predict_row(self, row):
        if self.encoder is None:
            # in case it has been packaged
            self.load_encoder_from_package()
            self.packaged_encoder = None

        encoded_row = self.encoder.encode_row(row)
        return self.predict_encoded_row(encoded_row)

    def predict_rows(self, rows):
        if self.encoder is None:
            # in case it has been packaged
            self.load_encoder_from_package()
            self.packaged_encoder = None

        encoded_rows = [self.encoder.encode_row(row) for row in rows]
        return self.predict_encoded_rows(encoded_rows)

    def predict_stream_slow(self, stream):
        return (self.predict_row(row) for row in stream)

    def predict_stream(self, stream):
        batch_size = 1000
        return mini_batch_eval(stream, batch_size, self.predict_rows)

    def save(self, filename):
        # The encoder apparently is not pickelable.
        # No problem. The encoder has built in serialization
        # so make use if it.
        self.packaged_encoder = self.encoder.package_data()
        self.encoder = None
        joblib.dump(self, filename)
