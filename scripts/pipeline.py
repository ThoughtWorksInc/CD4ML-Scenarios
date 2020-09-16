import argparse

import logging
from cd4ml.problems import get_problem, list_available_scenarios

DEFAULT_ARGUMENT = 'default'


def make_argument_parser():
    list_of_arguments = [
        {'arg_name': "ml_pipeline_params_name", 'help': "The name of the problem to Run"},
        {'arg_name': "feature_set_name", 'help': "The name of the problem to Run"},
        {'arg_name': "algorithm_name", 'help': "The name of the problem to Run"},
        {'arg_name': "algorithm_params_name", 'help': "The name of the problem to Run"}
    ]
    parser = argparse.ArgumentParser()
    parser.add_argument("problem_name",
                        help="The name of the problem to run",
                        choices=list_available_scenarios(),
                        nargs='?',
                        default="houses")

    for arg in list_of_arguments:
        parser.add_argument(arg['arg_name'],
                            help=arg['help'],
                            nargs='?',
                            default=DEFAULT_ARGUMENT)
    return parser


def main(args):
    """
    Run the pipeline
    """
    logger = logging.getLogger(__name__)
    arg_parser = make_argument_parser()

    parsed_args = arg_parser.parse_args(args)
    problem_name = parsed_args.problem_name

    ml_pipeline_params_name = parsed_args.ml_pipeline_params_name
    feature_set_name = parsed_args.feature_set_name
    algorithm_name = parsed_args.algorithm_name
    algorithm_params_name = parsed_args.algorithm_params_name

    logger.info(f'Desired Problem to Run: {problem_name}')
    # TODO: Allow a different data_downloader

    problem = get_problem(problem_name,
                          data_downloader=DEFAULT_ARGUMENT,
                          ml_pipeline_params_name=ml_pipeline_params_name,
                          feature_set_name=feature_set_name,
                          algorithm_name=algorithm_name,
                          algorithm_params_name=algorithm_params_name)

    # Call the run_all method, which will perform the entire data pipeline
    problem.run_all()
