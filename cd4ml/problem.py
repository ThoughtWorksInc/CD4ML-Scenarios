from time import time
from cd4ml import tracking
from cd4ml.get_encoder import get_trained_encoder
from cd4ml.validate import write_validation_info
from cd4ml.validation_metrics import get_validation_metrics
from cd4ml.filenames import get_filenames
from cd4ml.ml_model import MLModel
from cd4ml.feature_importance import get_feature_importance


class Problem:
    """
    Generic Problem Interface for Problems
    Implementation needs to add various data elements and methods
    """

    def __init__(self, feature_set_name='default',
                 problem_params_name='default',
                 ml_params_name='default',
                 algorithm_name='default'):

        self.validation_metric_names = ['r2_score', 'rms_score', 'mad_score', 'num_validated']

        # attributes to be filled in by derived class
        self.pipeline_params = None
        self.problem_name = None
        self.feature_set = None

        self.feature_set_name = feature_set_name
        self.problem_params_name = problem_params_name
        self.ml_params_name = ml_params_name
        self.algorithm_name = algorithm_name

        # methods to be implemented

        # when called on pipeline_params, returns a data stream
        self._stream_data = None

        # when given a row of data, returns True or False depending on
        # whether is in training or validation
        # override if need a special case

        self.training_filter = None
        self.validation_filter = None

        # function which runs on a function returning an iterable
        # of (true, predicted) values
        # and returns a dictionary of metrics
        # might have to run multiple times so needs to create new
        # streams when called

        self.get_validation_metrics = None

        # filled in by methods in base class
        self.trained_model = None
        self.validation_metrics = None
        self.encoder = None
        self.ml_model = None
        self.tracker = None
        self.feature_data = None
        self.importance = None

    def _post_init(self):
        # Call this after the derived class __init__ is called
        # TODO: a little awkward, where does identifier_field really belong
        self.feature_set.identifier_field = self.pipeline_params['problem_params']['identifier_field']

    def stream_processed(self):
        return self._stream_data(self.pipeline_params)

    def stream_features(self):
        return (self.feature_set.features(processed_row) for processed_row in self.stream_processed())

    def prepare_feature_data(self):
        pass

    def get_encoder(self, write=False, read_from_file=False):
        # TODO: train on all featuress of just training?
        self.prepare_feature_data()

        start = time()
        ml_fields = self.feature_set.ml_fields()
        omitted = self.feature_set.params['encoder_untransformed_fields']

        self.encoder = get_trained_encoder(self.stream_features(),
                                           ml_fields,
                                           self.pipeline_params['problem_name'],
                                           write=write,
                                           read_from_file=read_from_file,
                                           base_features_omitted=omitted)

        self.encoder.add_numeric_stats(self.stream_features())

        runtime = time() - start
        print('Encoder time: %0.1f seconds' % runtime)

    def training_stream(self):
        return (row for row in self.stream_processed() if self.training_filter(row))

    def validation_stream(self):
        return (row for row in self.stream_processed() if self.validation_filter(row))

    def train(self):
        print('Training')
        start = time()
        if self.encoder is None:
            self.get_encoder()

        self.ml_model = MLModel(self.pipeline_params,
                                self.feature_set,
                                self.encoder,
                                self.tracker)

        self.ml_model.train(self.training_stream())

        model_name = self.pipeline_params['problem_params']['model_name']
        self.importance = get_feature_importance(self.ml_model.trained_model, model_name, self.encoder)

        runtime = time() - start
        print('Training time: %0.1f seconds' % runtime)

    def true_target_stream(self, stream):
        target_name = self.feature_set.params['target_field']
        return (row[target_name] for row in stream)

    def _write_validation_info(self):
        true_validation_target = list(self.true_target_stream(self.validation_stream()))
        validation_predictions = list(self.ml_model.predict_processed_rows(self.validation_stream()))

        write_validation_info(self.validation_metrics,
                              self.tracker,
                              true_validation_target,
                              validation_predictions,
                              self.problem_name)

    def validate(self):
        print('Validating')
        start = time()

        def get_validation_stream():
            true_validation_target_stream = self.true_target_stream(self.validation_stream())
            validation_prediction_stream = self.ml_model.predict_processed_rows(self.validation_stream())

            validation_stream = zip(true_validation_target_stream, validation_prediction_stream)
            return validation_stream

        # one downside of these next two steps is that they score the same data twice
        # but that isn't really a major performance hit overall

        print('Getting validation metrics')
        self.validation_metrics = get_validation_metrics(self.validation_metric_names, get_validation_stream)
        print('Writing validation info')
        self._write_validation_info()
        runtime = time() - start
        print('Validation time: %0.1f seconds' % runtime)

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
        file_names = get_filenames(self.problem_name)
        filename = file_names['full_model']
        print("Writing full model to: %s" % filename)
        self.ml_model.save(filename)

    def run_all(self):
        start = time()
        with tracking.track() as tracker:
            self.tracker = tracker

            self.get_encoder()
            self.train()
            self.validate()
            self.write_ml_model()

        runtime = time() - start
        print('All ML steps time: %0.1f seconds' % runtime)
