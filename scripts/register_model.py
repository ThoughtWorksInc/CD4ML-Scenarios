from cd4ml.register_model import register_model
from cd4ml.utils.problem_utils import get_last_model_subdir


def main(*args):
    """
    Check model meets acceptance threshold
    """
    args = args[0]

    if len(args) > 0:
        host_name = args[0]
    else:
        # for the local environment only, Jenkins will give the
        # relevant url
        host_name = "http://localhost:12000"

    if len(args) > 1:
        model_id = args[1]
    else:
        latest_subdir = get_last_model_subdir()
        model_id = latest_subdir.split('/')[-1]

    register_model(model_id, host_name)
