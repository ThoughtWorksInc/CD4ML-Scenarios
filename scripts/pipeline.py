import numpy as np
from cd4ml import pipeline_helpers as ph
from cd4ml.pipeline_params import pipeline_params


def main(*args):
    """
    Run the pipeline
    """
    args = args[0]
    if len(args) > 0:
        variable = args[0]
    else:
        variable = None

    np.random.seed(462748)

    if variable:
        print('variable: %s' % variable)

    if pipeline_params["data_source"] == "file":
        ph.download_data(pipeline_params)

    ph.train_and_validate_model(pipeline_params)
