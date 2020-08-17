from cd4ml.problems.problem_base import ProblemBase
import cd4ml.problems.iris.readers.stream_data as stream_data


class Problem(ProblemBase):
    def __init__(self,
                 problem_name,
                 data_downloader='default',
                 ml_pipeline_params_name='default',
                 feature_set_name='default',
                 algorithm_name='default',
                 algorithm_params_name='default'):

        super(Problem, self).__init__(problem_name,
                                      data_downloader=data_downloader,
                                      feature_set_name=feature_set_name,
                                      ml_pipeline_params_name=ml_pipeline_params_name,
                                      algorithm_name=algorithm_name,
                                      algorithm_params_name=algorithm_params_name)

        self._stream_data = stream_data.stream_data

    def get_feature_set_class(self, feature_set_name):

        if feature_set_name == 'default':
            import cd4ml.problems.iris.feature_sets.default as default_features
            return default_features.FeatureSet
        else:
            raise ValueError("Featureset name {} is not valid".format(feature_set_name))

    def prepare_feature_data(self):
        pass

    def download_data(self):
        import cd4ml.problems.iris.download_data.download_data as dd
        dd.download()
