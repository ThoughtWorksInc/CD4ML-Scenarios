import joblib
from cd4ml import tracking
from cd4ml.train import get_trained_model
from cd4ml.get_encoder import get_encoder
from cd4ml.validate import write_validation_info
from cd4ml.validation_metrics import get_validation_metrics
from cd4ml.filenames import file_names
from cd4ml.ml_model import MLModel


class Problem:
    """
    Generic Problem Interface
    Implementation needs to add various data elements and methods
    """

    def __init__(self):
        # attributes to be filled in
        self.pipeline_params = None
        self.problem_name = None
        self.trained_model = None
        self.validation_metrics = None
        self.encoder = None
        self.ml_model = None
        self.validation_metrics = ['r2_score', 'rms_score', 'mad_score']

        # methods to be implemented

        # when called on pipeline_params, returns a data stream
        self._stream_data = None

        # when given a row of data, returns True if it is in training set
        self.training_filter = None

        # when given a row of data, returns True if it is in validation set
        self.validation_filter = None

        # function which runs on a function returning an iterable
        # of (true, predicted) values
        # and returns a dictionary of metrics
        # might have to run multiple times so needs to create new
        # streams when called
        self.get_validation_metrics = None

    def stream(self):
        return self._stream_data(self.pipeline_params)

    def get_encoder(self, write=True, read_from_file=False):
        self.encoder = get_encoder(self.stream(),
                                   self.pipeline_params['ml_fields'],
                                   write=write,
                                   read_from_file=read_from_file)

    def training_stream(self):
        return (row for row in self.stream() if self.training_filter(row))

    def validation_stream(self):
        return (row for row in self.stream() if self.validation_filter(row))

    def train(self):
        if self.encoder is None:
            self.get_encoder()

        trained_model = get_trained_model(self.pipeline_params,
                                          self.training_stream,
                                          self.encoder)
        self.ml_model = MLModel(self.pipeline_params, trained_model, self.encoder)

    def true_target_stream(self, stream):
        target_name = self.pipeline_params['ml_fields']['target_name']
        return (row[target_name] for row in stream)

    def _write_validation_info(self):
        true_validation_target = list(self.true_target_stream(self.validation_stream()))
        validation_predictions = list(self.ml_model.predict_stream(self.validation_stream()))

        with tracking.track() as track:
            write_validation_info(self.validation_metrics,
                                  self.trained_model, track,
                                  true_validation_target,
                                  validation_predictions)

    def validate(self):
        def get_validation_stream():
            true_validation_target_stream = self.true_target_stream(self.validation_stream())
            validation_prediction_stream = self.ml_model.predict_stream(self.validation_stream())

            validation_stream = zip(true_validation_target_stream, validation_prediction_stream)
            return validation_stream

        self.validation_metrics = get_validation_metrics(self.validation_metrics, get_validation_stream)
        self._write_validation_info()

    def __repr__(self):
        # make it printable
        messages = ['Problem']
        for k, v in self.__dict__.items():
            if v is None:
                continue
            if str(v.__class__) == "<class 'function'>":
                continue
            messages.append("%s: \n%s\n" % (k, v))

        return '\n'.join(messages)

    def write_ml_model(self):
        filename = file_names['full_model']
        print("Writing full model to: %s" % filename)
        self.ml_model.save(filename)

    def run_all(self):
        self.get_encoder()
        self.train()
        self.validate()
        self.write_ml_model()

        test_persistence = False
        if test_persistence:
            # Test the read and write.
            # Validate a second time after rereading the model
            # from file
            reread_model = load_full_model()
            self.ml_model = reread_model
            self.validate()


def load_full_model():
    filename = file_names['full_model']
    print("Loading full model from: %s" % filename)
    return joblib.load(filename)
