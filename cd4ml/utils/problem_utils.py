class Specification:
    def __init__(self,
                 problem_name,
                 data_downloader,
                 ml_pipeline_params_name,
                 feature_set_name,
                 algorithm_name,
                 algorithm_params_name,
                 algorithm_name_actual):

        self.spec = {'problem_name': problem_name,
                     'data_downloader': data_downloader,
                     'ml_pipeline_params_name': ml_pipeline_params_name,
                     'feature_set_name': feature_set_name,
                     'algorithm_name': algorithm_name,
                     'algorithm_name_actual': algorithm_name_actual,
                     'algorithm_params_name': algorithm_params_name,
                     'git_hash': "NOTIMPLEMENTED"}

    def problem_specification_name(self, with_git_hash=False):
        sep = "$"

        parts = ['{problem_name}',
                 '{ml_pipeline_params_name}',
                 '{feature_set_name}',
                 '{algorithm_name}',
                 '{algorithm_params_name}']

        template = sep.join(parts)
        string = template.format(**self.spec)
        if with_git_hash:
            string = string + '#' + self.spec['git_hash']

        return string


