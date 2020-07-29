import requests
from cd4ml.filenames import get_filenames
# 'curl --request POST --data-binary "@data/models/full_model.pkl" http://model:5005/replace_model'


def deploy_model(problem_name, host_name=None):
    file_names = get_filenames(problem_name)
    model_file = file_names['full_model']
    # TODO: how to get correct url
    # url = "http://model:5005/replace_model/{problem_name}".format(problem_name=problem_name)

    if host_name is None:
        host_name = "http://localhost:5005"

    url = "{host_name}/replace_model/{problem_name}".format(problem_name=problem_name,
                                                            host_name=host_name)

    print(model_file)
    with open(model_file, 'rb') as fp:
        data_binary = fp.read()

    print('data_binary size:', len(data_binary))

    res = requests.post(url=url, data=data_binary)
    print(res.status_code)
