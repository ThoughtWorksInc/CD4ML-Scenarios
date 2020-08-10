from cd4ml.deploy_model import deploy_model


def main(*args):
    """
    Check model meets acceptance threshold
    """
    args = args[0]

    host_name = args[0]
    problem_name = args[1]
    ml_pipeline_params_name = args[2]
    feature_set_name = args[3]
    algorithm_name = args[4]
    algorithm_params_name = args[5]
    did_pass_acceptance = args[6]

    deploy_model(problem_name,
                 ml_pipeline_params_name,
                 feature_set_name,
                 algorithm_name,
                 algorithm_params_name,
                 did_pass_acceptance,
                 host_name=host_name)
