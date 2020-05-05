import joblib
from wickedhot import OneHotEncoder


class MLModel:
    def __init__(self, pipeline_params, trained_model, encoder):
        self.pipeline_params = pipeline_params
        self.trained_model = trained_model
        self.encoder = encoder
        self.packaged_encoder = None

    def predict_encoded_row(self, encoded_row):
        pred = self.trained_model.predict([encoded_row])[0]
        return float(pred)

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

    def predict_stream(self, stream):
        return (self.predict_row(row) for row in stream)

    def save(self, filename):
        # The encoder apparently is not pickelable.
        # No problem. The encoder has built in serialization
        # so make use if it.
        self.packaged_encoder = self.encoder.package_data()
        self.encoder = None
        joblib.dump(self, filename)
