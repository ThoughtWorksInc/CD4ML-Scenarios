# parameters for running the pipeline

pipeline_params = {'problem': 'shopping'}

if pipeline_params['problem'] == 'shopping':
    from cd4ml.problems.shopping.config.problem_params import problem_params
    from cd4ml.problems.shopping.config.ml_model_params import model_parameters
elif pipeline_params['problem'] == 'zillow':
    from cd4ml.problems.zillow.config.problem_params import problem_params
    from cd4ml.problems.zillow.config.ml_model_params import model_parameters
else:
    raise ValueError("Problem %s, must be one of 'shopping' or 'zillow'" % pipeline_params['problem'])

pipeline_params['problem_params'] = problem_params
pipeline_params['model_params'] = model_parameters
