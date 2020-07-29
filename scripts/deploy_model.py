from cd4ml.deploy_model import deploy_model
from cd4ml.get_problem import get_problem


def main(*args):
    """
    Check model meets acceptance threshold
    """
    args = args[0]
    print('args')
    print(args)
    if len(args) > 0:
        host_name = args[0]
    else:
        host_name = None

    problem = get_problem()
    problem_name = problem.problem_name
    deploy_model(problem_name, host_name=host_name)
