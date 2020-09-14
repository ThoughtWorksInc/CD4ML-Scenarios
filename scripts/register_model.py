import argparse

from cd4ml.register_model import register_model
from scripts.common_arg_parsers import get_model_id_location


def parse_arguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("registry_host_name",
                        help="The model_id folder to use to report",
                        nargs='?',
                        default="http://localhost:12000")
    parser.add_argument("did_pass_acceptance_test",
                        help="The model_id folder to use to report",
                        nargs='?',
                        default="not-checked")
    parser.add_argument("model_id",
                        help="The model_id folder to use to report",
                        nargs='?',
                        default=None)

    parsed_args = parser.parse_args(args)
    model_id = get_model_id_location(parsed_args.model_id)

    return parsed_args.registry_host_name, parsed_args.did_pass_acceptance_test, model_id


def main(args):
    """
    Register the model with the model registry
    """
    registry_host_name, did_pass_acceptance_test, model_id = parse_arguments(args)
    register_model(model_id, registry_host_name, did_pass_acceptance_test)
