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


def get_generic_feature_set(identifier_field,
                            target_field,
                            info,
                            this_file,
                            feature_set_class):
    """
    The function to call from Problem class. This makes the FeatureSet class
    referentially transparent and therefore easier to test
    :param identifier_field: field identifying each row, e.g. primary key
    :param target_field: the target fields
    :param info: a dictionary of any needed data such as lookups
    :param this_file: __file__ from the calling scope
    :param feature_set_class: the FeatureSet class from the same calling scope
    :return: Instantiated FeatureSet object with its particular params read from
        it's matching json file
    """
    feature_set_params = get_feature_params(this_file)

    return feature_set_class(identifier_field, target_field, info, feature_set_params)
