# parameters for running the pipeline

from cd4ml.problems.shopping.config.problem_params import problem_params
from cd4ml.problems.shopping.config.ml_model_params import model_parameters
from cd4ml.problems.shopping.config.ml_fields import get_ml_fields

pipeline_params = {'problem_name': 'shopping',
                   'problem_params': problem_params,
                   'model_params': model_parameters,
                   'ml_fields': get_ml_fields()}
