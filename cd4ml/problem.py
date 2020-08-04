from time import time
from cd4ml import tracking
from cd4ml.get_encoder import get_trained_encoder
from cd4ml.validate import write_validation_info
from cd4ml.validation_metrics import get_validation_metrics
from cd4ml.filenames import get_filenames
from cd4ml.ml_model import MLModel
from cd4ml.feature_importance import get_feature_importance
from cd4ml.splitter import splitter
from cd4ml.problem_utils import get_ml_pipeline_params, Specification
from cd4ml.problem_utils import get_feature_set_class, get_algorithm_params


class ProblemBase:
    """
    Generic Problem Interface for Problems
    Implementation needs to add various data elements and methods
    """

    def __init__(self,
                 problem_name,
                 feature_set_name='default',
                 ml_pipeline_params_name='default',
                 algorithm_name='default',
                 algorithm_params_name='default'):

        self.ml_pipeline_params = get_ml_pipeline_params(problem_name, ml_pipeline_params_name, __file__)

        if algorithm_name == 'default':
            algorithm_name_actual = self.ml_pipeline_params['default_algorithm']
        else:
            algorithm_name_actual = algorithm_name

        self.specification = Specification(problem_name,
                                           ml_pipeline_params_name,
                                           feature_set_name,
                                           algorithm_name,
                                           algorithm_params_name,
                                           algorithm_name_actual)

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

        self.training_filter, self.validation_filter = splitter(self.ml_pipeline_params)

        feature_set_class = get_feature_set_class(problem_name, feature_set_name, __file__)

        self.feature_set = feature_set_class(self.ml_pipeline_params['identifier_field'],
                                             self.ml_pipeline_params['target_field'],
                                             {})

        self.algorithm_params = get_algorithm_params(__file__,
                                                     problem_name,
                                                     algorithm_name_actual,
                                                     algorithm_params_name)

    def stream_processed(self):
        return self._stream_data(self.specification.spec['problem_name'])

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
                                           self.specification.spec['problem_name'],
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

        self.ml_model = MLModel(self.specification.spec['algorithm_name_actual'],
                                self.algorithm_params,
                                self.feature_set,
                                self.encoder,
                                self.tracker,
                                self.ml_pipeline_params['training_random_seed'])

        self.ml_model.train(self.training_stream())

        model_name = self.specification.spec['algorithm_name_actual']
        self.importance = get_feature_importance(self.ml_model.trained_model, model_name, self.encoder)

        runtime = time() - start
        print('Training time: %0.1f seconds' % runtime)

    def true_target_stream(self, stream):
        target_name = self.feature_set.target_field
        return (row[target_name] for row in stream)

    def _write_validation_info(self):
        file_names = get_filenames(self.specification.spec['problem_name'],
                                   self.specification.problem_specification_name())

        true_validation_target = list(self.true_target_stream(self.validation_stream()))
        validation_predictions = list(self.ml_model.predict_processed_rows(self.validation_stream()))

        write_validation_info(self.validation_metrics,
                              self.tracker,
                              true_validation_target,
                              validation_predictions,
                              file_names)

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

        validation_metric_names = self.ml_pipeline_params['validation_metric_names']
        self.validation_metrics = get_validation_metrics(validation_metric_names, get_validation_stream)
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
        file_names = get_filenames(self.specification.spec['problem_name'],
                                   self.specification.problem_specification_name())

        filename = file_names['full_model']
        print("Writing full model to: %s" % filename)
        self.ml_model.save(filename)
        self.tracker.log_artifact(filename)

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
