import os
import json


def get_feature_params(this_file):
    """
    Get the feature params from the same directory as the feature_set
    :param this_file: __file__ from calling scope
    :return: dictionary of params
    """
    this_dir = os.path.dirname(this_file)
    param_file = "%s/%s" % (this_dir, 'params.json')
    return json.load(open(param_file, 'r'))
