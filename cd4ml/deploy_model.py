import requests
from cd4ml.filenames import get_filenames
from cd4ml.problem_utils import Specification


def deploy_model(problem_name,
                 ml_pipeline_params_name,
                 feature_set_name,
                 algorithm_name,
                 algorithm_params_name,
                 host_name=None):

    spec = Specification(problem_name,
                         feature_set_name,
                         ml_pipeline_params_name,
                         algorithm_name,
                         algorithm_params_name,
                         '')

    spec_name = spec.problem_specification_name()
    print('spec_name', spec_name)
    file_names = get_filenames(problem_name, problem_specification_name=spec_name)
    model_file = file_names['full_model']

    if host_name is None:
        host_name = "http://localhost:5005"

    # maybe choose a better separator?
    url = "{host_name}/replace_model/{spec_name}".format(spec_name=spec_name,
                                                         host_name=host_name)
    with open(model_file, 'rb') as fp:
        data_binary = fp.read()

    print('data_binary size:', len(data_binary))

    print('url: ', url)
    res = requests.post(url=url, data=data_binary)
    print(res.status_code)
